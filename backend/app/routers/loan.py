from fastapi import APIRouter, Depends, HTTPException
import json
import urllib.request
from datetime import datetime
import json
import urllib.request
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.loan_application import LoanApplication
from app.models.customer import Customer
from app.models.prediction import Prediction
from app.core.permissions import admin_required


from app.schemas.loan_application import (
    LoanCreate,
    LoanUpdate,
    LoanStatusUpdate,
    LoanResponse
)

from ml.predict import predict_risk


def send_loan_to_blockchain(loan, customer, risk_category, confidence):
    payload = {
        "loanId": str(loan.loan_id),
        "customerId": str(loan.customer_id),
        "customerName": customer.full_name,
        "amount": str(loan.loan_amount),
        "loanPurpose": loan.loan_purpose or "",
        "riskLevel": risk_category,
        "confidence": str(confidence),
        "status": loan.status or "Pending",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        "http://localhost:4000/api/blockchain/loans",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ==================================================
# CREATE LOAN + AI RISK PREDICTION
# ==================================================
@router.post("/", response_model=LoanResponse)
def create_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db)
):

    try:

        # Check customer exists
        customer = db.query(Customer).filter(
            Customer.customer_id == loan.customer_id
        ).first()


        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )


        # -----------------------------
        # Prepare ML Input
        # -----------------------------
        customer_data = {

            "Age": customer.age,
            "Gender": customer.gender,
            "Province": customer.province,
            "District": customer.district,
            "Education_Level": customer.education_level,
            "Occupation": customer.occupation,
            "Employment_Type": customer.employment_type,

            "Monthly_Income_NPR": customer.monthly_income_npr,
            "Monthly_Expenses_NPR": customer.monthly_expenses_npr,
            "Savings_NPR": customer.savings_npr,

            "Existing_Loan_Amount_NPR": customer.existing_loan_amount_npr,
            "Loan_Duration_Months": customer.loan_duration_months,

            "Total_Assets_NPR": customer.total_assets_npr,
            "Total_Liabilities_NPR": customer.total_liabilities_npr,

            "Debt_to_Income_Ratio": customer.debt_to_income_ratio,
            "Collateral_Value_NPR": customer.collateral_value_npr,
            "Net_Worth_NPR": customer.net_worth_npr,

            "Credit_Score": customer.credit_score,

            "Previous_Loans": customer.previous_loans,
            "Previous_Default": customer.previous_default,
            "Late_Payments": customer.late_payments,

            "Repayment_History": customer.repayment_history,
            "Credit_Utilization": customer.credit_utilization,
            "Credit_Inquiries": customer.credit_inquiries,

            "Active_Loan_Accounts": customer.active_loan_accounts,

            "Monthly_Transaction_Count": customer.monthly_transaction_count,
            "Average_Transaction_Amount_NPR": customer.average_transaction_amount_npr,

            "Cash_Deposit_Frequency": customer.cash_deposit_frequency,
            "Cash_Withdrawal_Frequency": customer.cash_withdrawal_frequency,

            "Digital_Banking_Usage": customer.digital_banking_usage,
            "Mobile_Banking_Usage": customer.mobile_banking_usage,
            "ATM_Usage": customer.atm_usage,

            "Average_Monthly_Balance": customer.average_monthly_balance,

            "Spending_Pattern": customer.spending_pattern,
            "Merchant_Transaction_Count": customer.merchant_transaction_count,

            "Monthly_Remittance_NPR": customer.monthly_remittance_npr,

            "Insurance_Status": customer.insurance_status,
            "Insurance_Premium_NPR": customer.insurance_premium_npr,

            "Utility_Bill_Payment_Score": customer.utility_bill_payment_score,

            "Mobile_Wallet_Usage": customer.mobile_wallet_usage,

            "Cooperative_Membership": customer.cooperative_membership,

            "Digital_Payment_Frequency": customer.digital_payment_frequency,

            "Institution": customer.institution,
        }



        # -----------------------------
        # AI Prediction
        # -----------------------------
        prediction_result = predict_risk(customer_data)


        risk_category = str(
            prediction_result["risk_category"]
        )


        # IMPORTANT FIX
        confidence = float(
            prediction_result["confidence"]
        )



        # -----------------------------
        # Save Loan
        # -----------------------------
        new_loan = LoanApplication(
            **loan.model_dump()
        )


        db.add(new_loan)
        db.flush()



        # -----------------------------
        # Save Prediction
        # -----------------------------
        prediction = Prediction(

            loan_id=new_loan.loan_id,

            risk_category=risk_category,

            confidence=confidence,

            model_name="Logistic Regression"
        )


        db.add(prediction)

        # -----------------------------
        # Save Loan to Hyperledger Fabric
        # -----------------------------
        try:
            send_loan_to_blockchain(
                new_loan,
                customer,
                risk_category,
                confidence
            )
        except Exception as blockchain_error:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Blockchain transaction failed: {blockchain_error}"
            )

        # Commit everything together
        db.commit()

        db.refresh(new_loan)

        return {
         "customer_id": new_loan.customer_id,
         "loan_amount": new_loan.loan_amount,
         "loan_purpose": new_loan.loan_purpose,
         "loan_term": new_loan.loan_term,
         "annual_income": new_loan.annual_income,
         "employment_status": new_loan.employment_status,
         "credit_score": new_loan.credit_score,
         "loan_id": new_loan.loan_id,
         "status": new_loan.status,
         "customer_name": customer.full_name,
         "risk_category": risk_category,
         "confidence": confidence
     }
       


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




# ==================================================
# GET ALL LOANS
# ==================================================

@router.get("/", response_model=list[dict])
def get_loans(
    db: Session = Depends(get_db)
):
    loans = db.query(LoanApplication).all()

    result = []

    for loan in loans:

        prediction = (
            db.query(Prediction)
            .filter(Prediction.loan_id == loan.loan_id)
            .first()
        )

        customer = (
            db.query(Customer)
            .filter(Customer.customer_id == loan.customer_id)
            .first()
        )

        result.append({
            "loan_id": loan.loan_id,
            "customer_id": loan.customer_id,
            "customer_name": customer.full_name if customer else "-",
            "loan_amount": loan.loan_amount,
            "loan_purpose": loan.loan_purpose,
            "loan_term": loan.loan_term,
            "status": loan.status,
            "risk_category": prediction.risk_category if prediction else "-",
            "confidence": prediction.confidence if prediction else 0
        })

    return result


# ==================================================
# GET LOAN BY ID
# ==================================================
@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()


    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )


    return loan




# ==================================================
# UPDATE LOAN
# ==================================================
@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    updated_loan: LoanUpdate,
    db: Session = Depends(get_db)
):

    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()


    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )


    for key, value in updated_loan.model_dump().items():

        setattr(
            loan,
            key,
            value
        )


    db.commit()
    db.refresh(loan)


    return loan




# ==================================================
# DELETE LOAN
# ==================================================
@router.delete("/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()


    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )


    db.delete(loan)

    db.commit()


    return {
        "message": "Loan deleted successfully"
    }

@router.put("/{loan_id}/status")
def update_loan_status(
    loan_id: int,
    status_data: LoanStatusUpdate,
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    loan = db.query(LoanApplication).filter(
        LoanApplication.loan_id == loan_id
    ).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    loan.status = status_data.status

    db.commit()
    db.refresh(loan)

    return {
        "message": "Loan status updated successfully",
        "loan": loan
    }