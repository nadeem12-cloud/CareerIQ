"""CareerIQ – Data Refresh Page"""

import streamlit as st
import sys, os, time, pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import get_data_stats, force_reload, should_auto_refresh
from utils.scraper import (run_scrape_pipeline, SCRAPE_QUERIES,
                            get_api_key, test_api_connection)
from utils.ui_components import inject_css, sidebar_logo, page_header

st.set_page_config(page_title="Data Refresh – CareerIQ", page_icon="🔄", layout="wide")
inject_css()
sidebar_logo()

page_header("🔄", "Live Data Refresh", "Fetch latest LinkedIn job listings via JSearch API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRAPE_LOG_PATH = os.path.join(BASE_DIR, "Data", "Processed", "scrape_log.csv")

api_key = get_api_key()

# ── API key status ─────────────────────────────────────────────────────────────
if not api_key:
    st.markdown(
        """<div style="background:rgba(255,184,0,0.08);border:1px solid rgba(255,184,0,0.3);
                       border-radius:10px;padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
          <div style="font-family:'Space Mono',monospace;font-size:0.75rem;
                      color:#FFB800;letter-spacing:1px;margin-bottom:0.75rem;">⚠ RAPIDAPI KEY REQUIRED</div>
          <div style="font-family:'DM Sans',sans-serif;font-size:0.88rem;color:#94A3B8;line-height:2;">
            <strong style="color:#E2E8F0;">Step 1</strong> &nbsp;→&nbsp;
            <a href="https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch" target="_blank"
               style="color:#00D4FF;">rapidapi.com → JSearch</a>
            — sign up, subscribe to <strong style="color:#E2E8F0;">Basic (free)</strong><br>
            <strong style="color:#E2E8F0;">Step 2</strong> &nbsp;→&nbsp; Copy your <strong style="color:#E2E8F0;">X-RapidAPI-Key</strong><br>
            <strong style="color:#E2E8F0;">Step 3</strong> &nbsp;→&nbsp; Open
            <code style="background:#1A2235;padding:2px 8px;border-radius:4px;color:#00FF94;">
            app/.streamlit/secrets.toml</code> and add:<br>
            <code style="background:#0D2040;display:block;padding:10px 14px;border-radius:6px;
                          margin-top:6px;color:#00FF94;font-size:0.85rem;">
            RAPIDAPI_KEY = "paste_your_key_here"</code>
          </div>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown('<span class="badge-fresh">✓ API KEY CONFIGURED</span>',
                unsafe_allow_html=True)
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ── Dataset status ─────────────────────────────────────────────────────────────
st.markdown("#### Current Dataset")
stats = get_data_stats()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Records",  f"{stats['total_records']:,}" if stats["total_records"] else "0")
k2.metric("Data Age",       f"{stats['age_hours']}h" if stats.get("age_hours") else "Unknown")
k3.metric("Last Fetched",   stats["last_scraped"].split(" ")[0] if stats.get("last_scraped") else "Never")
k4.metric("Status",         "🔴 Stale" if stats["is_stale"] else "🟢 Fresh")

st.divider()

# ── Manual fetch ───────────────────────────────────────────────────────────────
st.markdown("#### Manual Fetch")

with st.expander("⚙️ Settings", expanded=False):
    pages = st.slider("Pages per query", 1, 5, 2,
        help="Each page returns ~10 jobs. 2 pages × 5 queries = ~100 jobs per fetch.")
    total_req = pages * len(SCRAPE_QUERIES)
    st.caption(f"Uses ~{total_req} API requests this run  ·  Free plan: 200 req/month")
    st.markdown("**Active queries:**")
    cols = st.columns(3)
    for i, q in enumerate(SCRAPE_QUERIES):
        cols[i % 3].markdown(
            f'<span class="stat-pill">{q["keyword"]}</span>', unsafe_allow_html=True)

fetch_clicked = st.button(
    "🚀  Fetch Latest Jobs", type="primary",
    use_container_width=True, disabled=not api_key)

if fetch_clicked:
    progress  = st.progress(0, text="Starting...")
    status_box = st.empty()

    for i, q in enumerate(SCRAPE_QUERIES):
        progress.progress(int(i / len(SCRAPE_QUERIES) * 75),
                          text=f"Fetching: {q['keyword']}...")
        time.sleep(0.15)

    with st.spinner("Calling JSearch API — this takes ~30 seconds..."):
        result = run_scrape_pipeline(pages_per_query=pages)
        force_reload()

    progress.progress(100, text="Done!")

    if result["error"] and result["new_records"] == 0:
        status_box.error(
            f"**Fetch failed:** `{result['error']}`\n\n"
            f"Use the **API Debug** panel below to diagnose.")
    elif result["new_records"] > 0:
        status_box.success(
            f"✅ **+{result['new_records']} new jobs added** · "
            f"Total: {result['total_records']:,} · "
            f"Time: {result['elapsed_seconds']}s")
    else:
        status_box.warning(
            f"Fetch ran but **0 new jobs** were found.\n\n"
            f"All {result['scraped_raw']} fetched listings already exist in the dataset, "
            f"or the API returned empty results.\n\n"
            f"→ Use **API Debug** below to confirm the API is responding with data.")

st.divider()

# ── API Debug Panel ────────────────────────────────────────────────────────────
st.markdown("#### API Debug")
st.markdown(
    '<div class="page-subtitle">Run a live test to see exactly what JSearch returns for your key.</div>',
    unsafe_allow_html=True)

if st.button("🔬  Run API Test", disabled=not api_key):
    with st.spinner("Testing connection..."):
        result = test_api_connection()

    c1, c2 = st.columns(2)
    c1.metric("HTTP Status",  result.get("status_code", "—"))
    c2.metric("Jobs Returned", result.get("jobs_count", 0))

    if result["ok"]:
        st.success("✅ API is working! JSearch returned job data successfully.")
        with st.expander("Sample job (first result)", expanded=True):
            job = result.get("sample_job", {})
            st.markdown(f"""
            <div class="insight-card">
              <div class="insight-card-label">Job Title</div>
              <div class="insight-card-value" style="font-size:1rem;">{job.get('job_title','—')}</div>
              <div style="display:flex;gap:2rem;margin-top:12px;flex-wrap:wrap;">
                <div><div class="insight-card-label">Company</div>
                     <div style="color:#E2E8F0;font-size:0.85rem;">{job.get('employer_name','—')}</div></div>
                <div><div class="insight-card-label">Location</div>
                     <div style="color:#E2E8F0;font-size:0.85rem;">{job.get('job_city','') or job.get('job_country','—')}</div></div>
                <div><div class="insight-card-label">Source</div>
                     <div style="color:#E2E8F0;font-size:0.85rem;">{job.get('job_publisher','—')}</div></div>
              </div>
            </div>""", unsafe_allow_html=True)
            with st.expander("Full raw JSON"):
                st.json(job)
    else:
        err = result.get("error","Unknown error")
        if "401" in str(result.get("status_code","")) or "INVALID" in err:
            st.error("**Invalid API key.** Go to rapidapi.com, copy your key again, and update secrets.toml.")
        elif "403" in str(result.get("status_code","")) or "FORBIDDEN" in err:
            st.error("**Not subscribed.** Go to JSearch on RapidAPI and subscribe to the free Basic plan.")
        elif "429" in str(result.get("status_code","")) or "RATE" in err:
            st.warning("**Rate limited.** You've hit the free tier limit. Wait a minute and retry.")
        elif "CONNECTION" in err:
            st.error("**No internet connection.** Check your network.")
        else:
            st.error(f"**API error:** `{err}`")

if not api_key:
    st.info("Add your RAPIDAPI_KEY to secrets.toml to enable the API test.")

st.divider()

# ── Fetch history ──────────────────────────────────────────────────────────────
st.markdown("#### Fetch History")
if os.path.exists(SCRAPE_LOG_PATH):
    log_df = pd.read_csv(SCRAPE_LOG_PATH)
    if not log_df.empty:
        log_df = log_df.sort_values("timestamp", ascending=False).head(15)

        # Colour-code the status column
        def style_status(val):
            if val == "success":    return "color:#00FF94"
            if val == "no_new_data": return "color:#FFB800"
            return "color:#FF4757"

        log_df.columns = [c.replace("_"," ").title() for c in log_df.columns]
        st.dataframe(log_df, use_container_width=True, hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", width="small"),
                "New Records": st.column_config.NumberColumn("New Records", format="%d"),
                "Total Records": st.column_config.NumberColumn("Total Records", format="%d"),
            })
    else:
        st.info("No fetch history yet.")
else:
    st.info("No fetch history yet. Run your first fetch above.")
