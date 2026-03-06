import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plotly.express as px
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
from utils.ui_components import inject_css, navbar, page_header, plotly_theme

st.set_page_config(page_title="Dashboard – CareerIQ", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
inject_css()
navbar("Dashboard")

df = load_data()
df = preprocess_data(df)

page_header("📊", "Market Dashboard", "Hiring trends across Data · AI · ML · Cloud roles")

# ── Filters in main area (not sidebar) — immune to sidebar collapse bug ───────
with st.expander("🔽  Filters", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    job_filter = fc1.multiselect("Job Role",
        sorted(df["job_group"].dropna().unique()), placeholder="All roles", key="d_roles")
    loc_filter = fc2.multiselect("Location",
        sorted(df["clean_location"].dropna().unique()), placeholder="All cities", key="d_locs")
    compact = fc3.toggle("Compact charts", value=False, key="d_compact")

fdf = df.copy()
if job_filter: fdf = fdf[fdf["job_group"].isin(job_filter)]
if loc_filter: fdf = fdf[fdf["clean_location"].isin(loc_filter)]

roles_str = ", ".join(job_filter) if job_filter else "All Roles"
locs_str  = ", ".join(loc_filter) if loc_filter else "All Cities"
st.markdown(
    f'<div class="page-subtitle">Showing: <strong style="color:#E2E8F0;">{roles_str}</strong>'
    f' &nbsp;·&nbsp; <strong style="color:#E2E8F0;">{locs_str}</strong></div>',
    unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
market_ratio = len(fdf) / len(df) if len(df) > 0 else 0
if market_ratio > 0.4:   status_html = '<span class="market-strong">● STRONG MARKET</span>'
elif market_ratio > 0.2: status_html = '<span class="market-moderate">◐ MODERATE</span>'
else:                    status_html = '<span class="market-niche">○ NICHE SEGMENT</span>'

k1, k2, k3, k4 = st.columns(4)
k1.metric("Jobs Found",      f"{len(fdf):,}")
k2.metric("Unique Roles",    fdf["job_group"].nunique())
k3.metric("Active Cities",   fdf["clean_location"].nunique())
k4.metric("vs Total Market", f"{market_ratio:.0%}")
st.markdown(f"<div style='padding:0.25rem 0 1rem;'>{status_html}</div>", unsafe_allow_html=True)
st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
h = 320 if compact else 420
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Job Demand by Role")
    rc = fdf["job_group"].value_counts().reset_index()
    rc.columns = ["Role","Jobs"]
    fig = px.bar(rc, x="Role", y="Jobs", text="Jobs", color="Jobs",
        color_continuous_scale=[[0,"#1E2D45"],[1,"#00D4FF"]])
    fig.update_layout(**plotly_theme(), coloraxis_showscale=False, height=h)
    fig.update_traces(textfont_color="#94A3B8", marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Jobs by Location")
    lc = fdf["clean_location"].value_counts().head(6).reset_index()
    lc.columns = ["City","Jobs"]
    fig2 = px.pie(lc, names="City", values="Jobs", hole=0.52,
        color_discrete_sequence=["#00D4FF","#00FF94","#FFB800","#FF6B9D","#A78BFA","#FB923C"])
    fig2.update_layout(**plotly_theme(), height=h)
    fig2.update_traces(textfont_color="#E2E8F0", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.markdown("#### Experience Demand Breakdown")
exp_order = ["0-1","1-2","2-5","5-10","10+"]
ec = fdf["experience"].value_counts().reindex(exp_order, fill_value=0).reset_index()
ec.columns = ["Experience","Jobs"]
ec["pct"] = (ec["Jobs"] / ec["Jobs"].sum() * 100).round(1)
fig3 = px.bar(ec, x="Jobs", y="Experience", orientation="h", text="pct", color="Jobs",
    color_continuous_scale=[[0,"#1E2D45"],[0.5,"#0066CC"],[1,"#00D4FF"]])
fig3.update_layout(**plotly_theme(), coloraxis_showscale=False, height=280 if compact else 320)
fig3.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#94A3B8")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.markdown("#### Career Insight")
if not fdf.empty:
    top_role  = fdf["job_group"].value_counts().idxmax()
    top_city  = fdf["clean_location"].value_counts().idxmax()
    top_exp   = fdf["experience"].value_counts().idxmax()
    top_count = int(fdf["job_group"].value_counts().max())
    c1, c2, c3 = st.columns(3)
    for col, label, value, sub in [
        (c1, "Most In-Demand Role",    top_role,         f"{top_count} openings"),
        (c2, "Top Hiring City",        top_city,         ""),
        (c3, "Experience Sweet Spot",  f"{top_exp} yrs", "highest demand band"),
    ]:
        col.markdown(f"""<div class="insight-card">
            <div class="insight-card-label">{label}</div>
            <div class="insight-card-value">{value}</div>
            {'<div style="font-size:0.75rem;color:#64748B;margin-top:4px;">'+sub+'</div>' if sub else ''}
        </div>""", unsafe_allow_html=True)
else:
    st.warning("No data for selected filters.")
