from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, index=True)

    loan_id = Column(
        Integer,
        ForeignKey("loan_applications.loan_id"),
        nullable=False
    )

    risk_category = Column(
        String(50),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    model_name = Column(
        String(100),
        default="Logistic Regression"
    )

    predicted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    loan = relationship(
        "LoanApplication",
        back_populates="predictions"
    )