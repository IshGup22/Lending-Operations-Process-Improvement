# UAT plan and operational risk register

## UAT test cases (proposed)

| ID | Scenario | Expected outcome | Priority |
|---|---|---|---|
| UAT-01 | Missing mandatory income document | Flag missing item; allow resubmission | Critical |
| UAT-02 | Formatting difference in source-system identifier | Normalize and pass if same ID | High |
| UAT-03 | Genuine source identifier mismatch | Route for correction with traceable reason | Critical |
| UAT-04 | Probable duplicate submission | Flag and link to earlier case; do not auto-delete | High |
| UAT-05 | Correct complete application | No false stop; continue standard review | Critical |
| UAT-06 | Authorized override of ambiguous mismatch | Capture analyst ID, time, justification | Critical |
| UAT-07 | Role without override permission | Deny override; keep case available for escalation | High |
| UAT-08 | Dashboard filtered by one team and month | Aggregates reconcile with the case-level query | High |
| UAT-09 | Empty filter result | Show zeros rather than invalid rates | Medium |
| UAT-10 | Validation service unavailable | Fall back to defined manual review pathway | Critical |

**Important:** The above are design-stage UAT scenarios. No claim is made that a production product passed them. `tests/test_pipeline.py` separately contains executable tests for this repository's data pipeline.

## Risk register

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Valid cases incorrectly blocked | Medium | High | Rule-specific overrides, holdout comparison and false-positive review | Credit risk |
| Excessive new exception volume | Medium | Medium | Monitor total touch time, not only prevented errors | Operations |
| Incorrect source matching | Medium | High | Normalization tests, versioned matching rules | Technology |
| Unclear ownership of new SOP | Medium | Medium | Named business owner and sign-off | Operations |
| Overstated benefit forecast | High | Medium | Publish scenario assumptions and sensitivity ranges | Finance |
| Release affects processing continuity | Low | High | Feature flag, rollback and manual fallback | Technology |

## Definition of done

- All critical UAT cases passed in an actual future pilot.
- Operating procedures approved and walkthrough completed with relevant staff.
- KPI logic reconciled to source records and reporting owner identified.
- Benefit estimate updated with *observed* pilot measurements, not assumptions alone.
