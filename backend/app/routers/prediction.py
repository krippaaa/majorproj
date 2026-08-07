from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse
)

from app.services.risk_service import RiskService

from app.models.prediction import Prediction
from app.models.loan_application import LoanApplication
from app.models.customer import Customer


router = APIRouter(
    prefix="/prediction",
    tags=["AI Credit Risk Prediction"]
)


@router.post(
    "/predict-risk",
    response_model=PredictionResponse
)
def predict_risk(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        result = RiskService.predict(
            loan_id=request.loan_id,
            customer_data=request.customer_data,
            db=db
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/")
def get_predictions(
    db: Session = Depends(get_db)
):
    predictions = db.query(Prediction).all()

    result = []

    for prediction in predictions:

        loan = (
            db.query(LoanApplication)
            .filter(
                LoanApplication.loan_id == prediction.loan_id
            )
            .first()
        )

        customer = None

        if loan:
            customer = (
                db.query(Customer)
                .filter(
                    Customer.customer_id == loan.customer_id
                )
                .first()
            )

        result.append({
            "prediction_id": prediction.prediction_id,
            "loan_id": prediction.loan_id,
            "customer_name": customer.full_name if customer else "-",
            "risk_category": prediction.risk_category,
            "confidence": prediction.confidence,
            "model_name": prediction.model_name,
            "predicted_at": prediction.predicted_at
        })

    return result