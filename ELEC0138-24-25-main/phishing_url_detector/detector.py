# app.py

import streamlit as st
import joblib
from predict_helper import predict_url_phishing_proba, Converter

st.set_page_config(page_title="Phishing Detector", layout="centered")
st.title("🔐 Phishing URL Detection App")

@st.cache_resource
def load_model():
    return joblib.load("models/logreg_pipeline_model.pkl")

model = load_model()

def get_risk_label(score):
    if score >= 0.9:
        return "🟥 Extremely High", "error"
    elif score >= 0.7:
        return "🟧 High", "warning"
    elif score >= 0.4:
        return "🟨 Medium", "info"
    else:
        return "🟩 Low", "success"

url = st.text_input("🔗 Enter a URL to check", placeholder="e.g. http://secure-update-medicare-login.com")

if url:
    proba = predict_url_phishing_proba(url, model, show_output=False)
    st.metric("Phishing Probability", f"{proba:.3f}")
    label, style = get_risk_label(proba)
    getattr(st, style)(f"Risk Level: {label}")