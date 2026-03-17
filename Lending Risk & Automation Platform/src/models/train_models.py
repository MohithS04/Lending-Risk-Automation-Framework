import os
import glob
import pandas as pd
import polars as pl
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score
from src.models.feature_engineering import RiskFeatureEngineer

def load_data(processed_dir: str):
    files = glob.glob(os.path.join(processed_dir, "**/*.parquet"), recursive=True)
    dfs = [pl.read_parquet(f).to_pandas() for f in files]
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def baseline_heuristic(df: pd.DataFrame):
    """Simple baseline: Default if DTI > 35 or Int Rate > 20%"""
    predictions = (df["dti"] > 35) | (df["int_rate"] > 20)
    return predictions.astype(int)

def train():
    df = load_data("data/processed")
    if df.empty:
        print("No processed data found. Run ETL first.")
        return

    fe = RiskFeatureEngineer()
    processed_df = fe.engineer_features(df)
    
    X = processed_df.drop(columns=["is_default"])
    y = processed_df["is_default"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Baseline
    y_pred_baseline = baseline_heuristic(X_test)
    print("Baseline Heuristic Report:")
    print(classification_report(y_test, y_pred_baseline))

    # Models
    models = {
        "LogisticRegression": LogisticRegression(class_weight='balanced', max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=100, class_weight='balanced'),
        "XGBoost": XGBClassifier(scale_pos_weight=(len(y_train)-sum(y_train))/sum(y_train))
    }

    results = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        results[name] = auc
        print(f"{name} AUC: {auc:.4f}")
        print(classification_report(y_test, y_pred))

        # Save model
        joblib.dump(model, f"models/{name.lower()}_model.joblib")
    
    joblib.dump(fe, "models/feature_engineer.joblib")
    print("Models and feature engineer saved to models/")

if __name__ == "__main__":
    train()
