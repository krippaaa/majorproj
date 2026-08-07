from pydantic import BaseModel
from typing import Optional


class LoanBase(BaseModel):
    customer_id: int
    loan_amount: float
    loan_purpose: Optional[str] = None
    loan_term: Optional[int] = None
    annual_income: Optional[float] = None
    employment_status: Optional[str] = None
    credit_score: Optional[int] = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(LoanBase):
    status: Optional[str] = None


class LoanStatusUpdate(BaseModel):
    status: str


class LoanResponse(LoanBase):
    loan_id: int
    status: str

    customer_name: Optional[str] = None

    risk_category: Optional[str] = None
    confidence: Optional[float] = None

    class Config:
        from_attributes = True