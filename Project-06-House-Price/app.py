import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }
.prediction-box {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    border-radius: 14px;
    padding: 25px;
    text-align: center;
    color: white;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 20px 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.metric-card {
    background-color: #1e1e30;
    border: 1px solid #2d2d44;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}
.metric-card h3 { margin: 0; color: #888; font-size: 0.9rem; text-transform: uppercase; }
.metric-card p { margin: 5px 0 0 0; font-size: 1.6rem; font-weight: 700; color: #fff; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#11998e 0%,#38ef7d 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.35);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">🏠 House Price Prediction Dashboard</h1>
    <p style="color:#eefcf4;margin:8px 0 0;font-size:1.05rem;">
        Estimate house valuations using simple Linear Regression on area dimensions
    </p>
</div>
""", unsafe_allow_html=True)

CSV_PATH = "houseprice.csv"

# ─── Load Dataset ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        # Fallback dataset
        data = {
            "area": [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 1200, 1800, 2200, 2800, 3200, 3800, 4200, 900, 1100, 1600, 2100],
            "price": [50000, 75000, 100000, 125000, 150000, 175000, 200000, 225000, 250000, 62000, 92000, 112000, 140000, 162000, 192000, 212000, 45000, 55000, 82000, 107000]
        }
        df = pd.DataFrame(data)
    return df

df = load_data()

# ─── Model Training ──────────────────────────────────────────────────────────
X = df[["area"]].values
y = df["price"].values

model = LinearRegression()
model.fit(X, y)

# ─── UI Layout ────────────────────────────────────────────────────────────────
col_input, col_results = st.columns([1, 1])

with col_input:
    st.subheader("⚙️ Predict Valuation")
    input_area = st.number_input(
        "Enter House Area (sq ft):",
        min_value=100,
        max_value=20000,
        value=1800,
        step=50
    )
    
    predicted_val = model.predict([[input_area]])[0]
    
    st.markdown(f"""
    <div class="prediction-box">
        ${predicted_val:,.2f}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Model Parameters**")
    m_val = model.coef_[0]
    c_val = model.intercept_
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Slope (Price/sqft)</h3>
            <p>${m_val:.2f}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Intercept</h3>
            <p>${c_val:,.2f}</p>
        </div>""", unsafe_allow_html=True)

with col_results:
    st.subheader("📈 Linear Fit Visualizer")
    
    # Generate regression line points
    x_range = np.linspace(df["area"].min() * 0.8, df["area"].max() * 1.2, 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    
    fig = go.Figure()
    # Scatter data
    fig.add_trace(go.Scatter(
        x=df["area"], y=df["price"],
        mode="markers",
        marker=dict(size=9, color="#11998e"),
        name="Actual Listings"
    ))
    # Line
    fig.add_trace(go.Scatter(
        x=x_range, y=y_range,
        mode="lines",
        line=dict(color="#38ef7d", width=3),
        name="Regression Line"
    ))
    # User point
    fig.add_trace(go.Scatter(
        x=[input_area], y=[predicted_val],
        mode="markers",
        marker=dict(size=14, color="#e94560", symbol="star"),
        name="Your Valuation"
    ))
    
    fig.update_layout(
        xaxis_title="Area (sq ft)",
        yaxis_title="Price ($)",
        template="plotly_dark",
        height=380,
        margin=dict(t=20, b=20, l=20, r=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Dataset Preview")
st.dataframe(df.T, use_container_width=True)

st.caption("Project 06 — House Price Prediction • AI/ML Summer Internship")
