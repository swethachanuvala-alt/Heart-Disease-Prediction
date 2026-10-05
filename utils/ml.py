"""
Pure machine-learning helpers (no Streamlit imports, so `train_model.py` can reuse them).

Pipeline mirrors notebook GGST_8.ipynb
    drop the 25 unused columns  ->  LabelEncode Gender (Female=0, Male=1)
    -> 80/20 stratified split (random_state=42)  -> StandardScaler (fit on train)
    -> tuned Logistic Regression (C=0.1, solver='liblinear', max_iter=2000)

The classes are already perfectly balanced (50/50) in this dataset, so SMOTE in the
notebook leaves the training data unchanged — it is therefore not needed here.
"""
from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "heart_disease_dataset.csv"
MODEL_PATH = ROOT / "model" / "logistic_regression_model.pkl"
SCALER_PATH = ROOT / "model" / "scaler.pkl"

# Same column order as the notebook after dropping the unused columns
FEATURES = ["Age", "Gender", "BMI", "Smoking", "Alcohol", "PhysicalActivity", "DietScore",
            "SleepHours", "StressLevel", "FamilyHistory", "Diabetes", "Hypertension",
            "KidneyDisease", "StrokeHistory", "RestingHR", "HDL", "LDL", "ChestPainType",
            "ExerciseAngina"]
TARGET = "HeartDisease"
GENDER_CODE = {"Female": 0, "Male": 1}          # LabelEncoder sorts alphabetically
NICE = {
    "Age": "Age", "Gender": "Sex", "BMI": "BMI", "Smoking": "Smoking", "Alcohol": "Alcohol",
    "PhysicalActivity": "Physical activity", "DietScore": "Diet score", "SleepHours": "Sleep hours",
    "StressLevel": "Stress level", "FamilyHistory": "Family history", "Diabetes": "Diabetes",
    "Hypertension": "Hypertension", "KidneyDisease": "Kidney disease", "StrokeHistory": "Stroke history",
    "RestingHR": "Resting heart rate", "HDL": "HDL cholesterol", "LDL": "LDL cholesterol",
    "ChestPainType": "Chest-pain type", "ExerciseAngina": "Exercise angina",
}
BEST_PARAMS = dict(C=0.1, solver="liblinear", max_iter=2000, random_state=42)


# --------------------------------------------------------------------------- data
def load_dataset(path: Path = DATA_PATH, encode: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path)
    if encode:
        df["Gender"] = df["Gender"].map(GENDER_CODE)
    return df


def split_data(df: pd.DataFrame):
    d = df.copy()
    if d["Gender"].dtype == object or str(d["Gender"].dtype).startswith("str"):
        d["Gender"] = d["Gender"].map(GENDER_CODE)
    X, y = d[FEATURES], d[TARGET]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# --------------------------------------------------------------------------- training
def fit_pipeline(df: pd.DataFrame):
    X_train, _, y_train, _ = split_data(df)
    scaler = StandardScaler().fit(X_train)
    model = LogisticRegression(**BEST_PARAMS).fit(scaler.transform(X_train), y_train)
    return scaler, model


def save_artifacts(scaler, model) -> None:
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(model, MODEL_PATH)


def load_or_train(df: pd.DataFrame | None = None):
    """Load saved .pkl files; if missing/incompatible quietly re-train. Returns (scaler, model, source)."""
    df = load_dataset() if df is None else df
    try:
        scaler = joblib.load(SCALER_PATH)
        model = joblib.load(MODEL_PATH)
        probe = df.iloc[[0]].copy()
        probe["Gender"] = probe["Gender"].map(GENDER_CODE)
        model.predict_proba(scaler.transform(probe[FEATURES]))
        return scaler, model, "saved"
    except Exception:
        scaler, model = fit_pipeline(df)
        return scaler, model, "retrained"


# --------------------------------------------------------------------------- inference
def _row(person: dict) -> pd.DataFrame:
    p = dict(person)
    if isinstance(p["Gender"], str):
        p["Gender"] = GENDER_CODE[p["Gender"]]
    return pd.DataFrame([p])[FEATURES]


def predict_one(scaler, model, person: dict):
    """Return (risk probability, per-feature log-odds contribution, intercept)."""
    scaled = scaler.transform(_row(person))
    prob = float(model.predict_proba(scaled)[0, 1])
    contrib = dict(zip(FEATURES, (model.coef_[0] * scaled[0]).tolist()))
    return prob, contrib, float(model.intercept_[0])


def predict_many(scaler, model, frame: pd.DataFrame) -> np.ndarray:
    f = frame.copy()
    if f["Gender"].dtype == object or str(f["Gender"].dtype).startswith("str"):
        f["Gender"] = f["Gender"].map(GENDER_CODE)
    return model.predict_proba(scaler.transform(f[FEATURES]))[:, 1]


# --------------------------------------------------------------------------- evaluation
def evaluate(scaler, model, df: pd.DataFrame) -> dict:
    _, X_test, _, y_test = split_data(df)
    prob = model.predict_proba(scaler.transform(X_test))[:, 1]
    pred = (prob >= 0.5).astype(int)
    fpr, tpr, _ = roc_curve(y_test, prob)
    return {"accuracy": accuracy_score(y_test, pred), "precision": precision_score(y_test, pred),
            "recall": recall_score(y_test, pred), "f1": f1_score(y_test, pred),
            "roc_auc": roc_auc_score(y_test, prob), "cm": confusion_matrix(y_test, pred),
            "fpr": fpr, "tpr": tpr, "n_test": len(y_test)}


def coefficient_table(model) -> pd.DataFrame:
    t = pd.DataFrame({"feature": FEATURES, "coef": model.coef_[0]})
    t["label"] = t["feature"].map(NICE)
    t["abs"] = t["coef"].abs()
    return t.sort_values("abs", ascending=False).reset_index(drop=True)
