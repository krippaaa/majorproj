from fastapi import FastAPI

from app.database.db import engine, Base

from app.routers import loan

from app.models.role import Role
from app.models.user import User
from app.models.customer import Customer
from app.models.loan_application import LoanApplication
from app.routers import auth
from app.routers import customer

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blockchain and AI Powered Credit Risk Assessment in Nepal Using Big Data",
    version="1.0.0"
)

app.include_router(customer.router)


app.include_router(loan.router)
app.include_router(customer.router)
app.include_router(loan.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": "Backend Connected Successfully!"
    }
