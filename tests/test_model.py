import pytest
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

def test_audit_persistence():
    log_audit_event("TEST_ACTION", "Testing audit log persistence")
    logs = get_audit_logs()
    assert not logs.empty
    assert "TEST_ACTION" in logs['action'].values
