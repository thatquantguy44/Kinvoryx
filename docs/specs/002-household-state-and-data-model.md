# 002 Household State and Data Model

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 1-2  
**Related specs:** [003](003-ai-orchestration-and-audit.md), [004](004-capital-allocation-optimizer.md), [006](006-jurisdiction-intelligence.md)

## Purpose

Define the household state, data provenance, quality, permissions, and portability requirements required before recommendations can be generated.

## Domain Model

The household state is time-indexed and includes:

- People: household members, dependents, roles, permissions, approval rights.
- Income: recurring, variable, bonus, equity compensation, self-employment, and effective dates.
- Expenses: essential, discretionary, obligations, planned changes.
- Assets: cash, taxable accounts, retirement accounts, HSA, 529, and other supported accounts.
- Liabilities: balances, rates, minimums, terms, prepayment rules, penalties.
- Benefits: employer match, contribution limits, plan constraints, insurance deductibles, benefit elections.
- Goals: amount/outcome, target date, priority, minimum acceptable outcome, flexibility.
- Constraints: hard limits, soft preferences, aspiration targets, household fairness constraints.
- Tax profile: filing assumptions, domicile, residence, work location, income-source jurisdiction, supported rule scope.
- Decision history: recommendations, approvals, overrides, rejected plans, observed outcomes.

## Information Classes

| Class | Examples | Source of Truth |
|---|---|---|
| Authoritative public rules | Tax limits, agency guidance, official forms | Jurisdiction registry |
| Institutional research and policy | Capital-market assumptions, planning rules, review thresholds | Organization configuration |
| Household configuration | Goals, preferences, restrictions, permissions | Household-approved inputs |
| Observed state | Balances, transactions, debt details, payroll data | Imported or user-entered source snapshots |
| AI narrative | Summaries, explanations, drafts | Generated artifact with evidence links |

AI narrative is never promoted into a rule or household fact without governed review or user confirmation.

## Requirements

- **REQ-001 — Must:** Represent household members, dependents, income sources, recurring expenses, liquid reserves, accounts, debts, benefits, tax profile, goals, and constraints with effective dates.
- **REQ-002 — Must:** Distinguish user-entered, imported, inferred, defaulted, stale, and unavailable values.
- **REQ-003 — Must:** Show completeness and freshness before optimization.
- **REQ-004 — Must:** Users can correct, exclude, or override imported or inferred values.
- **REQ-005 — Should:** Two household members can express separate preferences, non-negotiable constraints, and approval rights.
- **REQ-006 — Should:** Support reusable household templates without representing synthetic defaults as user facts.
- **REQ-010 — Must:** Goals include target amount or outcome, target date or horizon, priority, minimum acceptable outcome, and flexibility.
- **REQ-011 — Must:** Hard constraints, soft preferences, and aspiration targets are distinct.
- **REQ-012 — Must:** Users can see how recommendations change when a preference or constraint changes.
- **REQ-013 — Should:** Contradictory goals trigger prioritization instead of silent resolution.
- **REQ-014 — Could:** Learned preference suggestions require user confirmation before material use.
- **REQ-DATA-001 — Must:** Each material field declares information class, source, jurisdiction, effective date, freshness, owner, confidence or validation status, and permitted uses.
- **REQ-DATA-002 — Must:** Apply documented precedence when institutional policy, household configuration, and default assumptions differ.
- **REQ-DATA-003 — Must:** AI-generated narrative is not treated as authoritative data without review or confirmation.
- **REQ-DATA-004 — Must:** Calculations fail safely or disclose bounded assumptions when required authoritative rules or household configuration are absent.

## Non-Functional Requirements

- **NFR-001 — Privacy:** Collect only decision-relevant data; permissions are granular, revocable, and understandable.
- **NFR-002 — Security:** Encrypt sensitive data in transit and at rest; enforce least privilege and auditable admin access.
- **NFR-012 — Portability:** Users can export household inputs, assumptions, goals, and decision history.
- **NFR-013 — Deletion:** Users can request deletion consistent with legal retention requirements.
- **NFR-015 — Household fairness:** Multi-person recommendations expose distribution of cost, time, risk, and flexibility.

## Acceptance Criteria

- Completeness and freshness status is visible before optimization.
- A recommendation cannot proceed when missing, stale, contradictory, or unsupported fields would materially change the decision unless a bounded sensitivity result or review route is used.
- Every field used in a recommendation traces to a retained source snapshot or confirmed user input.
- Export includes inputs, assumptions, goals, and decision history in a usable format.

