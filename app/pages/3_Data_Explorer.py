import streamlit as st
from utils.data_loader import load_data
from utils.data_processing import preprocess_data

# =============================
# LOAD DATA
# =============================
df = load_data()
df = preprocess_data(df)

st.title("📂 CareerIQ – Data Explorer")
st.markdown("Explore structured job market intelligence data.")
st.divider()

# =============================
# SIDEBAR FILTERS
# =============================
st.sidebar.header("Filters")

role_filter = st.sidebar.multiselect(
    "Filter by Role",
    sorted(df["job_group"].dropna().unique())
)

location_filter = st.sidebar.multiselect(
    "Filter by Location",
    sorted(df["clean_location"].dropna().unique())
)

filtered_df = df.copy()

if role_filter:
    filtered_df = filtered_df[filtered_df["job_group"].isin(role_filter)]

if location_filter:
    filtered_df = filtered_df[filtered_df["clean_location"].isin(location_filter)]

# =============================
# DATA SUMMARY
# =============================
st.subheader("📊 Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Unique Roles", filtered_df["job_group"].nunique())
col3.metric("Unique Locations", filtered_df["clean_location"].nunique())

st.divider()

# =============================
# ONLY SHOW CLEAN USER COLUMNS
# =============================
st.subheader("📑 Select Columns to Display")

# 🔒 Hard-restricted visible columns
allowed_columns = {
    "Job Title": "job_title",
    "Role Category": "job_group",
    "Location": "clean_location",
    "Experience": "experience",
    "Skills": "skills_extracted"
}

selected_labels = st.multiselect(
    "Choose columns",
    list(allowed_columns.keys()),
    default=["Job Title", "Role Category", "Location", "Experience"]
)

# Map back to actual dataframe columns
selected_columns = [allowed_columns[label] for label in selected_labels]

if not selected_columns:
    selected_columns = [
        "job_title",
        "job_group",
        "clean_location",
        "experience"
    ]

display_df = filtered_df[selected_columns]

# =============================
# PREVIEW
# =============================
with st.expander("🔍 Preview Data"):
    st.caption("Showing first 100 rows")
    st.dataframe(display_df.head(100), use_container_width=True, height=350)

# =============================
# DOWNLOAD
# =============================
st.divider()
st.subheader("⬇ Download Data")

csv_data = display_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="careerIQ_filtered_data.csv",
    mime="text/csv"
)

# =============================
# DATA INFO
# =============================
st.divider()

st.subheader("📌 Dataset Info")

st.markdown(f"""
- Original Dataset Size: **{len(df)} records**
- Filtered Dataset Size: **{len(filtered_df)} records**
- Available Analytical Fields: **{len(allowed_columns)}**
""")