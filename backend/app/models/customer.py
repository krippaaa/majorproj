from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)

    # Basic Details
    full_name = Column(String(100), nullable=False)
    citizenship_no = Column(String(50), unique=True)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(255))

    # AI Features
    age = Column(Integer)
    gender = Column(String(20))
    province = Column(String(50))
    district = Column(String(100))
    education_level = Column(String(100))
    occupation = Column(String(100))
    employment_type = Column(String(100))

    monthly_income_npr = Column(Float)
    monthly_expenses_npr = Column(Float)
    savings_npr = Column(Float)
    existing_loan_amount_npr = Column(Float)
    loan_duration_months = Column(Integer)

    total_assets_npr = Column(Float)
    total_liabilities_npr = Column(Float)
    debt_to_income_ratio = Column(Float)
    collateral_value_npr = Column(Float)
    net_worth_npr = Column(Float)

    credit_score = Column(Integer)
    previous_loans = Column(Integer)
    previous_default = Column(String(10))
    late_payments = Column(Integer)
    repayment_history = Column(String(50))
    credit_utilization = Column(Float)
    credit_inquiries = Column(Integer)
    active_loan_accounts = Column(Integer)

    monthly_transaction_count = Column(Integer)
    average_transaction_amount_npr = Column(Float)
    cash_deposit_frequency = Column(Integer)
    cash_withdrawal_frequency = Column(Integer)

    digital_banking_usage = Column(String(50))
    mobile_banking_usage = Column(String(20))
    atm_usage = Column(Integer)
    average_monthly_balance = Column(Float)

    spending_pattern = Column(String(50))
    merchant_transaction_count = Column(Integer)

    monthly_remittance_npr = Column(Float)

    insurance_status = Column(String(50))
    insurance_premium_npr = Column(Float)

    utility_bill_payment_score = Column(Float)

    mobile_wallet_usage = Column(String(50))
    cooperative_membership = Column(String(20))
    digital_payment_frequency = Column(Integer)

    institution = Column(String(150))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loans = relationship("LoanApplication", back_populates="customer")