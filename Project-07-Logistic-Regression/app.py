import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
import os

st.set_page_config(
    page_title="Insurance Purchase Prediction",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }
.prediction-card {
    border-radius: 14px;
    padding: 25px;
    text-align: center;
    color: white;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 20px 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.yes-card { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.no-card  { background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%); }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#cb2d3e 0%,#ef473a 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.35);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">🛡️ Life Insurance Purchase Prediction</h1>
    <p style="color:#ffd9db;margin:8px 0 0;font-size:1.05rem;">
        Predict likelihood of life insurance acquisition based on age using Logistic Regression
    </p>
</div>
""", unsafe_allow_html=True)

CSV_PATH = "insurance_data.csv"

# ─── Load Dataset ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        # Fallback dataset
        data = {
            "age": [22, 25, 47, 52, 46, 56, 55, 60, 62, 61, 18, 28, 27, 29, 49, 33, 35, 44, 48, 31, 38, 57, 63, 24, 26, 58, 42, 50, 43, 21, 30, 66, 68, 36, 40, 53, 65, 69, 20, 34],
            "bought_insurance": [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0]
        }
        df = pd.DataFrame(data)
    return df

df = load_data()

# ─── Model Training ──────────────────────────────────────────────────────────
X = df[["age"]].values
y = df["bought_insurance"].values

model = LogisticRegression()
model.fit(X, y)

# ─── UI Layout ────────────────────────────────────────────────────────────────
col_input, col_results = st.columns([1, 1])

with col_input:
    st.subheader("⚙️ Predict Insurance Acquisition")
    input_age = st.slider("Enter Age:", min_value=1, max_value=100, value=35)
    
    pred_prob = model.predict_proba([[input_age]])[0]
    prob_buy = pred_prob[1]
    prob_no = pred_prob[0]
    
    pred_class = model.predict([[input_age]])[0]
    
    if pred_class == 1:
        st.markdown(f"""
        <div class="prediction-card yes-card">
            ✅ Will Buy Insurance ({prob_buy*100:.1f}%)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="prediction-card no-card">
            ❌ Unlikely to Buy ({prob_no*100:.1f}%)
        </div>
        """, unsafe_allow_html=True)
        
    st.write("**Prediction Probability Breakdown**")
    st.progress(prob_buy)
    st.markdown(f"Probability of purchasing: **{prob_buy*100:.1f}%**")
    st.markdown(f"Probability of not purchasing: **{prob_no*100:.1f}%**")

with col_results:
    st.subheader("📈 Logistic Sigmoid Curve")
    
    # Generate sigmoid line points
    x_range = np.linspace(10, 80, 200)
    y_prob = model.predict_proba(x_range.reshape(-1, 1))[:, 1]
    
    fig = go.Figure()
    # Scatter data
    fig.add_trace(go.Scatter(
        x=df["age"], y=df["bought_insurance"],
        mode="markers",
        marker=dict(size=9, color=df["bought_insurance"].map({0:"#ef473a", 1:"#38ef7d"})),
        name="Users"
    ))
    # Sigmoid Curve
    fig.add_trace(go.Scatter(
        x=x_range, y=y_prob,
        mode="lines",
        line=dict(color="#ffd9db", width=3),
        name="Sigmoid Probability"
    ))
    # User point
    fig.add_trace(go.Scatter(
        x=[input_age], y=[prob_buy],
        mode="markers",
        marker=dict(size=14, color="#ffa726", symbol="star"),
        name="Current Query"
    ))
    
    # Decision boundary line (y = 0.5)
    # Solve 1 / (1 + exp(-(m*x + c))) = 0.5 => m*x + c = 0 => x = -c/m
    m_val = model.coef_[0][0]
    c_val = model.intercept_[0]
    decision_boundary = -c_val / m_val
    fig.add_vline(x=decision_boundary, line_dash="dash", line_color="#ffa726",
                 annotation_text=f"Decision Boundary ({decision_boundary:.1f} yrs)")
    
    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Probability of Buying Insurance",
        template="plotly_dark",
        height=380,
        margin=dict(t=20, b=20, l=20, r=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Dataset Preview")
st.dataframe(df.T, use_container_width=True)

st.caption("Project 07 — Logistic Regression Purchase Predictor • AI/ML Summer Internship")
