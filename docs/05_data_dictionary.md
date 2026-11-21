# Data dictionary and KPI definitions

All records are generated programmatically with a fixed random seed. No identifiers in this repository represent actual borrowers or customers.

| Field | Type | Meaning |
|---|---|---|
| case_id | text | Unique fake ID, `CASE-000001` style |
| created_date | date | Simulated intake date in 2026 |
| segment | category | Retail, SME, Auto, Mortgage |
| team | category | Fictional operations team |
| amount_cad | number | Synthetic amount, not used in benefit calculations |
| risk_tier | category | Synthetic case complexity descriptor, not a credit approval decision |
| exception_flag | 0/1 | Whether the case required intervention |
| root_cause | category | Exception cause or `None` |
| first_pass_flag | 0/1 | Exactly one when `exception_flag=0` |
| rework_flag | 0/1 | Whether exception introduced further rework |
| processing_hours | number | End-to-end elapsed processing hours |
| sla_hours | number | 24 hours for Retail/Auto, 36 hours for SME/Mortgage (synthetic business rules) |
| sla_breached | 0/1 | Whether `processing_hours > sla_hours` |
| review_minutes | number | Manual review effort for the case |
| status | category | Resolved / Open (synthetic) |

## Measures

- **Exception rate** = flagged cases / all cases.
- **First-pass yield** = cases without exception / all cases.
- **SLA breach rate** = cases exceeding the synthetic SLA / all cases.
- **Review effort (hours)** = sum of `review_minutes` / 60.
- **Eligible exceptions** = flagged cases with cause in {missing documentation, source mismatch, duplicate submission}.
- **Scenario prevented cases** = eligible exceptions × assumed prevention rate.
- **Modeled review hours saved** = scenario prevented cases × assumed avoided review minutes / 60.
- **Modeled total review-effort reduction** = modeled review hours saved / baseline manual review hours.

The scenario deliberately does **not** translate reduced review effort into a guaranteed SLA or financial cost impact.
