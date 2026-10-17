# HealthShield Z — Experimental Risk Analytics Prototype

HealthShield Z is an experimental clinical analytics prototype built for the **IBM Z Datathon 2026**.

## 🚀 Key Features
- **Reproducible Synthetic Dataset:** 1,000 records generated via documented metabolic rules.
- **Robust Evaluation:** Precision, recall, F1, ROC-AUC, and confusion matrix on held-out test data.
- **Persistent Audit Logging:** SQLite event logging with UTC timestamps.
- **Privacy Safeguards:** No direct patient identifiers or feature values stored in logs.
- **Automated Tests:** Comprehensive pytest suite (`python -m pytest -q`).

## 🛠️ Quickstart Guide
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python -m pytest -q
   ```

3. Run the dashboard:
   ```bash
   streamlit run app.py
   ```
