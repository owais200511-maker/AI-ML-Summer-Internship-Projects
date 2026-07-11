import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import urllib.request

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Google Play Store Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }
.metric-box {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #0f3460;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-box h2 { color: #e94560; font-size: 2rem; margin: 0; }
.metric-box p  { color: #a8b2d8; font-size: 0.9rem; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0f3460 0%,#16213e 50%,#1a1a2e 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);">
    <h1 style="color:white;margin:0;font-size:2.4rem;letter-spacing:-0.5px;">
        📱 Google Play Store Dashboard
    </h1>
    <p style="color:#a8b2d8;margin:8px 0 0;font-size:1.05rem;">
        Interactive data visualization of Android app market trends
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Data Loading ────────────────────────────────────────────────────────────
DATA_URL = ("https://raw.githubusercontent.com/Danishkhan757/"
            "ARTIFICAL-INTELLIGENCE-SUMMER-INTERSHIP/main/"
            "Project-%2001-%20Data%20visualization/googleplaystore_v2.csv")
LOCAL_CSV = "googleplaystore_v2.csv"

@st.cache_data(show_spinner=False)
def load_data():
    if not os.path.exists(LOCAL_CSV):
        with st.spinner("📥 Downloading dataset…"):
            urllib.request.urlretrieve(DATA_URL, LOCAL_CSV)
    df = pd.read_csv(LOCAL_CSV)
    df = df.dropna(subset=["Rating"])
    for col, fn in [
        ("Price",    lambda s: pd.to_numeric(s.str.replace("$","",regex=False), errors="coerce")),
        ("Reviews",  lambda s: pd.to_numeric(s, errors="coerce")),
        ("Installs", lambda s: pd.to_numeric(
            s.str.replace(",","",regex=False).str.replace("+","",regex=False),
            errors="coerce")),
        ("Size",     lambda s: pd.to_numeric(
            s.str.replace("M","",regex=False).str.replace("k","",regex=False),
            errors="coerce")),
    ]:
        if col in df.columns:
            df[col] = fn(df[col].astype(str))
    return df

with st.spinner("Loading data…"):
    df = load_data()

# ─── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.header("🎛️ Filters")
categories = sorted(df["Category"].dropna().unique()) if "Category" in df.columns else []
sel_cats = st.sidebar.multiselect("Category", categories, default=categories[:5])
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.5, 0.1)
content_types = df["Type"].dropna().unique().tolist() if "Type" in df.columns else []
sel_type = st.sidebar.multiselect("App Type", content_types, default=content_types)

mask = (
    df["Category"].isin(sel_cats) &
    (df["Rating"] >= min_rating) &
    df["Type"].isin(sel_type)
) if sel_cats and sel_type else pd.Series([True]*len(df))

filtered = df[mask]

# ─── KPI Cards ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("Total Apps", f"{len(filtered):,}"),
    ("Avg Rating",  f"{filtered['Rating'].mean():.2f} ⭐"),
    ("Total Reviews", f"{filtered['Reviews'].sum()/1e6:.1f}M"),
    ("Categories",  f"{filtered['Category'].nunique()}"),
]
for col, (label, val) in zip([c1,c2,c3,c4], kpis):
    col.markdown(f"""
    <div class="metric-box">
        <h2>{val}</h2>
        <p>{label}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Charts ──────────────────────────────────────────────────────────────────
row1_l, row1_r = st.columns(2)

with row1_l:
    st.subheader("📊 Avg Rating by Category")
    avg_rat = (filtered.groupby("Category")["Rating"].mean()
               .sort_values(ascending=False).head(15).reset_index())
    fig = px.bar(avg_rat, x="Rating", y="Category", orientation="h",
                 color="Rating", color_continuous_scale="plasma",
                 template="plotly_dark")
    fig.update_layout(showlegend=False, height=420,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with row1_r:
    st.subheader("🍩 Free vs Paid Apps")
    type_counts = filtered["Type"].value_counts().reset_index()
    type_counts.columns = ["Type","Count"]
    fig2 = px.pie(type_counts, names="Type", values="Count",
                  color_discrete_sequence=px.colors.sequential.RdBu,
                  template="plotly_dark", hole=0.45)
    fig2.update_layout(height=420,
                       paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

row2_l, row2_r = st.columns(2)

with row2_l:
    st.subheader("📈 Rating Distribution")
    fig3 = px.histogram(filtered, x="Rating", nbins=20,
                        color_discrete_sequence=["#e94560"],
                        template="plotly_dark")
    fig3.update_layout(height=350,
                       plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with row2_r:
    st.subheader("📦 Top 10 Categories by App Count")
    top_cats = filtered["Category"].value_counts().head(10).reset_index()
    top_cats.columns = ["Category","Count"]
    fig4 = px.bar(top_cats, x="Count", y="Category", orientation="h",
                  color="Count", color_continuous_scale="viridis",
                  template="plotly_dark")
    fig4.update_layout(showlegend=False, height=350,
                       plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

# ─── Reviews vs Rating Scatter ────────────────────────────────────────────────
st.subheader("🔵 Reviews vs Rating (by Category)")
scatter_df = filtered.dropna(subset=["Reviews","Rating","Category"])
scatter_df = scatter_df[scatter_df["Reviews"] < scatter_df["Reviews"].quantile(0.99)]
fig5 = px.scatter(scatter_df, x="Reviews", y="Rating", color="Category",
                  size_max=12, opacity=0.7,
                  template="plotly_dark",
                  hover_data=["App"] if "App" in scatter_df.columns else None)
fig5.update_layout(height=450,
                   plot_bgcolor="rgba(0,0,0,0)",
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig5, use_container_width=True)

# ─── Raw Data ─────────────────────────────────────────────────────────────────
with st.expander("🗃️ View Raw Data"):
    st.dataframe(filtered.head(200), use_container_width=True)

st.caption("Data source: Google Play Store Dataset • Project 01 — AI/ML Summer Internship")
