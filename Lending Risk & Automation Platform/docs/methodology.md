# Risk Modeling Methodology

## Model Objective
The goal is to predict the likelihood of a loan "Default" (Status: Charged Off or Late) to automate the approval process.

## Feature Engineering
- **Categorical Encoding**: Label encoding used for Grade, Term, and Employment Length.
- **Normalization**: Numerical fields like income and loan amount are cast to high-precision floats.
- **Derived Metrics**: Loan-to-Income ratio introduced to capture relative debt burden.

## Models Evaluated
1. **Logistic Regression**: Used as an interpretable baseline.
2. **Random Forest**: Captures non-linear relationships.
3. **XGBoost**: Selected as the primary model for production due to superior handling of imbalanced datasets and performance.

## Handling Class Imbalance
We utilize `scale_pos_weight` in XGBoost and `class_weight='balanced'` in other models to ensure the minority "Default" class is prioritized.

## Evaluation
- **Primary Metric**: AUC-ROC (measures separation between default and non-default).
- **Secondary Metric**: Precision-Recall (critical for lending profit/loss).
- **Explainability**: SHAP (Shapley Additive Explanations) values used to rank feature importance.
