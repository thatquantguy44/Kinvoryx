# 001 Product Foundation

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 0-2  
**Related specs:** [002](002-household-state-and-data-model.md), [004](004-capital-allocation-optimizer.md), [007](007-validation-and-market-research.md)

## Purpose

Define the product boundary, users, jobs, first beachhead, phase gates, and approval criteria for the Household Capital Allocation Optimizer.

## Product Thesis

Households do not have separate money, calendar, career, and family problems. They have one constrained resource-allocation problem observed through different applications.

The initial product solves the household's next-dollar allocation problem. It creates a defensible decision artifact that compares feasible alternatives under explicit assumptions and uncertainty.

## Target Beachhead

The initial beachhead is financially sophisticated but operationally underserved U.S. households:

- Ages approximately 28-50.
- Household income roughly $150,000-$500,000.
- Multiple account types, debts, benefits, or near-term goals.
- At least one complicating factor such as variable compensation, equity compensation, student debt, childcare, home purchase, self-employment, or competing savings goals.
- Too complex for a simple calculator but below, or unwilling to pay for, traditional private wealth support.

## Users and Buyers

| Role | Job | Success Evidence |
|---|---|---|
| Household user | Understand the best next use of money and trade-offs | Completes first decision artifact and can explain recommendation assumptions |
| Couple or multi-adult household | Resolve preference conflicts and approve material actions | Separate preferences and approvals are captured |
| Financial planner or RIA | Produce reviewable client decision cases without repetitive rekeying | Reduced preparation time and fewer manual handoffs |
| CPA or tax planner | Review tax-sensitive recommendations inside explicit scope | Supported calculations and unresolved tax questions are clear |
| Employer or benefits platform | Improve employee financial decisions without exposing private household data | Privacy-preserving pilot with useful decision artifacts |
| Platform/API buyer | Embed governed decision modules | Reproducible API outputs with traceable evidence |

## Scope

### Phase 1 In Scope

- U.S. household use cases.
- Cash, taxable investments, retirement accounts, HSA, 529, common consumer debts, emergency reserves, and user-defined goals.
- Employer-match logic and configurable contribution limits.
- Supported federal/state tax estimates only where the reviewed coverage matrix allows.
- Single-period prioritization and multi-period scenarios.
- Manual entry and file import before production-grade account connectivity.
- Individual and two-adult household modeling.
- Recommendations, alternatives, constraint diagnostics, action checklists, approvals, and professional review.
- Research sandbox using synthetic households.

### Phase 1 Out of Scope

- Custody, money movement, trade execution, tax filing, legal/tax/medical/insurance/fiduciary representation.
- Individual-security selection or return prediction.
- Autonomous borrowing, refinancing, benefits elections, or account opening.
- International tax or non-U.S. regulatory coverage.
- LLM-authored authoritative calculations or eligibility conclusions.

## Phases and Gates

| Phase | Deliverable | Required Gate |
|---:|---|---|
| 0 | Discovery interviews, competitive audit, TAM v1, regulatory issue map, clickable decision artifact | GATE-M1 and GATE-M2 pass |
| 1 | Manual-input research prototype with baseline, allocation alternatives, scenarios, explanations, and decision record | All Phase 1 Must requirements pass |
| 2 | Controlled human pilot with secure onboarding, consent, human review, paid/budget-backed evidence | GATE-M3 and GATE-M4 pass |
| 3 | Professional/employer distribution with org governance, role-based review, batch monitoring | GATE-M5 passes |
| 4-6 | Financial extensions, cross-domain decisions, household operating system | Extension gates pass per module |

## Product Requirements

- **REQ-PROD-001 — Must:** The first approved pilot shall name one beachhead, trigger event, buyer, pricing hypothesis, and primary job to be done.
- **REQ-PROD-002 — Must:** Product copy, interface labels, and proposal language shall distinguish decision support from execution, tax filing, legal advice, or fiduciary representation.
- **REQ-PROD-003 — Must:** The product shall present at least one transparent baseline beside any optimized recommendation.
- **REQ-PROD-004 — Must:** All material recommendations shall remain conditional on stated assumptions, supported jurisdictions, available data, and approval state.
- **REQ-PROD-005 — Must:** Unsupported or incomplete cases shall produce a qualified result, safe refusal, sensitivity range, or review route.
- **REQ-PROD-006 — Should:** The product shall support both direct household and professional-review workflows without changing the underlying recommendation record.
- **REQ-PROD-007 — Should:** Recurring monitoring value shall be validated before positioning the product as an ongoing subscription.

## Acceptance Criteria

- Maps to overview AC-001 through AC-009, AC-012, AC-014, and AC-015.
- Product/design approval is blocked until every Phase 1 Must requirement has an owner and verification method.
- Pilot launch is blocked until legal/compliance, privacy, security, accessibility, and incident-response reviews are complete.

