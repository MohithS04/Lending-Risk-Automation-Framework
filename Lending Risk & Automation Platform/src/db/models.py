from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from src.db.database import Base
from datetime import datetime

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(String, primary_key=True)
    loan_amount = Column(Float)
    term = Column(String)
    int_rate = Column(Float)
    installment = Column(Float)
    grade = Column(String)
    sub_grade = Column(String)
    emp_length = Column(String)
    home_ownership = Column(String)
    annual_inc = Column(Float)
    verification_status = Column(String)
    issue_d = Column(String)
    loan_status = Column(String)
    purpose = Column(String)
    dti = Column(Float)
    updated_at = Column(DateTime)

class CreditProfile(Base):
    __tablename__ = "credit_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(String, ForeignKey("loan_applications.id"))
    dti = Column(Float)
    annual_inc = Column(Float)

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(String, ForeignKey("loan_applications.id"))
    risk_score = Column(Float)
    decision_flag = Column(String)  # APPROVE/REJECT
    model_version = Column(String)

class PipelineAuditLog(Base):
    __tablename__ = "pipeline_audit_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_timestamp = Column(DateTime, default=datetime.utcnow)
    rows_processed = Column(Integer)
    module = Column(String)
    status = Column(String)
