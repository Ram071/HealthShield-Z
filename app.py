import streamlit as st
import pandas as pd
import numpy as np
from src.model import generate_synthetic_healthcare_data, train_risk_model, get_audit_logs, log_audit_event

st.set_page_config(
    page_title="HealthShield Z | Experimental Risk Analytics",
    page_icon="🛡️",
    layout="wide"
)

df = generate_synthetic_healthcare_data(1000)
model, metrics, feature_names = train_risk_model(df)

st.sidebar.title("🛡️ HealthShield Z")
st.sidebar.markdown("Experimental Clinical Analytics Prototype")
menu = st.sidebar.radio("Navigation", ["Live Risk Dashboard", "Model Evaluation", "Audit Trail & Privacy", "System Architecture & Demo Script"])

if menu == "Live Risk Dashboard":
    st.title("🩺 Experimental Risk Analytics Dashboard")
    st.warning("⚠️ **Safety Notice:** This prototype uses synthetic data and heuristic correlations. It is strictly an experimental demonstration and does **not** provide validated clinical probabilities, medical diagnoses, or formal healthcare recommendations.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Patient Vitals Input")
        age = st.slider("Age", 18, 90, 45)
        bmi = st.slider("BMI", 15.0, 50.0, 26.5)
        bp = st.slider("Blood Pressure (mmHg)", 90, 200, 120)
        cholesterol = st.slider("Cholesterol (mg/dL)", 120, 350, 200)
        glucose = st.slider("Glucose Level (mg/dL)", 70, 300, 95)
        smoking = st.selectbox("Smoking Status", [("Non-Smoker", 0), ("Smoker", 1)], format_func=lambda x: x[0])[1]

    with col2:
        st.subheader("Experimental Risk Score Output")
        input_data = pd.DataFrame([[age, bmi, bp, cholesterol, glucose, smoking]], columns=feature_names)
        
        prob = model.predict_proba(input_data)[0][1]
        risk_percentage = round(prob * 100, 2)
        
        if risk_percentage > 70:
            st.error(f"🔴 **High Experimental Risk Score: {risk_percentage}%**")
            st.write("Notice: Profile exhibits high correlation with synthetic risk indicators.")
        elif risk_percentage > 40:
            st.warning(f"🟡 **Moderate Experimental Risk Score: {risk_percentage}%**")
            st.write("Notice: Moderate synthetic risk indicators identified.")
        else:
            st.success(f"🟢 **Low Experimental Risk Score: {risk_percentage}%**")
            st.write("Notice: Profile falls within normal synthetic baseline parameters.")

        log_audit_event("RISK_ASSESSMENT", "Evaluated anonymous patient profile.")

    st.markdown("---")
    st.subheader("📊 Feature Importance (Explainable AI)")
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    st.bar_chart(feat_imp_df.set_index('Feature'))

elif menu == "Model Evaluation":
    st.title("📈 Robust Model Evaluation Metrics")
    st.markdown("Performance metrics evaluated on held-out synthetic test data (20% split).")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%")
    c2.metric("Precision", f"{metrics['precision']*100:.2f}%")
    c3.metric("Recall", f"{metrics['recall']*100:.2f}%")
    c4.metric("ROC-AUC", f"{metrics['roc_auc']:.3f}")

    st.subheader("Confusion Matrix")
    conf_df = pd.DataFrame(
        metrics['conf_matrix'], 
        index=["Actual Low Risk", "Actual High Risk"], 
        columns=["Predicted Low", "Predicted High"]
    )
    st.dataframe(conf_df, use_container_width=True)

elif menu == "Audit Trail & Privacy":
    st.title("🔒 Audit Trail & Privacy Safeguards")
    
    st.subheader("Persistent SQLite Audit Log (UTC Timestamps)")
    audit_df = get_audit_logs()
    st.dataframe(audit_df, use_container_width=True)
    
    st.subheader("Privacy Design")
    st.info("ℹ️ **Privacy Notice:** No patient identifiers or submitted feature values are stored in audit logs.")

elif menu == "System Architecture & Demo Script":
    st.title("🏗️ Architecture & Hackathon Demo Script")
    st.markdown("""
    ### 🎬 Hackathon Demo Script (2-Minute Pitch)
    1. **Introduction (0:00 - 0:30):** Introduce *HealthShield Z* — experimental analytics prototype demonstrating transparent machine learning and secure audit logging.
    2. **Live Dashboard & Safety (0:30 - 1:00):** Adjust sliders on the Live Risk Dashboard. Emphasize explicit safety disclaimers and lack of medical recommendations.
    3. **Model Rigor & Evaluation (1:00 - 1:30):** Show precision, recall, ROC-AUC, and confusion matrix on held-out test data.
    4. **Audit Trail & Deployment (1:30 - 2:00):** Highlight persistent SQLite logging with UTC timestamps and LinuxONE containerization readiness.
    """)
