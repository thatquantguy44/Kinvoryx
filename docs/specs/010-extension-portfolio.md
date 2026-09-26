# 010 Extension Portfolio

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 4-6  
**Related specs:** [001](001-product-foundation.md), [002](002-household-state-and-data-model.md), [003](003-ai-orchestration-and-audit.md), [007](007-validation-and-market-research.md)

## Purpose

Define how future financial and cross-domain modules are admitted, sequenced, and bounded.

## Admission Requirements

- **REQ-EXT-001 — Must:** A module defines one consequential decision, target user, buyer, trigger event, baseline, and measurable outcome.
- **REQ-EXT-002 — Must:** A module demonstrates incremental value over the capital optimizer or current best alternative.
- **REQ-EXT-003 — Must:** A module specifies minimum additional data required and why each field is necessary.
- **REQ-EXT-004 — Must:** A module defines professional, regulatory, ethical, and autonomy boundaries before pilot.
- **REQ-EXT-005 — Must:** A module preserves household preference conflicts rather than averaging them away.
- **REQ-EXT-006 — Must:** A module includes safe fallback when data, model confidence, or supported jurisdiction is insufficient.
- **REQ-EXT-007 — Should:** A module reuses household state and scenario definitions only where semantic equivalence is verified.

## Candidate Sequence

| Phase | Candidate Modules | Approval Notes |
|---:|---|---|
| 4 | Equity compensation, tax-aware portfolio transition, retirement drawdown, variable income, benefits and total compensation | Each expands financial scope and may increase tax/securities/compliance review |
| 5 | Household resilience, major purchase timing, housing/location, career capital | Must avoid false precision, referral conflicts, bias, and normative overreach |
| 6 | Time and energy, family logistics, goal portfolio, health-supporting routines, household digital twin | Requires strong privacy, fairness, health-boundary, and autonomy controls |

## Module-Specific Requirements

### Housing and Location — Home Sweet Home

[Spec 013](013-home-sweet-home-optimization.md) provides the dedicated housing
extension handoff, with `REQ-HOME-001` through `REQ-HOME-026`. Confirmed scope
includes buying and renting; integrated and standalone modes; detailed optional
education access; additional job access; and town, neighborhood, and street
recommendations leading to address-level comparison. Its ten confirmed regions
are Boston, New York/North Jersey, Washington DC area, Atlanta, Chicago, Austin,
Dallas, Seattle, Los Angeles, and San Francisco.

The module remains a specification draft. Its proposed architecture, backlog,
source leads, and pilot footprints do not establish passed admission requirements
or authorize a real-household pilot. It must satisfy `REQ-EXT-001` through
`REQ-EXT-007`, with the evidence and safe fallback described in Spec 013.

### Life-Event Simulator

- **REQ-LIFE-001 — Must:** Compare at least two named alternatives against no-change baseline.
- **REQ-LIFE-002 — Must:** Display money, time, risk, flexibility, and goal effects separately.
- **REQ-LIFE-003 — Must:** Identify robust conclusions and conclusions that reverse under plausible assumptions.
- **REQ-LIFE-004 — Must:** Avoid normative directives on intimate decisions.

### Time, Energy, and Household Coordination

- **REQ-TIME-001 — Must:** Users define protected time, non-negotiable obligations, recovery constraints, and fairness rules.
- **REQ-TIME-002 — Must:** Quantify schedule fragility and retain buffers.
- **REQ-TIME-003 — Must:** Both affected adults approve recurring responsibility assignments.
- **REQ-TIME-004 — Should:** Predictions expose uncertainty and allow correction.

### Career Capital

- **REQ-CAR-001 — Must:** Comparisons include compensation, benefits, taxes, commute, flexibility, learning, stability, and values.
- **REQ-CAR-002 — Must:** Separate sourced labor-market evidence from inferred future opportunity.
- **REQ-CAR-003 — Must:** Protected characteristics are not used to reduce recommendations or opportunity estimates.
- **REQ-CAR-004 — Should:** Represent option value and path dependence.

### Health-Supporting Routines

- **REQ-HLT-001 — Must:** Stay non-diagnostic and non-treatment unless regulated workflow and clinical oversight exist.
- **REQ-HLT-002 — Must:** Safety exclusions and escalation guidance are reviewed by qualified experts.
- **REQ-HLT-003 — Must:** Do not optimize engagement, weight, sleep, or exercise in ways that encourage unsafe behavior.

## Acceptance Criteria

- No extension starts implementation until it passes REQ-EXT-001 through REQ-EXT-007.
- Every extension has its own numbered spec before design or engineering begins.
- Extension launch claims are limited to validated decision types, jurisdictions, users, and data coverage.
