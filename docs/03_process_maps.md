# As-is and to-be workflows

These are **proposed** operating models based on a synthetic case study, not observed internal bank processes.

## As-is: exception identified after intake

```mermaid
flowchart LR
 A[Receive case] --> B[Queue for analyst review]
 B --> C{Documents and IDs valid?}
 C -- Yes --> D[Complete review]
 C -- No --> E[Request correction]
 E --> F[Wait for resubmission]
 F --> B
 D --> G[Close case and record KPI]
```

**Failure modes:** manual detection occurs late; repeat hand-offs; duplicated checking; inconsistent reasons for return.

## To-be: controls before manual queue

```mermaid
flowchart LR
 A[Receive case] --> B[Run upstream validation]
 B --> C{Validation result}
 C -- Pass --> D[Queue for standard review]
 C -- Fixable issue --> E[Return actionable request]
 C -- Ambiguous --> F[Analyst exception queue]
 F --> G{Override approved?}
 G -- Yes --> D
 G -- No --> E
 E --> H[Correct and resubmit]
 H --> B
 D --> I[Log outcome and KPI]
```

**Controls:** validation rule ownership, exception code, override reasons, timestamped decisions, audit trail and a fallback manual route.

## Implementation stages

1. Baseline measurement and root-cause validation with Operations and Credit.
2. Requirements sign-off, rule design, and data quality check with Technology.
3. UAT including negative scenarios and false-positive handling.
4. Limited pilot, weekly management reporting, and benefit validation.
5. Training and knowledge transfer to end users; SOP approval before scaled rollout.

## RACI (suggested)

| Activity | Operations | Credit risk | Technology | Finance |
|---|---|---|---|---|
| Define pain points | A/R | C | C | C |
| Approve controls | R | A | C | I |
| Implement validation | C | C | A/R | I |
| Conduct UAT | A/R | R | R | I |
| Validate benefit model | C | I | C | A/R |
| Rollout and knowledge transfer | A/R | C | R | I |

A = Accountable, R = Responsible, C = Consulted, I = Informed. These assignments are proposed, not confirmed organizational roles.
