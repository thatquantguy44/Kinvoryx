# 004 Capital Allocation Optimizer

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 1-2  
**Related specs:** [002](002-household-state-and-data-model.md), [003](003-ai-orchestration-and-audit.md), [006](006-jurisdiction-intelligence.md), [007](007-validation-and-market-research.md)

## Purpose

Specify the Household Capital Allocation Optimizer: baselines, candidate alternatives, scenarios, constraints, explanations, and research comparisons.

## Decision Contract

Input: a validated household state, supported jurisdiction rules, institutional assumptions, household preferences, and a scenario set.

Output: feasible allocation alternatives that reconcile sources and uses, identify binding constraints, quantify uncertainty, show opportunity cost, and retain a reproducible decision record.

## Required Baselines

- User's current allocation behavior.
- Simple waterfall heuristic: minimum obligations, emergency reserve, employer match, high-cost debt, tax-advantaged savings, taxable goals.
- Equal-priority allocation across goals.
- Deterministic point-estimate optimization.

## Objective Research Backlog

Research must compare:

- Goal-attainment probability subject to liquidity and risk constraints.
- Weighted goal shortfall minimization.
- Expected lifetime utility with user-calibrated risk preferences.
- Robust optimization against adverse but plausible parameter sets.
- Multi-objective optimization producing a Pareto frontier.

No objective family is approved for production until validation confirms feasibility, stability, explanation fidelity, and user/professional comprehension.

## Functional Requirements

- **REQ-020 — Must:** Generate a rules-based baseline using configurable ordering logic.
- **REQ-021 — Must:** Allocate incremental cash across eligible uses while satisfying hard constraints.
- **REQ-022 — Must:** Support a multi-period plan with user-selectable horizon and time step.
- **REQ-023 — Must:** Produce at least three feasible alternatives when meaningful trade-offs exist: recommended, liquidity-preserving, and goal-acceleration variants.
- **REQ-024 — Must:** Report infeasibility and identify minimum conflicting constraint set or equivalent actionable diagnosis.
- **REQ-025 — Must:** Every output reconciles sources and uses of funds.
- **REQ-026 — Should:** Support contribution limits, employer matches, debt minimums, prepayment rules, and configurable penalties.
- **REQ-027 — Should:** Model transaction costs, taxes, lockups, settlement delay, and account restrictions when relevant.
- **REQ-030 — Must:** Support deterministic stresses for income loss, unexpected expense, market decline, inflation, and goal-cost increase.
- **REQ-031 — Must:** Display outcome ranges and scenario failure rates rather than only expected values.
- **REQ-032 — Must:** Distinguish sourced assumptions, model estimates, and subjective judgments.
- **REQ-033 — Should:** Support correlated shocks.
- **REQ-034 — Should:** Compare recommendation with current behavior and baseline across the same scenarios.
- **REQ-035 — Could:** Personalized probabilistic forecasts require calibration, drift, and subgroup-performance measurement.
- **REQ-040 — Must:** Every recommendation states decision, amount, timing, expected benefit, main assumptions, principal risks, and next-best alternative.
- **REQ-041 — Must:** Identify binding constraints and marginal value of relaxing important constraints.
- **REQ-042 — Must:** Show opportunity cost.
- **REQ-043 — Must:** Users can inspect trace from household inputs to constraints, scenarios, and recommendation.
- **REQ-044 — Must:** Generate shareable decision summary.
- **REQ-045 — Should:** Evaluate explanations for fidelity to the decision model.

## Validation Requirements

- Conservation of cash/property-based checks.
- Constraint satisfaction checks.
- Reconciliation of all sources and uses.
- Golden cases reviewed by financial-planning, tax, optimization, security, and compliance specialists.
- Sensitivity and stability tests for small input changes.
- Scenario comparison against transparent heuristics.
- Expert material-error threshold set before testing.

## Rejection Criteria

A candidate optimizer cannot advance if it:

- Produces unstable recommendations under immaterial input changes.
- Cannot explain important drivers faithfully.
- Improves expected wealth by violating unacceptable liquidity or tail-risk constraints.
- Needs unavailable or unreliable inputs to beat a simple heuristic.
- Produces personalization lift too small to justify added sensitive data.
- Degrades systematically for identifiable household segments without fallback.

## Acceptance Criteria

- All supported test cases reconcile funds and satisfy hard constraints.
- Infeasible cases expose the conflict rather than producing a plan.
- Users can compare recommended, baseline, liquidity-preserving, and goal-acceleration alternatives when trade-offs exist.
- Recommendation artifacts include assumptions, risks, outcome ranges, binding constraints, opportunity costs, and alternatives.

