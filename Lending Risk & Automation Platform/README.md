# 🏦 Lending Risk & Automation Platform

A production-grade framework for automated lending data ingestion, risk modeling, and financial analytics.

## 🏗️ Architecture
- **Ingetion Layer**: FastAPI Mock API serving loan records + Async Ingestion Engine with exponential backoff and watermarking.
- **ETL Layer**: Modular, configuration-driven pipeline using `Polars` for high-performance transformations.
- **Model Layer**: Predictive risk assessment using XGBoost and Random Forest, with SHAP-based explainability.
- **Data Layer**: Normalized SQLite database using SQLAlchemy ORM for downstream reporting and audit logs.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker (optional)

### Local Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Mock API**:
   ```bash
   python src/ingestion/mock_api.py
   ```

3. **Run ETL & Modeling Pipeline**:
   ```bash
   # In a new terminal
   export PYTHONPATH=$PYTHONPATH:.
   python src/etl/orchestrator.py
   python src/models/train_models.py
   python src/db/db_loader.py
   ```

4. **Run Analytics**:
   ```bash
   sqlite3 lending_platform.db < src/db/analytics.sql
   ```

## 📂 Project Structure
- `src/`: Source code for ingestion, ETL, modeling, and DB.
- `data/`: Raw and processed data storage (partitioned).
- `models/`: Serialized model artifacts.
- `config/`: Pipeline and watermark configurations.
- `docs/`: Detailed data dictionary and methodologies.

## 📊 Documentation
- [Data Dictionary](docs/data_dictionary.md)
- [Methodology](docs/methodology.md)
