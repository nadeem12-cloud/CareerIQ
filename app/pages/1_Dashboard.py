import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.data_processing import preprocess_data

# =============================
# 📂 LOAD & PREPROCESS DATA
# =============================
df = load_data()
df = preprocess_data(df)

st.title("📊 CareerIQ – Market Dashboard")
st.markdown("Analyze hiring trends across Data, AI, ML & Cloud roles.")
st.divider()

# =============================
# 🖼️ SCREENSHOT MODE
# =============================
st.sidebar.markdown("### 🖼️ Screenshot Mode")
screenshot_mode = st.sidebar.checkbox("Enable compact view")

# =============================
# 🔎 FILTERS
# =============================
st.sidebar.header("Filters")

job_group_filter = st.sidebar.multiselect(
    "Job Role",
    sorted(df["job_group"].dropna().unique())
)

location_filter = st.sidebar.multiselect(
    "Location",
    sorted(df["clean_location"].dropna().unique())
)

filtered_df = df.copy()

if job_group_filter:
    filtered_df = filtered_df[filtered_df["job_group"].isin(job_group_filter)]

if location_filter:
    filtered_df = filtered_df[filtered_df["clean_location"].isin(location_filter)]

# =============================
# 📌 FILTER SUMMARY
# =============================
selected_roles = ", ".join(job_group_filter) if job_group_filter else "All Roles"
selected_locations = ", ".join(location_filter) if location_filter else "All Locations"

st.info(f"Showing results for **{selected_roles}** in **{selected_locations}**")

# =============================
# 📈 KPI SECTION
# =============================
k1, k2, k3 = st.columns(3)

k1.metric("📌 Total Jobs", len(filtered_df))
k2.metric("💼 Unique Roles", filtered_df["job_group"].nunique())
k3.metric("🌍 Active Locations", filtered_df["clean_location"].nunique())

st.divider()

# =============================
# 📊 MARKET STATUS
# =============================
market_ratio = len(filtered_df) / len(df) if len(df) > 0 else 0

if market_ratio > 0.4:
    market_status = "🟢 Strong Hiring Market"
elif market_ratio > 0.2:
    market_status = "🟡 Moderate Competition"
else:
    market_status = "🔴 Competitive / Niche Segment"

st.success(f"Market Status: {market_status}")

# =============================
# 📊 CHARTS
# =============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Job Demand by Role")
    role_counts = filtered_df["job_group"].value_counts().reset_index()
    role_counts.columns = ["Role", "Jobs"]

    fig1 = px.bar(role_counts, x="Role", y="Jobs", text="Jobs")
    fig1.update_layout(height=350 if screenshot_mode else 450)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Jobs by Location")
    loc_counts = (
        filtered_df["clean_location"]
        .value_counts()
        .head(6)
        .reset_index()
    )
    loc_counts.columns = ["Location", "Jobs"]

    fig2 = px.pie(loc_counts, names="Location", values="Jobs", hole=0.45)
    fig2.update_layout(height=350 if screenshot_mode else 450)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# =============================
# 🎓 EXPERIENCE DISTRIBUTION
# =============================
st.subheader("📊 Experience Demand Overview")

exp_order = ["0-1", "1-2", "2-5", "5-10", "10+"]

exp_counts = (
    filtered_df["experience"]
    .value_counts()
    .reindex(exp_order, fill_value=0)
    .reset_index()
)

exp_counts.columns = ["Experience", "Jobs"]

fig3 = px.bar(
    exp_counts,
    x="Jobs",
    y="Experience",
    orientation="h",
    text="Jobs"
)

fig3.update_layout(height=350 if screenshot_mode else 450)
st.plotly_chart(fig3, use_container_width=True)

# =============================
# 🎯 CAREER INSIGHT
# =============================
st.divider()
st.subheader("🎯 Career Insight")

if not filtered_df.empty:
    top_role = filtered_df["job_group"].value_counts().idxmax()
    top_city = filtered_df["clean_location"].value_counts().idxmax()
    top_exp = filtered_df["experience"].value_counts().idxmax()

    st.markdown(f"""
**Most In-Demand Role:** {top_role}  
**Top Hiring City:** {top_city}  
**Experience Sweet Spot:** {top_exp} years  

💡 Build strong projects aligned with this demand trend.
""")
else:
    st.warning("No data available for selected filters.")