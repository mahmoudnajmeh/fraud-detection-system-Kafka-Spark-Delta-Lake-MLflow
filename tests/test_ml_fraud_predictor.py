from fraud_detection.models.data_models import Transaction
from fraud_detection.processors.ml_fraud_predictor import MLFraudPredictor


def test_ml_predictor_scores_high_risk_transaction():
    predictor = MLFraudPredictor()
    transaction = Transaction(
        user_id="test_user",
        amount=18000,
        merchant="Test Merchant",
        location="Berlin, DE",
        payment_method="CREDIT_CARD",
    )
    enriched = {
        "transaction": transaction,
        "user_profile": {
            "risk_score": 90,
            "avg_transaction_amount": 500,
            "country": "US",
            "verified": False,
        },
        "user_history": [
            {"amount": 2500},
            {"amount": 3000},
            {"amount": 4500},
            {"amount": 5000},
            {"amount": 6000},
        ],
    }

    prediction = predictor.predict(enriched)

    assert prediction.risk_score >= 75
    assert predictor.is_fraud(prediction)
    assert prediction.model_name == "random_forest_fraud_model"


def test_ml_predictor_scores_low_risk_transaction():
    predictor = MLFraudPredictor()
    transaction = Transaction(
        user_id="test_user",
        amount=75,
        merchant="Test Merchant",
        location="New York, US",
        payment_method="DEBIT_CARD",
    )
    enriched = {
        "transaction": transaction,
        "user_profile": {
            "risk_score": 5,
            "avg_transaction_amount": 100,
            "country": "US",
            "verified": True,
        },
        "user_history": [],
    }

    prediction = predictor.predict(enriched)

    assert prediction.risk_score < 75
    assert not predictor.is_fraud(prediction)
