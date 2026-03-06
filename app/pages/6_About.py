import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ui_components import inject_css, sidebar_logo, page_header

st.set_page_config(page_title="About – CareerIQ", page_icon="ℹ️", layout="wide")
inject_css()
sidebar_logo()

page_header("◈", "About CareerIQ", "Data-driven job market intelligence for India's tech sector")

# ── Overview ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="insight-card" style="margin-bottom:1rem;">
      <div class="insight-card-label">What is CareerIQ?</div>
      <div style="font-family:'DM Sans',sans-serif;font-size:0.9rem;color:#94A3B8;
                  line-height:1.8;margin-top:8px;">
        CareerIQ transforms raw job listing data into structured career intelligence.
        It helps students understand hiring demand, professionals identify skill gaps,
        and researchers observe market trends — all from a single unified platform.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card">
      <div class="insight-card-label">Problem It Solves</div>
      <div style="font-family:'DM Sans',sans-serif;font-size:0.9rem;color:#94A3B8;
                  line-height:1.8;margin-top:8px;">
        Job seekers rely on scattered portals with no structured insight. CareerIQ
        converts raw listings into analytics — role demand, skill frequency, experience
        distribution, and location-based hiring intensity.
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-card">
      <div class="insight-card-label">Tech Stack</div>
      <div style="margin-top:10px;display:flex;flex-direction:column;gap:8px;">
    """, unsafe_allow_html=True)

    for tech, desc in [
        ("Python", "Core language"),
        ("Streamlit", "Web framework"),
        ("Pandas", "Data processing"),
        ("Plotly", "Visualisations"),
        ("BeautifulSoup", "Web scraping"),
        ("Twilio API", "WhatsApp integration"),
    ]:
        st.markdown(
            f"""<div style="display:flex;justify-content:space-between;align-items:center;
                            padding:6px 0;border-bottom:1px solid #1E2D45;">
              <span style="font-family:'Space Mono',monospace;font-size:0.75rem;
                           color:#00D4FF;">{tech}</span>
              <span style="font-family:'DM Sans',sans-serif;font-size:0.75rem;
                           color:#64748B;">{desc}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

st.divider()

# ── Architecture ──────────────────────────────────────────────────────────────
st.markdown("#### System Architecture")
arch_cols = st.columns(4)
layers = [
    ("01", "Data Layer",        "Raw job datasets · Naukri scraper · CSV pipeline"),
    ("02", "Processing Layer",  "Skill extraction · Role mapping · Location cleanup"),
    ("03", "Analytics Layer",   "Dashboard · Skills intelligence · Trend analysis"),
    ("04", "Comms Layer",       "WhatsApp automation via Twilio sandbox"),
]
for col, (num, title, desc) in zip(arch_cols, layers):
    col.markdown(
        f"""<div class="insight-card" style="height:140px;">
          <div style="font-family:'Space Mono',monospace;font-size:1.4rem;
                      color:#1E2D45;font-weight:700;">{num}</div>
          <div style="font-family:'Space Mono',monospace;font-size:0.75rem;
                      color:#00D4FF;margin:4px 0;">{title}</div>
          <div style="font-family:'DM Sans',sans-serif;font-size:0.78rem;
                      color:#64748B;line-height:1.6;">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ── Future scope ──────────────────────────────────────────────────────────────
st.markdown("#### Future Scope")
future_cols = st.columns(3)
futures = [
    ("🔐", "User Auth",          "Personalised dashboards per user profile"),
    ("🤖", "AI Recommendations", "Resume ↔ skill gap analysis with LLMs"),
    ("☁️", "SaaS Deployment",    "Scalable cloud deployment with live APIs"),
]
for col, (icon, title, desc) in zip(future_cols, futures):
    col.markdown(
        f"""<div class="insight-card">
          <div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>
          <div style="font-family:'Space Mono',monospace;font-size:0.78rem;
                      color:#E2E8F0;font-weight:700;">{title}</div>
          <div style="font-family:'DM Sans',sans-serif;font-size:0.78rem;
                      color:#64748B;margin-top:4px;line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.divider()
st.markdown(
    """<div style="font-family:'DM Sans',sans-serif;font-size:0.78rem;color:#334155;
                   text-align:center;padding:0.5rem 0;">
      ◈ CareerIQ — Academic project demonstrating data engineering &amp; analytics · 2026
    </div>""", unsafe_allow_html=True)
