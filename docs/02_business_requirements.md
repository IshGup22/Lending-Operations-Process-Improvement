# Business requirements and acceptance criteria

**Initiative:** Upstream validation & exception-routing pilot  
**Version:** 1.0 (case study)  
**Scope:** Simulated lending-operation case creation, exception triage and KPI monitoring

## Problem statement

Credit and Operations teams receive loan cases with missing documents, mismatched IDs or duplicate entries. These are often found after an analyst has begun review. The proposed future state moves selected rules to the intake step and provides clear override handling.

## Roles and collaboration

| Stakeholder | Primary accountability | Decision or input |
|---|---|---|
| Operations manager | Business owner | Scope, SLA and SOP approval |
| Credit risk lead | Control reviewer | Approval for risk/override rules |
| Finance partner | Benefits validator | Review-effort baseline and scenario assumptions |
| Technology / delivery lead | Solution designer | Feasibility, logging, release and rollback |
| Frontline analyst | End user | Usability, false-positive handling, UAT feedback |

## Functional requirements

| ID | Priority | Requirement | Acceptance test |
|---|---|---|---|
| BR-01 | Must | Flag missing mandatory documents at submission | Missing required doc produces a specific actionable error |
| BR-02 | Must | Match source-system identifiers and distinguish formatting differences | Valid normalized matches pass; true mismatches are flagged |
| BR-03 | Must | Detect probable duplicate applications without automatically deleting records | Duplicates enter review queue with linked case reference |
| BR-04 | Must | Allow authorized analyst to override with reason and audit trail | Override captured with actor, timestamp and reason |
| BR-05 | Must | Track exception volume, cause, first-pass yield, SLA and review time | Aggregate totals reconcile with case register |
| BR-06 | Should | Filter KPIs by segment, team and month | Dashboard totals update with selected filters |
| BR-07 | Should | Export a weekly exception log for operations reviews | Export fields align with approved data dictionary |
| BR-08 | Must | Provide traceable change documentation, UAT and handover notes | Business owner signs off on pilot and updated SOP |

## Non-functional requirements

- **Privacy:** Use synthetic test data in development; role-based access and minimal exposure for any real deployment.
- **Auditability:** Do not destroy rejected/duplicate records; retain exception and override history.
- **Reliability:** Monitoring metrics must reconcile to transactional records.
- **Usability:** Provide plain-language rejection reasons and a manual exception path.
- **Change readiness:** Controlled rollout, rollback procedure, end-user walkthrough, signed SOP.

## Out of scope

- Loan approval/decline decisions, automated credit scoring, changes to legal/regulatory policy.
- Automated account action against real borrowers.
- Claiming observed production savings or deployment to a real bank.
