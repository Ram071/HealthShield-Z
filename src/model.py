import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import sqlite3
from datetime import datetime, timezone

DB_NAME = "healthshield_audit.db"

def init_audit_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_audit_event(action, details):
    init_audit_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    cursor.execute("INSERT INTO audit_logs (timestamp, action, details) VALUES (?, ?, ?)", (utc_time, action, details))
    conn.commit()
    conn.close()

def get_audit_logs():
    init_audit_db()
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT timestamp, action, details FROM audit_logs ORDER BY id DESC", conn)
    conn.close()
    return df

def generate_synthetic_healthcare_data(n=1000):
    np.random.seed(42)
    age = np.random.randint(25, 80, n)
    bmi = np.random.uniform(18.0, 42.0, n)
    blood_pressure = np.random.randint(90, 180, n)
    cholesterol = np.random.randint(150, 320, n)
    glucose = np.random.randint(70, 250, n)
    smoking_status = np.random.choice([0, 1], size=n, p=[0.7, 0.3])
    
    risk_score_latent = (
        (age > 50).astype(int) * 1.5 +
        (bmi > 30).astype(int) * 2.0 +
        (blood_pressure > 140).astype(int) * 2.0 +
        (glucose > 140).astype(int) * 2.5 +
        smoking_status * 1.5 +
        np.random.normal(0, 0.8, n)
    )
    target_risk = (risk_score_latent > 4.5).astype(int)
    
    df = pd.DataFrame({
        'age': age,
        'bmi': np.round(bmi, 1),
        'blood_pressure': blood_pressure,
        'cholesterol': cholesterol,
        'glucose': glucose,
        'smoking_status': smoking_status,
        'target_risk': target_risk
    })
    return df

def train_risk_model(df):
    X = df.drop(columns=['target_risk'])
    y = df['target_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y_test, preds),
        'precision': precision_score(y_test, preds, zero_division=0),
        'recall': recall_score(y_test, preds, zero_division=0),
        'f1': f1_score(y_test, preds, zero_division=0),
        'roc_auc': roc_auc_score(y_test, probs) if len(np.unique(y_test)) > 1 else 0.5,
        'conf_matrix': confusion_matrix(y_test, preds)
    }
    
    log_audit_event("MODEL_TRAINING", f"RandomForest trained on {len(df)} records. Accuracy: {metrics['accuracy']:.2f}")
    return model, metrics, X.columns
