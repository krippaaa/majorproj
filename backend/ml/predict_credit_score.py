import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "credit_score_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_credit_score(customer_data: dict):

    customer = pd.DataFrame([customer_data])

    predicted_score = model.predict(customer)[0]

    # Keep score within normal credit-score range
    predicted_score = max(
        300,
        min(850, predicted_score)
    )

    return round(float(predicted_score), 2)


