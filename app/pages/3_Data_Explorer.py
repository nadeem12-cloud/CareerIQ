import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
from utils.ui_components import inject_css, navbar, page_header

st.set_page_config(page_title="Data Explorer – CareerIQ", page_icon="📂", layout="wide", initial_sidebar_state="collapsed")
inject_css()
navbar("Explorer")

df = load_data()
df = preprocess_data(df)

page_header("📂", "Data Explorer", "Browse, filter and export structured job market data")

allowed = {"Job Title":"job_title","Role":"job_group","City":"clean_location",
           "Experience":"experience","Skills":"skills_extracted"}

# ── Filters in main area ───────────────────────────────────────────────────────
with st.expander("🔽  Filters & Columns", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    role_filter = fc1.multiselect("Role",
        sorted(df["job_group"].dropna().unique()), placeholder="All roles", key="ex_roles")
    loc_filter  = fc2.multiselect("City",
        sorted(df["clean_location"].dropna().unique()), placeholder="All cities", key="ex_locs")
    exp_filter  = fc3.multiselect("Experience",
        ["0-1","1-2","2-5","5-10","10+"], placeholder="All levels", key="ex_exp")
    sel_labels  = st.multiselect("Columns to show", list(allowed.keys()),
        default=["Job Title","Role","City","Experience"], key="ex_cols")

fdf = df.copy()
if role_filter: fdf = fdf[fdf["job_group"].isin(role_filter)]
if loc_filter:  fdf = fdf[fdf["clean_location"].isin(loc_filter)]
if exp_filter:  fdf = fdf[fdf["experience"].isin(exp_filter)]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Matching Records", f"{len(fdf):,}")
k2.metric("Unique Roles",     fdf["job_group"].nunique())
k3.metric("Cities",           fdf["clean_location"].nunique())
k4.metric("Filter Rate",      f"{len(fdf)/len(df):.0%}" if len(df) else "—")
st.divider()

sel_cols   = [allowed[l] for l in sel_labels] if sel_labels else list(allowed.values())
display_df = fdf[sel_cols].reset_index(drop=True)

st.markdown(
    f'<div class="page-subtitle">Showing <strong style="color:#00D4FF;">{min(200,len(display_df))}'
    f'</strong> of <strong style="color:#E2E8F0;">{len(display_df):,}</strong> records</div>',
    unsafe_allow_html=True)

st.dataframe(display_df.head(200), use_container_width=True, height=420, hide_index=True,
    column_config={
        "job_title":        st.column_config.TextColumn("Job Title",  width="large"),
        "job_group":        st.column_config.TextColumn("Role",       width="medium"),
        "clean_location":   st.column_config.TextColumn("City",       width="medium"),
        "experience":       st.column_config.TextColumn("Experience", width="small"),
        "skills_extracted": st.column_config.TextColumn("Skills",     width="large"),
    })

st.divider()
col_dl, col_info = st.columns([2, 3])
with col_dl:
    st.markdown("#### Export")
    st.download_button("⬇  Download as CSV",
        data=display_df.to_csv(index=False),
        file_name="careeriq_export.csv", mime="text/csv", use_container_width=True)
with col_info:
    st.markdown("#### Dataset Info")
    st.markdown(f"""<div class="insight-card">
      <div style="display:flex;gap:2rem;flex-wrap:wrap;">
        <div><div class="insight-card-label">Total</div>
             <div class="insight-card-value">{len(df):,}</div></div>
        <div><div class="insight-card-label">Filtered</div>
             <div class="insight-card-value">{len(fdf):,}</div></div>
        <div><div class="insight-card-label">Columns</div>
             <div class="insight-card-value">{len(sel_cols)}</div></div>
      </div></div>""", unsafe_allow_html=True)
