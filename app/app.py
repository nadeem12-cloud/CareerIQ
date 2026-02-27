import streamlit as st
import pandas as pd
import plotly.express as px
import os
from whatsapp_utils import send_whatsapp_message

# =============================
# 🔧 PAGE CONFIG
# =============================
st.set_page_config(
    page_title="CareerIQ – AI Based Career Advisory System",
    layout="wide"
)

# =============================
# 🖼️ SCREENSHOT MODE
# =============================
st.sidebar.markdown("### 🖼️ Screenshot Mode")
screenshot_mode = st.sidebar.checkbox("Enable compact view")

# =============================
# 📂 LOAD DATA
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Data", "Processed", "jobs_master.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, dtype=str)

df = load_data()

# =============================
# 🧹 CLEAN LOCATION
# =============================
def clean_location(loc):
    if pd.isna(loc):
        return None
    loc = loc.lower()
    if "pune" in loc:
        return "Pune"
    if "bangalore" in loc or "bengaluru" in loc:
        return "Bengaluru"
    if "mumbai" in loc:
        return "Mumbai"
    if "hyderabad" in loc:
        return "Hyderabad"
    if "chennai" in loc:
        return "Chennai"
    if "delhi" in loc or "ncr" in loc or "gurgaon" in loc:
        return "Delhi NCR"
    return loc.title()

df["clean_location"] = df["location"].apply(clean_location)

# =============================
# 🏷️ JOB GROUPING
# =============================
def map_job_group(title):
    title = str(title).lower()
    if "data scientist" in title:
        return "Data Scientist"
    if "data analyst" in title:
        return "Data Analyst"
    if "machine learning" in title or "ml engineer" in title:
        return "ML Engineer"
    if "ai engineer" in title:
        return "AI Engineer"
    if "data engineer" in title:
        return "Data Engineer"
    if "cloud" in title:
        return "Cloud Engineer"
    if "business analyst" in title:
        return "Business Analyst"
    if "software" in title or "developer" in title:
        return "Software Engineer"
    return "Other Roles"

df["job_group"] = df["job_title"].apply(map_job_group)

# =============================
# 🎓 CLEAN EXPERIENCE
# =============================
df["experience"] = df["experience"].astype(str).str.strip()
valid_exp = ["0-1", "1-2", "2-5", "5-10", "10+"]
df = df[df["experience"].isin(valid_exp)]

# =============================
# 📊 TITLE
# =============================
st.title("📊 CareerIQ – AI Based Career Advisory System")
st.markdown("Analyze hiring trends across Data, AI, ML & Cloud roles.")
st.divider()

# =============================
# 🔎 FILTERS
# =============================
st.sidebar.header("Filters")

job_group_filter = st.sidebar.multiselect(
    "Job Role",
    sorted(df["job_group"].unique())
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
# 📊 MARKET STRENGTH
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
    loc_counts = filtered_df["clean_location"].value_counts().head(6).reset_index()
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
# 🔧 SKILLS INSIGHT
# =============================
st.subheader("🔧 Top Skills in Demand")

if not filtered_df.empty and "skills_extracted" in filtered_df.columns:

    skills_series = (
        filtered_df["skills_extracted"]
        .dropna()
        .str.lower()
        .str.split(",")
        .explode()
        .str.strip()
    )

    skills_series = skills_series[skills_series != ""]

    top_skills = skills_series.value_counts().head(10).reset_index()
    top_skills.columns = ["Skill", "Demand"]
    top_skills["Skill"] = top_skills["Skill"].str.title()

    fig_skills = px.bar(
        top_skills,
        x="Demand",
        y="Skill",
        orientation="h",
        text="Demand"
    )

    fig_skills.update_layout(height=400 if screenshot_mode else 500)
    st.plotly_chart(fig_skills, use_container_width=True)

    if job_group_filter:
        role_df = filtered_df[filtered_df["job_group"] == job_group_filter[0]]
        role_skills = (
            role_df["skills_extracted"]
            .dropna()
            .str.lower()
            .str.split(",")
            .explode()
            .str.strip()
        )

        role_top = role_skills.value_counts().head(3).index.tolist()

        if role_top:
            st.info(f"For **{job_group_filter[0]}**, focus on: {', '.join(role_top).title()}")

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

# =============================
# 📂 DATA ACCESS
# =============================
st.divider()
st.subheader("📂 Data Access")

col_preview, col_download = st.columns([2, 1])

with col_preview:
    with st.expander("🔍 Preview Filtered Job Listings"):
        preview_df = filtered_df[
            ["job_title", "job_group", "clean_location", "experience"]
        ].rename(columns={"clean_location": "location"})

        st.caption("Showing first 100 rows")
        st.dataframe(preview_df.head(100), use_container_width=True, height=250)

with col_download:
    st.download_button(
        "⬇ Download Full Filtered Data",
        filtered_df.to_csv(index=False),
        file_name="careerIQ_filtered_jobs.csv"
    )

# =============================
# 📲 WHATSAPP INSIGHT
# =============================
st.divider()
st.markdown("Whatsapp Automation is Currently not avaliable as the app is still in Prototyping Phase")

st.subheader("📲 Share Insight")

if st.button("Send Insight to WhatsApp"):
    if not filtered_df.empty:

        top_roles = filtered_df["job_group"].value_counts().head(2)
        top_cities = filtered_df["clean_location"].value_counts().head(2)

        exp_dist = filtered_df["experience"].value_counts(normalize=True) * 100
        top_exp = exp_dist.idxmax()
        top_exp_pct = round(exp_dist.max())

        role_text = "\n".join(
            [f"{i+1}. {role} – {count} jobs"
             for i, (role, count) in enumerate(top_roles.items())]
        )

        city_text = "\n".join(
            [f"{i+1}. {city} – {count} openings"
             for i, (city, count) in enumerate(top_cities.items())]
        )

        message = f"""
📊 CareerIQ – Market Intelligence

🔹 Total Jobs Analyzed: {len(filtered_df)}

🔥 Top Hiring Roles:
{role_text}

🌍 Top Hiring Cities:
{city_text}

🎯 Experience Sweet Spot:
{top_exp} years ({top_exp_pct}% of roles)

💡 Action Tip:
Target {top_roles.index[0]} roles in {top_cities.index[0]} 
if you fall in the {top_exp} experience range.

Stay skilled. Stay relevant.
"""

        send_whatsapp_message(message)
        st.success("✅ Insight sent successfully!")
