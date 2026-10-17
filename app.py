import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from src.model import generate_synthetic_healthcare_data, train_risk_model, get_audit_logs, log_audit_event

st.set_page_config(
    page_title="HealthShield Z | Experimental Risk Analytics",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("🛡️ HealthShield Z")
st.sidebar.markdown("Experimental Clinical Analytics Prototype")

# --- CUSTOM DATASET UPLOADER ---
st.sidebar.subheader("📂 Data Source")

# Downloadable Sample CSV template
sample_template_df = generate_synthetic_healthcare_data(50)
sample_csv_bytes = sample_template_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Download Sample CSV Template",
    data=sample_csv_bytes,
    file_name="sample_patient_data.csv",
    mime="text/csv",
    help="Download a 50-row CSV file with the exact required schema to test the uploader."
)

uploaded_file = st.sidebar.file_uploader("Upload custom CSV dataset", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {'age', 'bmi', 'blood_pressure', 'cholesterol', 'glucose', 'smoking_status', 'target_risk'}
        if required_cols.issubset(df.columns):
            st.sidebar.success(f"Loaded custom dataset ({len(df)} rows)!")
        else:
            st.sidebar.error(f"Missing required columns: {required_cols - set(df.columns)}")
            st.sidebar.info("Falling back to synthetic dataset.")
            df = generate_synthetic_healthcare_data(1000)
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        df = generate_synthetic_healthcare_data(1000)
else:
    df = generate_synthetic_healthcare_data(1000)
    st.sidebar.info("Using default synthetic dataset (1,000 records).")

# Train model on whichever dataset is active
model, metrics, feature_names = train_risk_model(df)

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

        # Real-time clinical risk factor breakdown
        alerts = []
        if bp > 140:
            alerts.append("⚠️ **Stage 2 Hypertension Alert** (Systolic BP > 140 mmHg)")
        if glucose > 140:
            alerts.append("⚠️ **Hyperglycemia Marker** (Blood Glucose > 140 mg/dL)")
        if bmi > 30.0:
            alerts.append("⚠️ **Elevated BMI (Obesity Range)** (BMI > 30.0 kg/m²)")
        if cholesterol > 200:
            alerts.append("⚠️ **Hypercholesterolemia Marker** (Cholesterol > 200 mg/dL)")
        if age > 50:
            alerts.append("⚠️ **Age Demographic Factor** (Age > 50)")
        if smoking == 1:
            alerts.append("⚠️ **Active Tobacco Smoking Factor**")

        if alerts:
            with st.expander("🔍 Identified Clinical Risk Drivers", expanded=True):
                for a in alerts:
                    st.markdown(f"- {a}")
        else:
            st.info("ℹ️ All patient vitals fall within standard synthetic baseline parameters.")

        log_audit_event("RISK_ASSESSMENT", f"Evaluated patient profile (Calculated Risk: {risk_percentage}%).")

    st.markdown("---")
    st.subheader("📊 Feature Importance (Explainable AI)")
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    st.bar_chart(feat_imp_df.set_index('Feature'))

elif menu == "Model Evaluation":
    st.title("📈 Robust Model Evaluation Metrics")
    st.markdown(f"Performance metrics evaluated on held-out test data (20% split of {len(df)} records).")
    
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

    if not audit_df.empty:
        audit_csv = audit_df.to_csv(index=False).encode('utf-8')
        utc_stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        st.download_button(
            label="📥 Export Audit Trail (CSV)",
            data=audit_csv,
            file_name=f"healthshield_audit_logs_{utc_stamp}.csv",
            mime="text/csv",
            help="Export complete audit history for compliance and governance reviews."
        )
    
    st.subheader("Privacy Design")
    st.info("ℹ️ **Privacy Notice:** No patient identifiers or raw submitted feature values are stored in audit logs.")

elif menu == "System Architecture & Demo Script":
    st.title("🏗️ Architecture & Hackathon Demo Script")
    st.markdown("""
    ### 🎬 Hackathon Demo Script (2-Minute Pitch)
    1. **Introduction (0:00 - 0:30):** Introduce *HealthShield Z* — experimental analytics prototype demonstrating transparent machine learning and secure audit logging.
    2. **Live Dashboard & Safety (0:30 - 1:00):** Adjust sliders on the Live Risk Dashboard. Emphasize explicit safety disclaimers and lack of medical recommendations.
    3. **Model Rigor & Evaluation (1:00 - 1:30):** Show precision, recall, ROC-AUC, and confusion matrix on held-out test data.
    4. **Audit Trail & Deployment (1:30 - 2:00):** Highlight persistent SQLite logging with UTC timestamps and LinuxONE containerization readiness.
    """)
