from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    citizenship_no = Column(String(50), unique=True)

    phone = Column(String(20))

    email = Column(String(100))

    address = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loans = relationship("LoanApplication", back_populates="customer")