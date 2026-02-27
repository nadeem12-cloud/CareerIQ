import streamlit as st
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
from whatsapp_utils import send_whatsapp_message
# Optional import (safe handling)
try:
    from app.whatsapp_utils import send_whatsapp_message
    WHATSAPP_AVAILABLE = True
except Exception:
    WHATSAPP_AVAILABLE = False

# =============================
# LOAD DATA
# =============================
df = load_data()
df = preprocess_data(df)

st.title("📲 CareerIQ – WhatsApp Market Insight")
st.markdown("Generate and share real-time hiring intelligence.")
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
# GENERATE INSIGHT
# =============================
st.subheader("📊 Insight Preview")

if filtered_df.empty:
    st.warning("No data available for selected filters.")
else:

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

    st.code(message)

# =============================
# SEND BUTTON
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
