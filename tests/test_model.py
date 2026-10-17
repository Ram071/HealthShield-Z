import pytest
import os
import pandas as pd
from src.model import generate_synthetic_healthcare_data, train_risk_model, log_audit_event, get_audit_logs

def test_synthetic_data_generation():
    df = generate_synthetic_healthcare_data(100)
    assert len(df) == 100
    expected_cols = {'age', 'bmi', 'blood_pressure', 'cholesterol', 'glucose', 'smoking_status', 'target_risk'}
    assert expected_cols.issubset(df.columns)

def test_model_training_and_metrics():
    df = generate_synthetic_healthcare_data(200)
    model, metrics, features = train_risk_model(df)
    
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1' in metrics
    assert 'roc_auc' in metrics
    assert 0.0 <= metrics['accuracy'] <= 1.0
    assert 0.0 <= metrics['roc_auc'] <= 1.0

def test_prediction_output_bounds():
    df = generate_synthetic_healthcare_data(200)
    model, _, features = train_risk_model(df)
    
    sample_input = pd.DataFrame([[55, 28.5, 135, 210, 110, 1]], columns=features)
    prob = model.predict_proba(sample_input)[0][1]
    assert 0.0 <= prob <= 1.0

def test_sample_csv_compatibility():
    sample_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_patient_data.csv')
    if os.path.exists(sample_csv_path):
        df = pd.read_csv(sample_csv_path)
        required_cols = {'age', 'bmi', 'blood_pressure', 'cholesterol', 'glucose', 'smoking_status', 'target_risk'}
        assert required_cols.issubset(df.columns)
        assert len(df) > 0

def test_audit_persistence():
    log_audit_event("TEST_ACTION", "Testing audit log persistence")
    logs = get_audit_logs()
    assert not logs.empty
    assert "TEST_ACTION" in logs['action'].values
