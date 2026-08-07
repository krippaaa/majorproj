from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import engine, Base

from app.models.role import Role
from app.models.user import User
from app.models.customer import Customer
from app.models.loan_application import LoanApplication
from app.models.prediction import Prediction

from app.routers import auth
from app.routers import customer
from app.routers import loan
from app.routers import prediction
from app.routers import dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blockchain and AI Powered Credit Risk Assessment in Nepal Using Big Data",
    version="1.0.0"
)

# ==========================
# CORS Configuration
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(loan.router)
app.include_router(prediction.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "message": "Backend Connected Successfully!"
    }