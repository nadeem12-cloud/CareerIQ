from collections import Counter
from preprocessing import load_and_clean_data
import pandas as pd

SKILLS = [
    "python", "machine learning", "sql", "aws",
    "deep learning", "nlp", "docker", "kubernetes"
]

def generate_skill_counts():
    df = load_and_clean_data()
    counter = Counter()

    for desc in df["clean_description"]:
        for skill in SKILLS:
            if skill in desc:
                counter[skill] += 1

    output_df = pd.DataFrame(counter.items(), columns=["Skill", "Count"])
    return output_df

if __name__ == "__main__":
    output = generate_skill_counts()
    output.to_csv("Data/Processed/skills_output.csv", index=False)
    print(output)
