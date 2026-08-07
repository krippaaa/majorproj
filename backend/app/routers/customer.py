#Router vaneko gate ho.
#Frontend bata request aauda router le receive garcha.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import admin_required
from app.database.db import SessionLocal
from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Create Customer
# -----------------------------
@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    new_customer = Customer(**customer.model_dump())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# -----------------------------
# Get All Customers
# -----------------------------
@router.get("/", response_model=list[CustomerResponse])
def get_customers(
   
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


# -----------------------------
# Get Single Customer
# -----------------------------
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# -----------------------------
# Update Customer
# -----------------------------
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    updated_customer: CustomerUpdate,
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    for key, value in updated_customer.model_dump().items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


# -----------------------------
# Delete Customer
# -----------------------------
@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    current_user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }