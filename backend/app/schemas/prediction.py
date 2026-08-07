from pydantic import BaseModel


class PredictionRequest(BaseModel):
    loan_id: int
    customer_data: dict


class PredictionResponse(BaseModel):
    risk_category: str
    confidence: float