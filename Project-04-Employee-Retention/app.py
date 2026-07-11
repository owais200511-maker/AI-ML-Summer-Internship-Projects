import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import urllib.request

st.set_page_config(
    page_title="Employee Retention Analysis",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3 { font-family: 'Outfit', sans-serif; }
.kpi-card {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    border-radius:14px; padding:22px 18px; text-align:center;
    border-top: 3px solid; color:white;
    box-shadow:0 6px 20px rgba(0,0,0,0.25);
}
.kpi-card h2 { margin:0; font-size:2rem; }
.kpi-card p  { margin:5px 0 0; font-size:0.85rem; color:#b2dfdb; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0f2027 0%,#203a43 50%,#2c5364 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">👥 Employee Retention Analysis</h1>
    <p style="color:#80cbc4;margin:8px 0 0;font-size:1rem;">
        Understand why employees leave and what drives retention
    </p>
</div>
""", unsafe_allow_html=True)

DATA_URL = ("https://raw.githubusercontent.com/Danishkhan757/"
            "ARTIFICAL-INTELLIGENCE-SUMMER-INTERSHIP/main/"
            "Project-04-%20Employee_Retention_Analysis/HR_comma_sep%20(2).csv")
LOCAL_CSV = "HR_comma_sep.csv"

@st.cache_data(show_spinner=False)
def load_data():
    if not os.path.exists(LOCAL_CSV):
        with st.spinner("📥 Downloading HR dataset…"):
            urllib.request.urlretrieve(DATA_URL, LOCAL_CSV)
    df = pd.read_csv(LOCAL_CSV)
    return df

with st.spinner("Loading HR data…"):
    df = load_data()

# ── Rename columns for clarity ────────────────────────────────────────────────
rename_map = {
    "satisfaction_level": "Satisfaction",
    "last_evaluation": "Last Evaluation",
    "number_project": "Projects",
    "average_montly_hours": "Monthly Hours",
    "time_spend_company": "Tenure (yrs)",
    "Work_accident": "Work Accident",
    "left": "Left",
    "promotion_last_5years": "Promoted",
    "Department": "Department",
    "salary": "Salary"
}
df = df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns})

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("🎛️ Filters")
depts = sorted(df["Department"].dropna().unique()) if "Department" in df.columns else []
sel_dept = st.sidebar.multiselect("Department", depts, default=depts)
if "Salary" in df.columns:
    salaries = df["Salary"].unique().tolist()
    sel_sal = st.sidebar.multiselect("Salary Level", salaries, default=salaries)
else:
    sel_sal = []

mask = pd.Series([True]*len(df))
if sel_dept and "Department" in df.columns:
    mask = mask & df["Department"].isin(sel_dept)
if sel_sal and "Salary" in df.columns:
    mask = mask & df["Salary"].isin(sel_sal)

fdf = df[mask]

# ── KPIs ──────────────────────────────────────────────────────────────────────
total = len(fdf)
left_count = fdf["Left"].sum() if "Left" in fdf.columns else 0
stayed = total - left_count
attrition_rate = left_count / total * 100 if total else 0

c1,c2,c3,c4 = st.columns(4)
kpis = [
    ("Total Employees", f"{total:,}", "#26a69a"),
    ("Stayed", f"{stayed:,}", "#66bb6a"),
    ("Left", f"{left_count:,}", "#ef5350"),
    ("Attrition Rate", f"{attrition_rate:.1f}%", "#ffa726"),
]
for col, (label, val, color) in zip([c1,c2,c3,c4], kpis):
    col.markdown(f"""
    <div class="kpi-card" style="border-color:{color};">
        <h2 style="color:{color};">{val}</h2>
        <p>{label}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
r1a, r1b = st.columns(2)

with r1a:
    st.subheader("📊 Attrition by Department")
    if "Department" in fdf.columns and "Left" in fdf.columns:
        dept_att = fdf.groupby("Department")["Left"].mean().mul(100).reset_index()
        dept_att.columns = ["Department","Attrition %"]
        fig = px.bar(dept_att.sort_values("Attrition %", ascending=True),
                     x="Attrition %", y="Department", orientation="h",
                     color="Attrition %", color_continuous_scale="RdYlGn_r",
                     template="plotly_dark")
        fig.update_layout(height=400, showlegend=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

with r1b:
    st.subheader("💰 Attrition by Salary Level")
    if "Salary" in fdf.columns and "Left" in fdf.columns:
        order_map = {"low":0,"medium":1,"high":2}
        sal_att = fdf.groupby("Salary")["Left"].mean().mul(100).reset_index()
        sal_att.columns = ["Salary","Attrition %"]
        sal_att["order"] = sal_att["Salary"].map(order_map)
        sal_att = sal_att.sort_values("order")
        fig2 = px.bar(sal_att, x="Salary", y="Attrition %",
                      color="Attrition %", color_continuous_scale="RdYlGn_r",
                      template="plotly_dark",
                      text="Attrition %")
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig2.update_layout(height=400, showlegend=False,
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
r2a, r2b = st.columns(2)

with r2a:
    st.subheader("😊 Satisfaction vs Evaluation")
    if "Satisfaction" in fdf.columns and "Last Evaluation" in fdf.columns and "Left" in fdf.columns:
        sample = fdf.sample(min(1000, len(fdf)), random_state=42)
        fig3 = px.scatter(sample, x="Satisfaction", y="Last Evaluation",
                          color=sample["Left"].map({0:"Stayed",1:"Left"}),
                          color_discrete_map={"Stayed":"#4caf50","Left":"#ef5350"},
                          template="plotly_dark", opacity=0.6)
        fig3.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

with r2b:
    st.subheader("⏰ Avg Monthly Hours by Status")
    if "Monthly Hours" in fdf.columns and "Left" in fdf.columns:
        fig4 = px.histogram(fdf, x="Monthly Hours",
                            color=fdf["Left"].map({0:"Stayed",1:"Left"}),
                            barmode="overlay", opacity=0.75,
                            color_discrete_map={"Stayed":"#42a5f5","Left":"#ef5350"},
                            template="plotly_dark", nbins=40)
        fig4.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)

# ── Tenure Analysis ────────────────────────────────────────────────────────────
if "Tenure (yrs)" in fdf.columns and "Left" in fdf.columns:
    st.subheader("📅 Attrition by Tenure")
    ten_att = fdf.groupby("Tenure (yrs)")["Left"].mean().mul(100).reset_index()
    ten_att.columns = ["Tenure (years)","Attrition %"]
    fig5 = px.line(ten_att, x="Tenure (years)", y="Attrition %",
                   markers=True, template="plotly_dark",
                   color_discrete_sequence=["#ff7043"])
    fig5.update_traces(line_width=3, marker_size=8)
    fig5.update_layout(height=350, plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig5, use_container_width=True)

with st.expander("🗃️ Raw Data Preview"):
    st.dataframe(fdf.head(200), use_container_width=True)

st.caption("Data: HR Dataset • Project 04 — Employee Retention Analysis • AI/ML Summer Internship")
