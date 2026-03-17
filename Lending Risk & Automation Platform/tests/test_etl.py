import pytest
import polars as pl
from src.etl.transformer import LoanTransformer

def test_transformation_logic():
    mock_data = [
        {
            "id": "1", "loan_amount": 10000, "annual_inc": 50000, 
            "int_rate": 10.5, "dti": 15.0, "grade": "a", 
            "updated_at": "2024-01-01T10:00:00"
        }
    ]
    transformer = LoanTransformer()
    df = transformer.transform(mock_data)
    
    assert df.height == 1
    assert df["loan_to_income_ratio"][0] == 0.2
    assert df["grade"][0] == "A"
    import datetime
    assert isinstance(df["updated_at"][0], datetime.datetime)

def test_empty_transformation():
    transformer = LoanTransformer()
    df = transformer.transform([])
    assert df.is_empty()
