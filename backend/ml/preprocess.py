import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder


def preprocess_data():

    # -----------------------------
    # Load Dataset
    # -----------------------------
    dataset_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "dataset",
        "Nepal_Credit_Risk_Synthetic_Dataset_With_Names.csv"
    )

    df = pd.read_csv(dataset_path)

    print("Dataset Loaded Successfully")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # -----------------------------
    # Drop unnecessary columns
    # -----------------------------
    drop_columns = [
        "Customer_ID",
        "First_Name",
        "Last_Name",
        "Full_Name"
    ]

    existing_drop = [c for c in drop_columns if c in df.columns]

    X = df.drop(
        columns=existing_drop + ["Risk_Category"]
    )

    # -----------------------------
    # Encode Target Labels
    # -----------------------------
    label_encoder = LabelEncoder()

    y = label_encoder.fit_transform(
        df["Risk_Category"]
    )

    print("\nRisk Classes:")
    print(label_encoder.classes_)


    # -----------------------------
    # Identify feature types
    # -----------------------------
    numeric_features = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    print(f"\nNumeric Features : {len(numeric_features)}")
    print(f"Categorical Features : {len(categorical_features)}")


    # -----------------------------
    # Numerical Pipeline
    # -----------------------------
    numeric_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ])


    # -----------------------------
    # Categorical Pipeline
    # -----------------------------
    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )
    ])


    # -----------------------------
    # Combine Pipelines
    # -----------------------------
    preprocessor = ColumnTransformer([
        (
            "num",
            numeric_pipeline,
            numeric_features
        ),
        (
            "cat",
            categorical_pipeline,
            categorical_features
        )
    ])


    # -----------------------------
    # Train Test Split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )


    # -----------------------------
    # Fit & Transform
    # -----------------------------
    X_train = preprocessor.fit_transform(
        X_train
    )

    X_test = preprocessor.transform(
        X_test
    )


    # -----------------------------
    # Save Models Folder
    # -----------------------------
    model_folder = os.path.join(
        os.path.dirname(__file__),
        "models"
    )

    os.makedirs(
        model_folder,
        exist_ok=True
    )


    # -----------------------------
    # Save Preprocessor & Encoder
    # -----------------------------
    joblib.dump(
        preprocessor,
        os.path.join(
            model_folder,
            "preprocessor.pkl"
        )
    )

    joblib.dump(
        label_encoder,
        os.path.join(
            model_folder,
            "label_encoder.pkl"
        )
    )


    print("\nPreprocessor Saved Successfully")
    print("Label Encoder Saved Successfully")


    return X_train, X_test, y_train, y_test



if __name__ == "__main__":
    preprocess_data()