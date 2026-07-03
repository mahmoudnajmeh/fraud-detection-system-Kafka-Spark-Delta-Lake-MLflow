from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Any, Dict, List, Tuple

from loguru import logger

try:
    from sklearn.ensemble import RandomForestClassifier
except Exception:
    RandomForestClassifier = None

from fraud_detection.models.data_models import Transaction


@dataclass
class MLPrediction:
    fraud_probability: float
    risk_score: int
    model_name: str
    model_version: str
    features: Dict[str, float]


class MLFraudPredictor:
    def __init__(self):
        self.model_name = "random_forest_fraud_model"
        self.model_version = "1.1.0"
        self.threshold = 0.50
        self.model = None
        self.feature_names = [
            "amount",
            "user_risk_score",
            "recent_transaction_count",
            "recent_total_amount",
            "amount_to_average_ratio",
            "is_foreign_location",
            "is_unverified_user",
            "missing_user_profile",
        ]
        self._train_bootstrap_model()

    def predict(self, enriched_transaction: Dict[str, Any]) -> MLPrediction:
        transaction = enriched_transaction["transaction"]
        features = self.extract_features(enriched_transaction)
        feature_vector = [[features[name] for name in self.feature_names]]
        heuristic_probability = self._heuristic_probability(transaction, features)

        if self.model is not None:
            model_probability = float(self.model.predict_proba(feature_vector)[0][1])
            probability = max(heuristic_probability, model_probability)
        else:
            probability = heuristic_probability

        probability = max(0.0, min(probability, 0.99))
        risk_score = int(round(probability * 100))
        logger.info(
            f"ML PREDICTION | transaction_id={transaction.transaction_id} | "
            f"probability={probability:.4f} | risk_score={risk_score}"
        )
        return MLPrediction(
            fraud_probability=probability,
            risk_score=risk_score,
            model_name=self.model_name,
            model_version=self.model_version,
            features=features,
        )

    def extract_features(self, enriched_transaction: Dict[str, Any]) -> Dict[str, float]:
        transaction: Transaction = enriched_transaction["transaction"]
        user_profile = enriched_transaction.get("user_profile") or {}
        user_history = enriched_transaction.get("user_history") or []
        recent_transaction_count = float(len(user_history))
        recent_total_amount = float(sum(item.get("amount", 0.0) for item in user_history))
        user_risk_score = float(user_profile.get("risk_score", 0.0))
        average_amount = float(user_profile.get("avg_transaction_amount") or 0.0)
        amount_to_average_ratio = transaction.amount / average_amount if average_amount > 0 else 1.0
        is_foreign_location = float(self._is_foreign_location(transaction, user_profile))
        is_unverified_user = 1.0 if user_profile and not user_profile.get("verified", False) else 0.0
        missing_user_profile = 0.0 if user_profile else 1.0

        return {
            "amount": float(transaction.amount),
            "user_risk_score": user_risk_score,
            "recent_transaction_count": recent_transaction_count,
            "recent_total_amount": recent_total_amount,
            "amount_to_average_ratio": float(amount_to_average_ratio),
            "is_foreign_location": is_foreign_location,
            "is_unverified_user": is_unverified_user,
            "missing_user_profile": missing_user_profile,
        }

    def is_fraud(self, prediction: MLPrediction) -> bool:
        return prediction.fraud_probability >= self.threshold

    def _train_bootstrap_model(self) -> None:
        if RandomForestClassifier is None:
            logger.warning("scikit-learn is not installed. Using built-in ML fraud scoring.")
            return

        x_train, y_train = self._training_data()
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        )
        self.model.fit(x_train, y_train)
        logger.info(f"Loaded {self.model_name} version {self.model_version}")

    def _training_data(self) -> Tuple[List[List[float]], List[int]]:
        normal = [
            [45, 5, 1, 45, 0.8, 0, 0, 0],
            [80, 10, 2, 130, 1.1, 0, 0, 0],
            [120, 15, 2, 240, 1.2, 0, 0, 0],
            [250, 20, 3, 500, 1.4, 0, 0, 0],
            [500, 25, 4, 1200, 1.7, 0, 0, 0],
            [900, 35, 5, 2500, 2.1, 0, 0, 0],
            [1500, 45, 6, 4800, 2.5, 0, 1, 0],
            [2200, 10, 0, 0, 1.0, 0, 0, 1],
        ]
        fraud = [
            [3800, 0, 0, 0, 1.0, 0, 0, 1],
            [4800, 0, 0, 0, 1.0, 0, 0, 1],
            [6500, 70, 8, 18000, 5.5, 1, 1, 0],
            [9000, 80, 9, 26000, 7.0, 1, 1, 0],
            [12000, 85, 10, 32000, 8.5, 0, 1, 0],
            [17000, 90, 12, 48000, 10.0, 1, 1, 0],
            [25000, 95, 15, 76000, 15.0, 1, 1, 0],
            [4000, 92, 14, 30000, 6.5, 1, 1, 0],
            [11000, 60, 7, 22000, 9.0, 1, 0, 0],
        ]
        return normal + fraud, [0] * len(normal) + [1] * len(fraud)

    def _heuristic_probability(self, transaction: Transaction, features: Dict[str, float]) -> float:
        amount_score = self._sigmoid((transaction.amount - 2500.0) / 1400.0) * 0.48
        risk_score = min(features["user_risk_score"] / 100.0, 1.0) * 0.18
        count_score = min(features["recent_transaction_count"] / 12.0, 1.0) * 0.10
        velocity_score = min(features["recent_total_amount"] / 25000.0, 1.0) * 0.10
        ratio_score = min(max(features["amount_to_average_ratio"] - 1.0, 0.0) / 8.0, 1.0) * 0.08
        location_score = 0.08 if features["is_foreign_location"] else 0.0
        verification_score = 0.05 if features["is_unverified_user"] else 0.0
        missing_profile_score = 0.12 if features["missing_user_profile"] else 0.0
        return amount_score + risk_score + count_score + velocity_score + ratio_score + location_score + verification_score + missing_profile_score

    def _sigmoid(self, value: float) -> float:
        return 1.0 / (1.0 + exp(-value))

    def _is_foreign_location(self, transaction: Transaction, user_profile: Dict[str, Any]) -> bool:
        user_country = str(user_profile.get("country", "")).strip().upper()
        if not user_country:
            return False
        transaction_country = transaction.location.split(",")[-1].strip().upper()
        return bool(transaction_country and not transaction_country.startswith(user_country[:2]))
