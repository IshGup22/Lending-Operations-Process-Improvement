-- Monthly performance, segmented by business area for leadership reporting.
SELECT SUBSTR(created_date,1,7) AS month, segment,
       COUNT(*) AS cases,
       ROUND(100.0*SUM(exception_flag)/COUNT(*),2) AS exception_rate_pct,
       ROUND(100.0*SUM(sla_breached)/COUNT(*),2) AS sla_breach_pct,
       ROUND(AVG(processing_hours),1) AS avg_processing_hours
FROM cases
GROUP BY SUBSTR(created_date,1,7),segment
ORDER BY month,segment;
