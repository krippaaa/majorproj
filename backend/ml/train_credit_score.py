import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# Paths
# ==========================================

BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "Nepal_Credit_Risk_Synthetic_Dataset_With_Names.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# Load Dataset
# ==========================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Total rows:", len(df))


# ==========================================
# Remove rows without Credit Score
# ==========================================

df = df.dropna(subset=["Credit_Score"]).copy()

print("Rows used for training:", len(df))


# ==========================================
# Target
# ==========================================

y = df["Credit_Score"]


# ==========================================
# Remove target + irrelevant columns
# ==========================================

drop_columns = [
    "Credit_Score",
    "Risk_Category",
    "Customer_ID",
    "First_Name",
    "Last_Name",
    "Full_Name"
]

X = df.drop(columns=drop_columns)


# ==========================================
# Identify feature types
# ==========================================

numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()


print("Numeric features:", len(numeric_features))
print("Categorical features:", len(categorical_features))


# ==========================================
# Preprocessing
# ==========================================

numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    )
])


categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="most_frequent")
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])


preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_pipeline,
        numeric_features
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_features
    )
])


# ==========================================
# Model
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)


pipeline = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        model
    )
])


# ==========================================
# Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training model...")


# ==========================================
# Train
# ==========================================

pipeline.fit(
    X_train,
    y_train
)


# ==========================================
# Evaluate
# ==========================================

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n==============================")
print("CREDIT SCORE MODEL RESULTS")
print("==============================")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 4))


# ==========================================
# Save Model
# ==========================================

model_path = os.path.join(
    MODEL_DIR,
    "credit_score_model.pkl"
)

joblib.dump(
    pipeline,
    model_path
)


print("\nModel saved to:")
print(model_path)