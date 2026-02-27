import streamlit as st

st.title("ℹ️ About CareerIQ")
st.divider()

# =============================
# PROJECT OVERVIEW
# =============================
st.header("📌 Project Overview")

st.markdown("""
**CareerIQ** is a data-driven job market intelligence system designed to analyze hiring trends 
across Data Science, AI, ML, and Cloud domains.

The platform transforms raw job listing data into structured insights that help:
- Students understand hiring demand
- Professionals identify skill gaps
- Recruiters observe market trends

It bridges the gap between raw job data and actionable career intelligence.
""")

# =============================
# PROBLEM STATEMENT
# =============================
st.header("🎯 Problem Statement")

st.markdown("""
Job seekers often rely on scattered job portals to understand market demand.  
However, raw listings do not provide structured insight into:

- Most in-demand roles
- Skill frequency trends
- Experience-level distribution
- Location-based hiring intensity

CareerIQ solves this by converting raw job listings into analytical insights.
""")

# =============================
# SYSTEM ARCHITECTURE
# =============================
st.header("🏗 System Architecture")

st.markdown("""
The system follows a modular architecture:

1. **Data Layer**
   - Raw job datasets (Naukri, LinkedIn, etc.)
   - Preprocessing & cleaning pipeline

2. **Processing Layer**
   - Skill extraction
   - Role categorization
   - Location normalization

3. **Analytics Layer**
   - Dashboard insights
   - Skill demand intelligence
   - Experience distribution analysis

4. **Communication Layer**
   - WhatsApp insight automation (Demo / API-enabled)

This separation ensures scalability and maintainability.
""")

# =============================
# TECHNOLOGY STACK
# =============================
st.header("⚙ Technology Stack")

st.markdown("""
- **Python**
- **Pandas** (Data processing)
- **Plotly** (Interactive visualizations)
- **Streamlit** (Web application framework)
- **Twilio API** (WhatsApp automation – demo integration)
""")

# =============================
# KEY FEATURES
# =============================
st.header("🚀 Key Features")

st.markdown("""
- 📊 Real-time hiring trend visualization  
- 🔧 Skill demand intelligence  
- 📂 Interactive data exploration  
- 📲 Automated market insight messaging  
- 🧩 Modular multi-page architecture  
""")

# =============================
# FUTURE SCOPE
# =============================
st.header("🔮 Future Scope")

st.markdown("""
- Live web scraping integration  
- User authentication & personalized dashboards  
- Resume-skill gap analysis  
- AI-powered job recommendation engine  
- Deployment as scalable SaaS platform  
""")

# =============================
# DEVELOPER NOTE
# =============================
st.header("👨‍💻 Developer Note")

st.markdown("""
CareerIQ was developed as an academic project to demonstrate 
data engineering, analytics, and system design principles.

The focus was on:
- Clean modular coding structure
- Real-world API integration
- Scalable architecture design
- Insight-driven analytics

This project reflects an industry-oriented approach to data systems.
""")

st.divider()
st.caption("© 2026 CareerIQ – Job Market Intelligence System")