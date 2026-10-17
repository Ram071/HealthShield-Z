# IBM Z / LinuxONE Deployment Notes

## Verified Functionality
- Local execution via Streamlit and Python.
- Persistent SQLite audit logging (`healthshield_audit.db`).
- Automated testing via pytest (`python -m pytest -q`).

## LinuxONE Containerization (Safe Execution)
To package the application for evaluation in an assigned s390x / LinuxONE environment without volume masking issues:

1. **Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run (Standard Container Execution):**
   ```bash
   docker build -t healthshield-z .
   docker run -d -p 8501:8501 --name healthshield-app healthshield-z
   ```
