import pandas as pd
import os

# -----------------------------
# Paths
# -----------------------------
RAW_DATA_PATH = "Data/Raw"
PROCESSED_DATA_PATH = "Data/Processed"

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

output_path = os.path.join(PROCESSED_DATA_PATH, "jobs_master.csv")

dfs = []

# =============================
# 1. NAUKRI DATASET
# Columns:
# ['Job_Role', 'Company', 'Location', 'Job Experience', 'Skills/Description']
# =============================
naukri_path = os.path.join(RAW_DATA_PATH, "naukri_data_science_jobs_india.csv")

if os.path.exists(naukri_path):
    naukri_df = pd.read_csv(naukri_path)

    naukri_clean = pd.DataFrame({
        "job_title": naukri_df["Job_Role"],
        "job_description": naukri_df["Skills/Description"],
        "skills_extracted": naukri_df["Skills/Description"],
        "location": naukri_df["Location"],
        "experience": naukri_df["Job Experience"],
        "role_category": "Data Science",
        "source_dataset": "Naukri"
    })

    dfs.append(naukri_clean)

# =============================
# 2. DATA SCIENCE SALARY DATASET
# Columns:
# ['job_title', 'job_category', 'experience_level', 'company_location', ...]
# =============================
ds_path = os.path.join(RAW_DATA_PATH, "data_science_job.csv")

if os.path.exists(ds_path):
    ds_df = pd.read_csv(ds_path)

    ds_clean = pd.DataFrame({
        "job_title": ds_df["job_title"],
        # CREATE description manually (IMPORTANT)
        "job_description": ds_df["job_title"] + " | " + ds_df["job_category"],
        "skills_extracted": ds_df["job_category"],
        "location": ds_df["company_location"],
        "experience": ds_df["experience_level"],
        "role_category": ds_df["job_category"],
        "source_dataset": "DS_Salary_Dataset"
    })

    dfs.append(ds_clean)

# -----------------------------
# Merge & Save
# -----------------------------
if len(dfs) == 0:
    raise Exception("❌ No datasets found in Data/Raw")

final_df = pd.concat(dfs, ignore_index=True)
final_df.fillna("", inplace=True)
final_df.drop_duplicates(inplace=True)

final_df.to_csv(output_path, index=False)

print("✅ preprocess.py ran successfully")
print("📄 File created:", output_path)
print("📊 Total rows:", len(final_df))
