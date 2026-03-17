import pandas as pd
import polars as pl
from sklearn.preprocessing import LabelEncoder

class RiskFeatureEngineer:
    def __init__(self):
        self.label_encoders = {}
        self.categorical_cols = ["term", "grade", "emp_length", "home_ownership", "verification_status", "purpose"]

    def engineer_features(self, df: pd.DataFrame, training: bool = True) -> pd.DataFrame:
        """
        Processes raw lending data into features suitable for ML models.
        """
        processed_df = df.copy()

        # Handle Target Variable: 'loan_status' -> 'is_default'
        # Classes: 'Current', 'Fully Paid', 'Charged Off', 'Late (31-120 days)'
        if "loan_status" in processed_df.columns:
            processed_df["is_default"] = processed_df["loan_status"].apply(
                lambda x: 1 if x in ["Charged Off", "Late (31-120 days)"] else 0
            )

        # Derived Features (already partially done in ETL, but ensuring consistency)
        processed_df["loan_to_income"] = processed_df["loan_amount"] / (processed_df["annual_inc"] + 1)
        
        # Encoding Categorical Variables
        for col in self.categorical_cols:
            if col in processed_df.columns:
                if training:
                    le = LabelEncoder()
                    processed_df[col] = le.fit_transform(processed_df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    le = self.label_encoders.get(col)
                    if le:
                        processed_df[col] = le.transform(processed_df[col].astype(str))

        # Select Features
        features = [
            "loan_amount", "int_rate", "installment", "annual_inc", 
            "dti", "loan_to_income"
        ] + self.categorical_cols
        
        if "is_default" in processed_df.columns:
            return processed_df[features + ["is_default"]]
        return processed_df[features]

if __name__ == "__main__":
    # Test with a dummy sample
    data = {
        "loan_amount": [1000, 5000], "annual_inc": [50000, 100000], 
        "int_rate": [10, 15], "dti": [20, 10], "term": ["36 months", "60 months"],
        "grade": ["A", "B"], "emp_length": ["10+ years", "1 year"],
        "home_ownership": ["RENT", "OWN"], "verification_status": ["Verified", "Not Verified"],
        "purpose": ["debt_consolidation", "credit_card"], "loan_status": ["Current", "Charged Off"],
        "installment": [35, 150]
    }
    df = pd.DataFrame(data)
    fe = RiskFeatureEngineer()
    processed = fe.engineer_features(df)
    print(processed.head())
