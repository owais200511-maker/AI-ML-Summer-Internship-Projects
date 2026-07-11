import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="MALE vs FEMALE Classifier",
    page_icon="😊",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3 { font-family: 'Outfit', sans-serif; }
.result-box {
    border-radius: 16px; padding: 28px; text-align: center;
    font-size: 2rem; font-weight: 700; margin: 20px 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    animation: fadeIn 0.6s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.male-box    { background: linear-gradient(135deg,#00b4db,#0083b0); color:white; }
.female-box  { background: linear-gradient(135deg,#ff758c,#ff7eb3); color:white; }
.upload-zone { border: 2px dashed #555; border-radius:12px;
               padding:30px; text-align:center; background:#111; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0083b0 0%,#ff7eb3 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">👨 Male vs Female Image Classifier</h1>
    <p style="color:#e0f7fa;margin:8px 0 0;font-size:1rem;">
        Classify facial images using DeepFace Deep Learning Models — 95%+ accuracy
    </p>
</div>
""", unsafe_allow_html=True)

# ── DeepFace Model Loading ────────────────────────────────────────────────────
@st.cache_resource(show_spinner=True)
def load_deepface():
    """Import and warm up DeepFace (downloads model weights on first run)."""
    from deepface import DeepFace
    return DeepFace

with st.spinner("🧠 Loading Deep Learning Model (first time may take ~30 s)..."):
    DeepFace = load_deepface()

# ── Upload Section ─────────────────────────────────────────────────────────────
st.subheader("📤 Upload Face Image")
uploaded = st.file_uploader(
    "Choose a JPG/PNG face image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded:
    image_data = Image.open(uploaded).convert("RGB")
    col_img, col_result = st.columns([1, 1])

    with col_img:
        st.subheader("🖼️ Uploaded Image")
        st.image(image_data, use_column_width=True, caption=uploaded.name)

    with col_result:
        st.subheader("🔍 Prediction")

        with st.spinner("Analysing face..."):
            img_arr = np.array(image_data)
            try:
                results = DeepFace.analyze(
                    img_arr,
                    actions=["gender"],
                    enforce_detection=False,
                    detector_backend="skip",
                    silent=True
                )
                # DeepFace returns a list; take the first detected face
                result = results[0] if isinstance(results, list) else results
                gender_scores = result["gender"]          # {'Man': %, 'Woman': %}
                male_pct   = gender_scores.get("Man", 0)
                female_pct = gender_scores.get("Woman", 0)
                dominant   = result["dominant_gender"]     # 'Man' or 'Woman'

                is_male    = dominant == "Man"
                label      = "👨 MALE" if is_male else "👩 FEMALE"
                confidence = male_pct if is_male else female_pct
                css_class  = "male-box" if is_male else "female-box"

                st.markdown(f"""
                <div class="result-box {css_class}">
                    {label}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Confidence Scores**")
                st.metric("👨 Male Probability", f"{male_pct:.1f}%")
                st.progress(male_pct / 100)
                st.metric("👩 Female Probability", f"{female_pct:.1f}%")
                st.progress(female_pct / 100)

                st.info(f"**Overall Confidence:** {confidence:.1f}%")

            except Exception as e:
                st.error(f"⚠️ Could not analyse the image: {e}")
                st.info("Please upload a clear frontal face photo for best results.")
else:
    st.markdown("""
    <div class="upload-zone">
        <p style="color:#888;font-size:1.1rem;">
            👆 Upload a facial photo to classify gender
        </p>
    </div>
    """, unsafe_allow_html=True)

st.caption("Project 09 — Male vs Female Classifier • AI/ML Summer Internship")
