# HealthShield Z — Experimental Risk Analytics Prototype

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Ram071/HealthShield-Z&branch=main&mainModule=app.py)
[![Live Demo on GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen?logo=github)](https://ram071.github.io/HealthShield-Z/)
[![CI/CD Pipeline](https://github.com/Ram071/HealthShield-Z/actions/workflows/ci.yml/badge.svg)](https://github.com/Ram071/HealthShield-Z/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

HealthShield Z is an enterprise-grade, privacy-first experimental clinical analytics prototype built for the **IBM Z Datathon 2026**, optimized for LinuxONE and IBM Z architectures.

---

## 🌐 Live Deployments

### Option 1: 1-Click Streamlit Community Cloud (Recommended)
Deploy and host this app online in 30 seconds for free:
👉 **[Click Here to 1-Click Deploy on Streamlit Cloud](https://share.streamlit.io/deploy?repository=Ram071/HealthShield-Z&branch=main&mainModule=app.py)**

### Option 2: Live GitHub Pages Web Demo (WebAssembly)
An in-browser WebAssembly version powered by Pyodide and stlite:
👉 **[View Live GitHub Pages Demo](https://ram071.github.io/HealthShield-Z/)**

---

## 🚀 Key Features
- **Reproducible Synthetic Dataset:** 1,000 records generated via documented metabolic rules.
- **Explainable AI (XAI):** Real-time feature importance rankings alongside clinical risk predictions.
- **Robust Evaluation:** Precision, recall, F1, ROC-AUC (~0.98), and confusion matrix on held-out test data.
- **Persistent Audit Logging:** SQLite event logging with standardized UTC timestamps.
- **Privacy Safeguards:** Zero PII storage; no direct patient identifiers or feature values persisted.
- **Automated CI/CD:** Pytest test suite executed automatically on every GitHub push and PR.
- **IBM Z / LinuxONE Ready:** Validated Dockerfile ready for containerized execution on s390x and x86.

---

## 🛠️ Quickstart Guide

### 1. Local Setup
```bash
# Clone the repository
git clone https://github.com/Ram071/HealthShield-Z.git
cd HealthShield-Z

# Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Automated Tests
```bash
python -m pytest tests -v
```

### 3. Launch Dashboard
```bash
streamlit run app.py
```

### 4. Run with Docker (LinuxONE / Local)
```bash
docker build -t healthshield-z .
docker run -d -p 8501:8501 --name healthshield-app healthshield-z
```
