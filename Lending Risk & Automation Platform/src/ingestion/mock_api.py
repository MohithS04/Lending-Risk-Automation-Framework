import random
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Mock Lending API")

class LoanRecord(BaseModel):
    id: str
    loan_amount: float
    term: str
    int_rate: float
    installment: float
    grade: str
    sub_grade: str
    emp_length: str
    home_ownership: str
    annual_inc: float
    verification_status: str
    issue_d: str
    loan_status: str
    purpose: str
    dti: float
    updated_at: str

def generate_mock_loan(loan_id: int, date_offset: int = 0) -> LoanRecord:
    updated_at = (datetime.now() - timedelta(days=date_offset)).isoformat()
    issue_d = (datetime.now() - timedelta(days=date_offset + 30)).strftime("%b-%Y")
    
    return LoanRecord(
        id=str(loan_id),
        loan_amount=random.uniform(1000, 40000),
        term=random.choice(["36 months", "60 months"]),
        int_rate=random.uniform(5.0, 25.0),
        installment=random.uniform(50, 1500),
        grade=random.choice(["A", "B", "C", "D", "E", "F"]),
        sub_grade=random.choice(["A1", "B2", "C3", "D4"]),
        emp_length=random.choice(["< 1 year", "1 year", "5 years", "10+ years"]),
        home_ownership=random.choice(["RENT", "OWN", "MORTGAGE"]),
        annual_inc=random.uniform(30000, 200000),
        verification_status=random.choice(["Verified", "Source Verified", "Not Verified"]),
        issue_d=issue_d,
        loan_status=random.choice(["Current", "Fully Paid", "Charged Off", "Late (31-120 days)"]),
        purpose=random.choice(["debt_consolidation", "credit_card", "home_improvement", "major_purchase"]),
        dti=random.uniform(0, 40),
        updated_at=updated_at
    )

@app.get("/loans", response_model=List[LoanRecord])
def get_loans(
    since: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Simulates a lending API with incremental extraction support.
    'since' should be an ISO format timestamp.
    """
    loans = []
    # Generate some records based on 'since' or just recent ones
    base_id = 10000
    for i in range(limit):
        loans.append(generate_mock_loan(base_id + i, date_offset=random.randint(0, 5)))
    
    if since:
        since_dt = datetime.fromisoformat(since)
        loans = [l for l in loans if datetime.fromisoformat(l.updated_at) > since_dt]
    
    return loans

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
