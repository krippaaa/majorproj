from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.db import SessionLocal
from app.models.customer import Customer
from app.models.loan_application import LoanApplication
from app.models.prediction import Prediction
from app.core.permissions import admin_required

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def dashboard_summary(
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    total_customers = db.query(Customer).count()

    total_loans = db.query(LoanApplication).count()

    approved_loans = db.query(LoanApplication).filter(
        LoanApplication.status == "Approved"
    ).count()

    pending_loans = db.query(LoanApplication).filter(
        LoanApplication.status == "Pending"
    ).count()

    rejected_loans = db.query(LoanApplication).filter(
        LoanApplication.status == "Rejected"
    ).count()

    risk_counts = (
        db.query(
            Prediction.risk_category,
            func.count(Prediction.prediction_id)
        )
        .group_by(Prediction.risk_category)
        .all()
    )

    risk_summary = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for risk, count in risk_counts:
        risk_summary[risk] = count

    return {
        "total_customers": total_customers,
        "total_loans": total_loans,
        "approved_loans": approved_loans,
        "pending_loans": pending_loans,
        "rejected_loans": rejected_loans,
        "risk_summary": risk_summary
    }