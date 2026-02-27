import pandas as pd
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "Data", "Processed", "jobs_master.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, dtype=str)