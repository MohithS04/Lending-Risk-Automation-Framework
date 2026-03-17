import polars as pl
from typing import List, Dict, Any
from src.etl.base_classes import Transformer

class LoanTransformer(Transformer):
    def transform(self, data: List[Dict[str, Any]]) -> pl.DataFrame:
        if not data:
            return pl.DataFrame()

        df = pl.DataFrame(data)

        # Basic Transformations
        df = df.with_columns([
            pl.col("loan_amount").cast(pl.Float64),
            pl.col("int_rate").cast(pl.Float64),
            pl.col("annual_inc").cast(pl.Float64),
            pl.col("dti").cast(pl.Float64),
            pl.col("updated_at").str.to_datetime(),
        ])

        # Fill missing values
        df = df.fill_null(0.0)

        # Derived Fields: Loan-to-Income (simulating LTV logic with income)
        df = df.with_columns([
            (pl.col("loan_amount") / pl.col("annual_inc")).alias("loan_to_income_ratio")
        ])

        # Standardize categories (Example)
        df = df.with_columns([
            pl.col("grade").str.to_uppercase()
        ])

        return df
