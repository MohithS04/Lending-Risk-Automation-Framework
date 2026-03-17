import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
from src.models.feature_engineering import RiskFeatureEngineer

def explain():
    model = joblib.load("models/xgboost_model.joblib")
    fe = joblib.load("models/feature_engineer.joblib")
    
    # Load some sample data for explanation
    import glob
    import polars as pl
    files = glob.glob("data/processed/**/*.parquet", recursive=True)
    if not files:
        return
    
    sample_df = pl.read_parquet(files[0]).to_pandas().head(100)
    X = fe.engineer_features(sample_df, training=False)
    if "is_default" in X.columns:
        X = X.drop(columns=["is_default"])

    # SHAP Explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # Plot
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    plt.savefig("logs/shap_summary.png")
    print("SHAP summary saved to logs/shap_summary.png")

if __name__ == "__main__":
    explain()
