import os
import glob
import pandas as pd
import polars as pl
import joblib
from sqlalchemy.orm import Session
from src.db.database import SessionLocal, init_db
from src.db.models import LoanApplication, RiskScore, PipelineAuditLog
from src.models.feature_engineering import RiskFeatureEngineer

def load_processed_data_to_db():
    init_db()
    db: Session = SessionLocal()
    
    # 1. Load Processed Parquet Files
    files = glob.glob("data/processed/**/*.parquet", recursive=True)
    if not files:
        print("No processed files found.")
        return

    dfs = [pl.read_parquet(f).to_pandas() for f in files]
    df = pd.concat(dfs, ignore_index=True)
    
    # 2. Get Model to generate Risk Scores
    model_path = "models/xgboost_model.joblib"
    fe_path = "models/feature_engineer.joblib"
    
    if os.path.exists(model_path) and os.path.exists(fe_path):
        model = joblib.load(model_path)
        fe = joblib.load(fe_path)
        
        X = fe.engineer_features(df, training=False)
        if "is_default" in X.columns:
            X = X.drop(columns=["is_default"])
        
        # Risk score (0-1000) based on probability of default
        probs = model.predict_proba(X)[:, 1]
        df["risk_score"] = (1 - probs) * 1000
        df["decision_flag"] = df["risk_score"].apply(lambda s: "APPROVE" if s > 600 else "REJECT")
    else:
        df["risk_score"] = 0.0
        df["decision_flag"] = "N/A"

    # 3. Insert into DB (Batch)
    # Using pandas.to_sql for simplicity in this stage
    from src.db.database import engine
    
    # Mapping columns to match LoanApplication table
    loan_cols = [
        "id", "loan_amount", "term", "int_rate", "installment", 
        "grade", "sub_grade", "emp_length", "home_ownership", 
        "annual_inc", "verification_status", "issue_d", 
        "loan_status", "purpose", "dti", "updated_at"
    ]
    df[loan_cols].to_sql("loan_applications", con=engine, if_exists="append", index=False)
    
    # Risk scores table
    risk_df = df[["id", "risk_score", "decision_flag"]].copy()
    risk_df.columns = ["loan_id", "risk_score", "decision_flag"]
    risk_df["model_version"] = "xgboost_v1.0"
    risk_df.to_sql("risk_scores", con=engine, if_exists="append", index=False)
    
    # Audit log
    audit = PipelineAuditLog(rows_processed=len(df), module="db_loader", status="SUCCESS")
    db.add(audit)
    db.commit()
    
    print(f"Successfully loaded {len(df)} records into the database.")
    db.close()

if __name__ == "__main__":
    load_processed_data_to_db()
