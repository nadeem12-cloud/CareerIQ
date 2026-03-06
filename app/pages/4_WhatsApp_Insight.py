import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
from utils.ui_components import inject_css, navbar, page_header

try:
    from whatsapp_utils import send_whatsapp_message
    WHATSAPP_AVAILABLE = True
except Exception:
    try:
        from app.whatsapp_utils import send_whatsapp_message
        WHATSAPP_AVAILABLE = True
    except Exception:
        WHATSAPP_AVAILABLE = False

st.set_page_config(page_title="WhatsApp – CareerIQ", page_icon="📲", layout="wide", initial_sidebar_state="collapsed")
inject_css()
navbar("WhatsApp")

df = load_data()
df = preprocess_data(df)

page_header("📲", "WhatsApp Market Insight", "Generate and share hiring intelligence reports")

st.markdown(
    """<div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);
                   border-radius:8px;padding:0.75rem 1rem;margin-bottom:1rem;">
      <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#00D4FF;
                   letter-spacing:1px;">DEMO MODE</span>
      <span style="font-family:'DM Sans',sans-serif;font-size:0.85rem;color:#94A3B8;
                   margin-left:0.75rem;">
        WhatsApp delivery works to the registered demo number via Twilio Sandbox.
      </span>
    </div>""", unsafe_allow_html=True)

# ── Filters in main area ───────────────────────────────────────────────────────
with st.expander("🔽  Filters", expanded=False):
    fc1, fc2 = st.columns(2)
    role_filter = fc1.multiselect("Role",
        sorted(df["job_group"].dropna().unique()), placeholder="All", key="wa_roles")
    loc_filter  = fc2.multiselect("City",
        sorted(df["clean_location"].dropna().unique()), placeholder="All", key="wa_locs")

fdf = df.copy()
if role_filter: fdf = fdf[fdf["job_group"].isin(role_filter)]
if loc_filter:  fdf = fdf[fdf["clean_location"].isin(loc_filter)]

if fdf.empty:
    st.warning("No data for selected filters.")
    st.stop()

top_roles  = fdf["job_group"].value_counts().head(3)
top_cities = fdf["clean_location"].value_counts().head(3)
exp_dist   = fdf["experience"].value_counts(normalize=True) * 100
top_exp    = exp_dist.idxmax()
top_exp_pct = round(exp_dist.max())

role_lines = "\n".join(f"  {i+1}. {r} — {c} jobs" for i,(r,c) in enumerate(top_roles.items()))
city_lines = "\n".join(f"  {i+1}. {c} — {n} openings" for i,(c,n) in enumerate(top_cities.items()))

message = f"""◈ CareerIQ — Market Intelligence Report

📌 Jobs Analysed: {len(fdf):,}

🔥 Top Hiring Roles:
{role_lines}

🌍 Top Hiring Cities:
{city_lines}

🎯 Experience Sweet Spot:
  {top_exp} years  ({top_exp_pct}% of roles)

💡 Insight:
  Target {top_roles.index[0]} roles in {top_cities.index[0]}
  if you have {top_exp} yrs experience.

Stay skilled. Stay relevant.
——
Powered by CareerIQ"""

col_prev, col_send = st.columns([3, 2])

with col_prev:
    st.markdown("#### Message Preview")
    st.markdown(
        f"""<div style="background:#111827;border:1px solid #1E2D45;border-radius:12px;
                        padding:1.25rem 1.5rem;font-family:'Space Mono',monospace;
                        font-size:0.78rem;color:#E2E8F0;white-space:pre-wrap;line-height:1.8;">
{message}</div>""", unsafe_allow_html=True)

with col_send:
    st.markdown("#### Send Report")
    k1, k2 = st.columns(2)
    k1.metric("Jobs", f"{len(fdf):,}")
    k2.metric("Top Role", top_roles.index[0].split()[0])
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    if st.button("📲  Send to WhatsApp", type="primary", use_container_width=True):
        if WHATSAPP_AVAILABLE:
            try:
                send_whatsapp_message(message)
                st.success("✅ Sent to demo number!")
            except Exception as e:
                st.error(f"Send failed: {e}")
        else:
            st.error("whatsapp_utils not loaded.")

    st.markdown(
        """<div style="font-family:'DM Sans',sans-serif;font-size:0.78rem;
                       color:#475569;margin-top:0.75rem;line-height:1.5;">
          Delivery via Twilio Sandbox.<br>
          Only the registered demo number receives messages.
        </div>""", unsafe_allow_html=True)
