import os
import joblib
import warnings

from preprocess import preprocess_data

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

warnings.filterwarnings("ignore")

# Try importing XGBoost
try:
    from xgboost import XGBClassifier
    xgboost_available = True
except ImportError:
    xgboost_available = False


def train_models():

    print("\nLoading Preprocessed Data...\n")

    X_train, X_test, y_train, y_test = preprocess_data()

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),
    }

    if xgboost_available:
        models["XGBoost"] = XGBClassifier(
            random_state=42,
            eval_metric="mlogloss"
        )

    best_model = None
    best_name = None
    best_score = 0

    print("=" * 60)

    for name, model in models.items():

        print(f"\nTraining {name}...")

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )
        recall = recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )
        f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")

        print("\nClassification Report")
        print(classification_report(y_test, predictions))

        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name

    model_path = os.path.join(
        os.path.dirname(__file__),
        "models",
        "best_model.pkl"
    )

    joblib.dump(best_model, model_path)

    print("\n" + "=" * 60)
    print(f"Best Model : {best_name}")
    print(f"Best F1 Score : {best_score:.4f}")
    print("Model Saved Successfully!")


if __name__ == "__main__":
    train_models()