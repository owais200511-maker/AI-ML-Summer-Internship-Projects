import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import urllib.request

st.set_page_config(
    page_title="Airbnb NYC Outlier Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3 { font-family: 'Outfit', sans-serif; }
.stat-card {
    background: linear-gradient(135deg,#1e3a5f,#0d2137);
    border-radius:12px; padding:18px 22px;
    border-left: 4px solid #4fc3f7;
    color:white; margin-bottom:6px;
}
.stat-card h3 { margin:0; color:#4fc3f7; font-size:1.6rem; }
.stat-card p  { margin:4px 0 0; color:#90caf9; font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0d2137 0%,#1a3a5c 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.35);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">📊 Airbnb NYC Outlier Detection</h1>
    <p style="color:#90caf9;margin:8px 0 0;font-size:1rem;">
        Remove statistical outliers using percentile clipping • Airbnb NYC 2019 Dataset
    </p>
</div>
""", unsafe_allow_html=True)

DATA_URL = ("https://raw.githubusercontent.com/Danishkhan757/"
            "ARTIFICAL-INTELLIGENCE-SUMMER-INTERSHIP/main/"
            "Project-02-%20Outliers%20percentile/AB_NYC_2019.csv")
LOCAL_CSV = "AB_NYC_2019.csv"

@st.cache_data(show_spinner=False)
def load_data():
    if not os.path.exists(LOCAL_CSV):
        with st.spinner("📥 Downloading Airbnb dataset…"):
            urllib.request.urlretrieve(DATA_URL, LOCAL_CSV)
    return pd.read_csv(LOCAL_CSV)

with st.spinner("Loading dataset…"):
    df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Outlier Settings")
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
column = st.sidebar.selectbox("Select Column", num_cols,
                               index=num_cols.index("price") if "price" in num_cols else 0)

lower_pct = st.sidebar.slider("Lower Percentile (%)", 0.0, 10.0, 1.0, 0.5)
upper_pct = st.sidebar.slider("Upper Percentile (%)", 90.0, 100.0, 99.0, 0.5)
show_room_type = st.sidebar.checkbox("Break down by Room Type", value=True)

lower_limit = df[column].quantile(lower_pct / 100)
upper_limit = df[column].quantile(upper_pct / 100)

df_clean = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
removed = len(df) - len(df_clean)

# ── KPI Cards ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="stat-card"><h3>{len(df):,}</h3><p>Original Records</p></div>""",
                unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-card"><h3>{len(df_clean):,}</h3><p>After Outlier Removal</p></div>""",
                unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="stat-card"><h3>{removed:,}</h3><p>Outliers Removed</p></div>""",
                unsafe_allow_html=True)
with c4:
    pct = removed / len(df) * 100
    st.markdown(f"""<div class="stat-card"><h3>{pct:.1f}%</h3><p>Data Removed</p></div>""",
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Percentile bounds info ───────────────────────────────────────────────────
st.info(f"📌 **{column}** — Lower bound: **{lower_limit:,.2f}** (P{lower_pct:.0f}) | "
        f"Upper bound: **{upper_limit:,.2f}** (P{upper_pct:.0f})")

# ── Distribution Charts ──────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Before Outlier Removal")
    fig_before = px.histogram(df, x=column, nbins=60,
                              color_discrete_sequence=["#ef5350"],
                              template="plotly_dark",
                              title=f"Distribution of {column}")
    fig_before.add_vline(x=lower_limit, line_dash="dash", line_color="#ffeb3b",
                         annotation_text=f"P{lower_pct:.0f}")
    fig_before.add_vline(x=upper_limit, line_dash="dash", line_color="#ffeb3b",
                         annotation_text=f"P{upper_pct:.0f}")
    fig_before.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                             height=380)
    st.plotly_chart(fig_before, use_container_width=True)

with col_b:
    st.subheader("After Outlier Removal")
    fig_after = px.histogram(df_clean, x=column, nbins=60,
                             color_discrete_sequence=["#4caf50"],
                             template="plotly_dark",
                             title=f"Cleaned Distribution of {column}")
    fig_after.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            height=380)
    st.plotly_chart(fig_after, use_container_width=True)

# ── Box plots comparison ──────────────────────────────────────────────────────
st.subheader("📦 Box Plot Comparison")
fig_box = go.Figure()
fig_box.add_trace(go.Box(y=df[column].dropna(), name="Original",
                          marker_color="#ef5350", boxmean=True))
fig_box.add_trace(go.Box(y=df_clean[column].dropna(), name="Cleaned",
                          marker_color="#4caf50", boxmean=True))
fig_box.update_layout(template="plotly_dark", height=380,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_box, use_container_width=True)

# ── Room Type Breakdown ───────────────────────────────────────────────────────
if show_room_type and "room_type" in df_clean.columns:
    st.subheader("🏠 Price by Room Type (After Cleaning)")
    fig_rt = px.box(df_clean, x="room_type", y=column,
                    color="room_type", template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Set2)
    fig_rt.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         height=400, showlegend=False)
    st.plotly_chart(fig_rt, use_container_width=True)

# ── Stats Table ───────────────────────────────────────────────────────────────
st.subheader("📈 Descriptive Statistics Comparison")
stat_df = pd.DataFrame({
    "Metric": ["Mean","Median","Std Dev","Min","Max","Skewness"],
    "Before Cleaning": [
        df[column].mean(), df[column].median(), df[column].std(),
        df[column].min(),  df[column].max(), df[column].skew()
    ],
    "After Cleaning": [
        df_clean[column].mean(), df_clean[column].median(), df_clean[column].std(),
        df_clean[column].min(),  df_clean[column].max(), df_clean[column].skew()
    ],
}).set_index("Metric")
st.dataframe(stat_df.style.format("{:.2f}"), use_container_width=True)

with st.expander("🗃️ Cleaned Data Preview"):
    st.dataframe(df_clean.head(100), use_container_width=True)

st.caption("Data: Airbnb NYC 2019 • Project 02 — AI/ML Summer Internship")
