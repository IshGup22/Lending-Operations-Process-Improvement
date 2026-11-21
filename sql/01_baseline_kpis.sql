-- Baseline operating measures. Run on cases imported from data/synthetic_loan_operations.csv.
SELECT
  COUNT(*) AS cases,
  SUM(exception_flag) AS exceptions,
  ROUND(100.0 * SUM(exception_flag) / COUNT(*), 2) AS exception_rate_pct,
  ROUND(100.0 * SUM(first_pass_flag) / COUNT(*), 2) AS first_pass_rate_pct,
  ROUND(100.0 * SUM(sla_breached) / COUNT(*), 2) AS sla_breach_rate_pct,
  ROUND(SUM(review_minutes) / 60.0, 1) AS review_hours
FROM cases;
