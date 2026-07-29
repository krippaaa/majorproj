from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerBase(BaseModel):
    full_name: str
    citizenship_no: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True