import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Iris Clustering Dashboard",
    page_icon="🌸",
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
    background: linear-gradient(135deg, #3a1c71 0%, #d76d77 50%, #ffaf7b 100%);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}
.metric-box h2 { font-size: 2rem; margin: 0; }
.metric-box p { color: #fff; opacity: 0.9; font-size: 0.85rem; margin: 5px 0 0 0; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#3a1c71 0%,#d76d77 50%,#ffaf7b 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.35);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">🌸 Iris Flower K-Means Clustering</h1>
    <p style="color:#ffffff;margin:8px 0 0;font-size:1.05rem;opacity:0.9;">
        Unsupervised categorization of Iris species based on sepal and petal features
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Load Dataset ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["target"] = iris.target
    df["species"] = df["target"].map({0: "setosa", 1: "versicolor", 2: "virginica"})
    return df, iris.feature_names

df, features_all = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Clustering Parameters")
x_feat = st.sidebar.selectbox("X-Axis Feature", features_all, index=2) # default petal length
y_feat = st.sidebar.selectbox("Y-Axis Feature", features_all, index=3) # default petal width

k_val = st.sidebar.slider("Number of Clusters (K)", 2, 6, 3)

show_ground_truth = st.sidebar.checkbox("Compare with Ground Truth (Species)", value=True)

# ─── Preprocessing & K-Means ──────────────────────────────────────────────────
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[[x_feat, y_feat]]),
    columns=[x_feat, y_feat]
)

km = KMeans(n_clusters=k_val, random_state=42, n_init=10)
df["Cluster"] = km.fit_predict(df_scaled)
df["Cluster"] = df["Cluster"].astype(str)

# Calculate SSE for Elbow Chart
sse = []
k_rng = range(1, 8)
for k in k_rng:
    kmean_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmean_temp.fit(df_scaled)
    sse.append(kmean_temp.inertia_)

# ─── Layout & Visuals ────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎯 K-Means Clusters")
    
    # Get centroids
    centroids = scaler.inverse_transform(km.cluster_centers_)
    centroid_df = pd.DataFrame(centroids, columns=[x_feat, y_feat])
    
    fig_cluster = px.scatter(
        df, x=x_feat, y=y_feat, color="Cluster",
        title=f"K-Means (K={k_val}) Clusters",
        color_discrete_sequence=px.colors.qualitative.Bold,
        template="plotly_dark"
    )
    
    # Add centroids
    for idx, row in centroid_df.iterrows():
        fig_cluster.add_scatter(
            x=[row[x_feat]], y=[row[y_feat]],
            mode="markers",
            marker=dict(size=14, color="white", symbol="x", line=dict(width=2, color="black")),
            name=f"Centroid {idx}"
        )
        
    fig_cluster.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_cluster, use_container_width=True)

with col2:
    if show_ground_truth:
        st.subheader("🌿 Actual Species (Ground Truth)")
        fig_truth = px.scatter(
            df, x=x_feat, y=y_feat, color="species",
            title="Actual Species Labels",
            color_discrete_sequence=px.colors.qualitative.Safe,
            template="plotly_dark"
        )
        fig_truth.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_truth, use_container_width=True)
    else:
        st.subheader("📈 Elbow Method Curve")
        fig_elbow = px.line(
            x=list(k_rng), y=sse,
            labels={"x": "K", "y": "Sum of Squared Errors (SSE)"},
            title="Optimal Cluster Evaluation",
            markers=True,
            template="plotly_dark"
        )
        fig_elbow.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_elbow, use_container_width=True)

# ─── Stats Table ─────────────────────────────────────────────────────────────
st.subheader("📋 Dataset Preview & Cluster Mapping")
st.dataframe(
    df[[x_feat, y_feat, "species", "Cluster"]].head(150),
    use_container_width=True,
    height=240
)

st.caption("Project 10 — Iris Flower Clustering • AI/ML Summer Internship")
