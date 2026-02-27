import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.data_processing import preprocess_data

# =============================
# 📂 LOAD DATA
# =============================
df = load_data()
df = preprocess_data(df)

st.title("🔧 Skills Demand Intelligence")
st.markdown("Analyze most in-demand skills across roles.")
st.divider()

# =============================
# 🎯 ROLE FILTER
# =============================
st.sidebar.header("Filter by Role")

role_filter = st.sidebar.selectbox(
    "Select Role (Optional)",
    ["All Roles"] + sorted(df["job_group"].dropna().unique())
)

filtered_df = df.copy()

if role_filter != "All Roles":
    filtered_df = filtered_df[filtered_df["job_group"] == role_filter]

# =============================
# 📊 TOP SKILLS
# =============================
st.subheader("📈 Top 10 Skills in Demand")

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

    fig = px.bar(
        top_skills,
        x="Demand",
        y="Skill",
        orientation="h",
        text="Demand"
    )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No skill data available for selected filter.")

# =============================
# 🎓 ROLE SPECIFIC ADVICE
# =============================
st.divider()
st.subheader("🎯 Career Recommendation")

if role_filter != "All Roles" and not filtered_df.empty:

    role_skills = (
        filtered_df["skills_extracted"]
        .dropna()
        .str.lower()
        .str.split(",")
        .explode()
        .str.strip()
    )

    top_3 = role_skills.value_counts().head(3).index.tolist()

    if top_3:
        st.success(
            f"For **{role_filter}**, focus on mastering: "
            f"{', '.join(top_3).title()}"
        )
    else:
        st.info("Not enough skill data for recommendation.")

else:
    st.info("Select a specific role to get targeted skill advice.")

# =============================
# 📌 SKILL COVERAGE METRIC
# =============================
st.divider()

total_roles = df["job_group"].nunique()
roles_with_skills = df[df["skills_extracted"].notna()]["job_group"].nunique()

st.metric("Roles with Skill Mapping", f"{roles_with_skills} / {total_roles}")