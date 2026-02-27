import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
import datetime

st.set_page_config(
    page_title="CareerIQ – AI Based Career Advisory System",
    layout="wide"
)

st.title("🚀 CareerIQ – AI Based Career Advisory System")
st.markdown("Modular AI Career Intelligence Platform")

df = load_data()
df = preprocess_data(df)

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df))
col2.metric("Unique Roles", df["job_group"].nunique())
col3.metric("Locations Covered", df["clean_location"].nunique())

st.divider()

st.caption(f"Data Last Updated: February 2026")
st.caption("Architecture: Modular | Scalable | Deployment Ready")

st.markdown("""


Use the sidebar to navigate:

📊 Dashboard  
🔧 Skills Insights  
📂 Data Explorer  
📲 WhatsApp Insights  
ℹ️ About  
""")