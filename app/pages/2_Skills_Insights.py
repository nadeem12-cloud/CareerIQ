import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plotly.express as px
from utils.data_loader import load_data
from utils.data_processing import preprocess_data
from utils.ui_components import inject_css, navbar, page_header, plotly_theme

st.set_page_config(page_title="Skills – CareerIQ", page_icon="🔧", layout="wide", initial_sidebar_state="collapsed")
inject_css()
navbar("Skills")

df = load_data()
df = preprocess_data(df)

page_header("🔧", "Skills Intelligence", "Discover the most in-demand skills by role")

# ── Filters in main area ───────────────────────────────────────────────────────
with st.expander("🔽  Filters", expanded=False):
    fc1, fc2 = st.columns([3, 1])
    role_filter = fc1.selectbox("Select Role",
        ["All Roles"] + sorted(df["job_group"].dropna().unique()), key="sk_role")
    top_n = fc2.slider("Top N skills", 5, 20, 10, key="sk_topn")

fdf = df.copy()
if role_filter != "All Roles":
    fdf = fdf[fdf["job_group"] == role_filter]

has_skills = "skills_extracted" in fdf.columns
if has_skills:
    skills_series = (
        fdf["skills_extracted"].dropna()
        .str.lower().str.split(",").explode().str.strip()
    )
    skills_series = skills_series[skills_series != ""]
    top_skills = skills_series.value_counts().head(top_n).reset_index()
    top_skills.columns = ["Skill","Count"]
    top_skills["Skill"] = top_skills["Skill"].str.title()
else:
    top_skills = None

total_roles       = df["job_group"].nunique()
roles_with_skills = df[df["skills_extracted"].notna()]["job_group"].nunique() if has_skills else 0

k1, k2, k3 = st.columns(3)
k1.metric("Jobs Analysed",         f"{len(fdf):,}")
k2.metric("Roles with Skill Data", f"{roles_with_skills} / {total_roles}")
k3.metric("Unique Skills Found",
    f"{skills_series.nunique():,}" if has_skills and top_skills is not None else "—")

st.divider()

if has_skills and top_skills is not None and not top_skills.empty:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"#### Top {top_n} Skills — {role_filter}")
        fig = px.bar(top_skills.sort_values("Count"), x="Count", y="Skill",
            orientation="h", text="Count", color="Count",
            color_continuous_scale=[[0,"#0D2040"],[0.5,"#005580"],[1,"#00D4FF"]])
        fig.update_layout(**plotly_theme(), coloraxis_showscale=False, height=max(320, top_n*36))
        fig.update_traces(textposition="outside", textfont_color="#94A3B8", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Skill Share")
        fig2 = px.pie(top_skills.head(8), names="Skill", values="Count", hole=0.5,
            color_discrete_sequence=["#00D4FF","#00FF94","#FFB800","#FF6B9D",
                                      "#A78BFA","#FB923C","#34D399","#60A5FA"])
        fig2.update_layout(**plotly_theme(), height=max(320, top_n*36))
        fig2.update_traces(textfont_color="#E2E8F0", textinfo="percent")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown("#### Career Recommendation")
    top3 = top_skills.head(3)["Skill"].tolist()
    focus = role_filter if role_filter != "All Roles" else "All Roles"
    detail = (f'Most frequent in <strong style="color:#E2E8F0;">{focus}</strong> listings. '
               'Mastering these maximises your application match rate.'
              if role_filter != "All Roles" else
              'Select a specific role above for targeted recommendations.')
    st.markdown(f"""<div class="insight-card">
        <div class="insight-card-label">Focus Skills for {focus}</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
          {"".join(f'<span class="stat-pill">{s}</span>' for s in top3)}
        </div>
        <div style="font-family:'DM Sans',sans-serif;font-size:0.85rem;
                    color:#94A3B8;margin-top:10px;line-height:1.6;">{detail}</div>
    </div>""", unsafe_allow_html=True)
else:
    st.warning("No skill data available for the selected filter.")
