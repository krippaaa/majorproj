from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    loan_id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))

    loan_amount = Column(Float, nullable=False)

    loan_purpose = Column(String(255))

    loan_term = Column(Integer)

    annual_income = Column(Float)

    employment_status = Column(String(100))

    credit_score = Column(Integer)

    status = Column(String(50), default="Pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="loans")