# Data Dictionary - Lending Risk Platform

| Field | Source | Data Type | Definition | Transformation |
|---|---|---|---|---|
| `id` | API | String | Unique loan application identifier | None |
| `loan_amount` | API | Float | Requested loan amount | Cast to Float64 |
| `int_rate` | API | Float | Interest rate applied to the loan | Cast to Float64 |
| `grade` | API | String | LendingClub assigned loan grade (A-G) | Uppercased |
| `annual_inc` | API | Float | Self-reported annual income | Cast to Float64 |
| `dti` | API | Float | Debt-to-income ratio | Cast to Float64 |
| `loan_to_income_ratio` | Derived | Float | Ratio of loan amount to annual income | `loan_amount / annual_inc` |
| `risk_score` | Model | Float | Probability of repayment (0-1000) | `(1 - prob_default) * 1000` |
| `decision_flag` | Model | String | Automated decision (APPROVE/REJECT) | `APPROVE` if score > 600 |
| `updated_at` | API | DateTime | Timestamp of the last record update | String to DateTime |
