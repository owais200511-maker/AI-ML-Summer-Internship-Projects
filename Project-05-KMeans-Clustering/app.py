import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import os

st.set_page_config(
    page_title="K-Means Clustering App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }
.metric-card {
    background: linear-gradient(135deg, #1f4068 0%, #162447 100%);
    border: 1px solid #1f4068;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-card h2 { color: #e94560; font-size: 2.2rem; margin: 0; }
.metric-card p { color: #a8b2d8; font-size: 0.9rem; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1f4068 0%,#162447 50%,#1a1a2e 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">📊 K-Means Clustering Dashboard</h1>
    <p style="color:#a8b2d8;margin:8px 0 0;font-size:1.05rem;">
        Partition datasets into distinct groups based on income and age characteristics
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ──────────────────────────────────────────────────────────────
CSV_PATH = "income.csv"

@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        # Fallback inline data
        data = {
            "Name": ["Rob","Michael","Mohan","Ismail","Kory","Gautam","David","Brad","Ramona","Vanessa","Steve","Liana","Raja","Priya","John","Sarah","Emily","Mark","Helen","Tom"],
            "Age": [27, 29, 29, 28, 42, 41, 43, 43, 38, 39, 44, 45, 24, 25, 26, 27, 34, 35, 36, 37],
            "Income($)": [70000, 90000, 61000, 60000, 150000, 155000, 160000, 162000, 115000, 119000, 170000, 180000, 35000, 38000, 42000, 45000, 95000, 98000, 102000, 108000]
        }
        df = pd.DataFrame(data)
    df.columns = [col.strip() for col in df.columns]
    return df

df = load_data()

st.subheader("📋 Dataset Overview")
col_tbl, col_desc = st.columns([2, 1])
with col_tbl:
    st.dataframe(df, use_container_width=True, height=220)
with col_desc:
    st.write("**Summary Statistics**")
    st.dataframe(df.describe().T, use_container_width=True)

# ─── Sidebar Controls ────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Clustering Settings")
features = st.sidebar.multiselect(
    "Features to Cluster",
    options=["Age", "Income($)"],
    default=["Age", "Income($)"]
)

k_val = st.sidebar.slider("Number of Clusters (K)", min_value=2, max_value=8, value=3)

if len(features) < 2:
    st.warning("⚠️ Please select at least 2 features for optimal 2D/3D visualization and clustering.")
    st.stop()

# ─── Preprocessing ──────────────────────────────────────────────────────────
scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[features] = scaler.fit_transform(df[features])

# ─── Elbow Method ────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
show_elbow = st.sidebar.checkbox("Compute Elbow Method", value=True)

if show_elbow:
    sse = []
    k_rng = range(1, 10)
    for k in k_rng:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(df_scaled[features])
        sse.append(km.inertia_)
    
    fig_elbow = px.line(
        x=list(k_rng), y=sse, 
        labels={"x": "K (Number of clusters)", "y": "Sum of Squared Error (SSE)"},
        title="📈 The Elbow Method (Find Optimal K)",
        template="plotly_dark",
        markers=True
    )
    fig_elbow.update_layout(height=280, margin=dict(t=40, b=10, l=10, r=10),
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

# ─── Clustering Execution ────────────────────────────────────────────────────
km = KMeans(n_clusters=k_val, random_state=42, n_init=10)
df["Cluster"] = km.fit_predict(df_scaled[features])
df_scaled["Cluster"] = df["Cluster"]

# Convert cluster ID to string category for visual clarity
df["Cluster"] = df["Cluster"].astype(str)
df_scaled["Cluster"] = df_scaled["Cluster"].astype(str)

# Get centroids
centroids = scaler.inverse_transform(km.cluster_centers_)
centroid_df = pd.DataFrame(centroids, columns=features)
centroid_df["Cluster"] = [f"Centroid {i}" for i in range(k_val)]

# ─── Plotly Scatter Plot ─────────────────────────────────────────────────────
st.subheader("🎯 Clustering Results")

col_plot, col_stats = st.columns([2, 1])

with col_plot:
    fig_scatter = px.scatter(
        df, 
        x=features[0], 
        y=features[1], 
        color="Cluster",
        hover_data=["Name"],
        title=f"K-Means Clustering (K = {k_val})",
        color_discrete_sequence=px.colors.qualitative.Bold,
        template="plotly_dark"
    )
    
    # Add centroids
    for idx, row in centroid_df.iterrows():
        fig_scatter.add_scatter(
            x=[row[features[0]]],
            y=[row[features[1]]],
            mode="markers",
            marker=dict(size=14, color="white", symbol="x", line=dict(width=2, color="black")),
            name=f"Centroid {idx}",
            showlegend=True
        )
        
    fig_scatter.update_layout(height=420, margin=dict(t=40, b=10, l=10, r=10),
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_stats:
    st.write("**Cluster Summary**")
    for cluster_id in sorted(df["Cluster"].unique()):
        cluster_data = df[df["Cluster"] == cluster_id]
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:12px; padding: 12px;">
            <h2 style="font-size: 1.5rem; color: #ffa726;">Cluster {cluster_id}</h2>
            <p>Count: <strong>{len(cluster_data)}</strong> | Avg Age: <strong>{cluster_data['Age'].mean():.1f}</strong> | Avg Income: <strong>${cluster_data['Income($)'].mean():,.0f}</strong></p>
        </div>
        """, unsafe_allow_html=True)

if show_elbow:
    st.plotly_chart(fig_elbow, use_container_width=True)

st.caption("Project 05 — K-Means Clustering • AI/ML Summer Internship")
