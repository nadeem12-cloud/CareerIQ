import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9, ]', '', text)
    return text

def load_and_clean_data():
    df = pd.read_csv("Data/Raw/sample_jobs.csv")
    df["clean_description"] = df["description"].apply(clean_text)
    return df

if __name__ == "__main__":
    df = load_and_clean_data()
    print(df[["job_title", "clean_description"]].head())
