-- Focus improvement effort where there is both preventable rework and SLA exposure.
SELECT segment, root_cause,
       COUNT(*) AS exception_cases,
       ROUND(AVG(processing_hours), 1) AS average_processing_hours,
       ROUND(100.0*SUM(sla_breached)/COUNT(*),1) AS sla_breach_pct,
       ROUND(SUM(review_minutes)/60.0, 1) AS review_hours
FROM cases
WHERE exception_flag = 1
GROUP BY segment, root_cause
ORDER BY review_hours DESC;
