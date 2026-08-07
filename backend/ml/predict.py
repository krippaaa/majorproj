import os
import joblib
import pandas as pd


# -----------------------------
# Load Saved Models
# -----------------------------

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(
    os.path.join(BASE_DIR, "models", "best_model.pkl")
)

preprocessor = joblib.load(
    os.path.join(BASE_DIR, "models", "preprocessor.pkl")
)

label_encoder = joblib.load(
    os.path.join(BASE_DIR, "models", "label_encoder.pkl")
)


# -----------------------------
# Prediction Function
# -----------------------------

def predict_risk(customer_data: dict):

    customer = pd.DataFrame([customer_data])

    print("\n====================")
    print(customer)
    print("====================")
    print(customer.dtypes)
    print("====================")

    processed_customer = preprocessor.transform(customer)

    prediction = model.predict(processed_customer)

    probabilities = model.predict_proba(processed_customer)

    risk_category = label_encoder.inverse_transform(prediction)[0]

    confidence = float(round(float(max(probabilities[0])) * 100, 2))

    return {
    "risk_category": str(risk_category),
    "confidence": float(confidence)
    } 
    