import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = Path("Data/Processed/jobs_master.csv")
OUTPUT_DIR = Path("EDA/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

print("✅ Dataset Loaded")
print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

# -----------------------------
# Basic Info
# -----------------------------
print("\n🔹 Data Info")
print(df.info())

print("\n🔹 Missing Values (%)")
print((df.isnull().mean() * 100).sort_values(ascending=False))

# -----------------------------
# 1️⃣ Job Role Distribution
# -----------------------------
if "job_title" in df.columns:
    plt.figure(figsize=(10, 5))
    df["job_title"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 Job Roles")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_job_roles.png")
    plt.close()

# -----------------------------
# 2️⃣ Location Distribution
# -----------------------------
if "location" in df.columns:
    plt.figure(figsize=(10, 5))
    df["location"].value_counts().head(10).plot(kind="bar", color="orange")
    plt.title("Top Job Locations")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_locations.png")
    plt.close()

# -----------------------------
# 3️⃣ Experience Level
# -----------------------------
if "experience" in df.columns:
    plt.figure(figsize=(8, 4))
    df["experience"].value_counts().plot(kind="bar", color="green")
    plt.title("Experience Distribution")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "experience_distribution.png")
    plt.close()

# -----------------------------
# 4️⃣ Salary Distribution (if present)
# -----------------------------
if "salary" in df.columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df["salary"].dropna(), bins=30, kde=True)
    plt.title("Salary Distribution")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "salary_distribution.png")
    plt.close()

# -----------------------------
# 5️⃣ Source Dataset Split
# -----------------------------
if "source_dataset" in df.columns:
    plt.figure(figsize=(6, 6))
    df["source_dataset"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Data Source Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "source_split.png")
    plt.close()

print("\n✅ EDA Completed")
print(f"📂 Plots saved in: {OUTPUT_DIR}")
