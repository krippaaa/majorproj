from sqlalchemy.orm import Session

from ml.predict import predict_risk
from app.models.prediction import Prediction


class RiskService:

    @staticmethod
    def predict(
        loan_id: int,
        customer_data: dict,
        db: Session
    ):

        # ML Prediction
        result = predict_risk(customer_data)

        # Save Prediction
        prediction = Prediction(
            loan_id=loan_id,
            risk_category=result["risk_category"],
            confidence=result["confidence"],
            model_name="Logistic Regression"
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return result