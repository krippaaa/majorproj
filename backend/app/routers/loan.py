from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.loan_application import LoanApplication
from app.schemas.loan_application import (
    LoanCreate,
    LoanUpdate,
    LoanResponse
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Loan
@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    new_loan = LoanApplication(**loan.model_dump())

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan


# Get All Loans
@router.get("/", response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    return db.query(LoanApplication).all()


# Get One Loan
@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan


# Update Loan
@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    updated_loan: LoanUpdate,
    db: Session = Depends(get_db)
):
    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    for key, value in updated_loan.model_dump().items():
        setattr(loan, key, value)

    db.commit()
    db.refresh(loan)

    return loan


# Delete Loan
@router.delete("/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    db.delete(loan)
    db.commit()

    return {
        "message": "Loan deleted successfully"
    }