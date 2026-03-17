-- Analytics Queries for Lending Risk Platform

-- 1. Default rate by loan grade
SELECT 
    grade, 
    COUNT(*) as total_loans,
    SUM(CASE WHEN loan_status IN ('Charged Off', 'Late (31-120 days)') THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as default_rate
FROM loan_applications
GROUP BY grade
ORDER BY grade;

-- 2. Average risk score by loan purpose
SELECT 
    l.purpose, 
    AVG(r.risk_score) as avg_risk_score,
    COUNT(*) as volume
FROM loan_applications l
JOIN risk_scores r ON l.id = r.loan_id
GROUP BY l.purpose
ORDER BY avg_risk_score DESC;

-- 3. Monthly loan volume and approval rate
SELECT 
    issue_d, 
    COUNT(*) as total_volume,
    SUM(CASE WHEN r.decision_flag = 'APPROVE' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as approval_rate
FROM loan_applications l
JOIN risk_scores r ON l.id = r.loan_id
GROUP BY issue_d
ORDER BY issue_d;
