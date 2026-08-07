from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerBase(BaseModel):

    # Basic Details
    full_name: str
    citizenship_no: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    # AI Features
    age: int
    gender: str
    province: str
    district: str
    education_level: str
    occupation: str
    employment_type: str

    monthly_income_npr: float
    monthly_expenses_npr: float
    savings_npr: float
    existing_loan_amount_npr: float
    loan_duration_months: int

    total_assets_npr: float
    total_liabilities_npr: float
    debt_to_income_ratio: float
    collateral_value_npr: float
    net_worth_npr: float

    credit_score: int
    previous_loans: int
    previous_default: str
    late_payments: int
    repayment_history: str
    credit_utilization: float
    credit_inquiries: int
    active_loan_accounts: int

    monthly_transaction_count: int
    average_transaction_amount_npr: float
    cash_deposit_frequency: int
    cash_withdrawal_frequency: int

    digital_banking_usage: str
    mobile_banking_usage: str
    atm_usage: int
    average_monthly_balance: float

    spending_pattern: str
    merchant_transaction_count: int

    monthly_remittance_npr: float

    insurance_status: str
    insurance_premium_npr: float

    utility_bill_payment_score: float

    mobile_wallet_usage: str
    cooperative_membership: str
    digital_payment_frequency: int

    institution: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True