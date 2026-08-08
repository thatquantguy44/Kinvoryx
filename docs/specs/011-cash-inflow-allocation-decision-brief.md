# 011 Cash Inflow Allocation Decision Brief

**Status:** Draft - vertical slice in progress
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)
**Primary phases:** 0-1
**Related specs:** [001](001-product-foundation.md), [002](002-household-state-and-data-model.md), [004](004-capital-allocation-optimizer.md), [007](007-validation-and-market-research.md)

## Purpose

Define the first narrow decision artifact for the Household Capital Allocation Optimizer: how a household should compare feasible uses of a discrete cash inflow. The initial discovery trigger is an after-tax annual bonus. The decision model is intentionally reusable for other validated inflows, such as surplus cash, tax refunds, or inheritance proceeds.

This is a decision-support prototype, not a financial plan, tax calculation, execution workflow, or autonomous recommendation engine. The first implementation accepts synthetic, manually entered data only.

## Decision Contract

**Question:** Given a discrete cash inflow, what trade-offs result from allocating it to liquidity, debt, matched retirement savings, other tax-advantaged savings, and a near-term goal?

**Required inputs:**

- Cash inflow amount.
- Monthly essential expenses and current liquid reserve.
- Supported debt balances and annual interest rates.
- Employer-match contribution capacity and match rate.
- Available tax-advantaged contribution room and disclosed estimated tax rate.
- Near-term goal funding need.
- Supported jurisdiction and all material assumptions.

**Required output:** A decision brief with a transparent baseline and seven comparable allocation alternatives. Each alternative reconciles the entire inflow, respects caps, reports common metrics, identifies its principal trade-off, and includes the same deterministic stress set.

## Scope and Safety Boundary

### In Scope

- Synthetic U.S. household cases.
- A discrete, post-tax cash inflow.
- Emergency reserve, debt principal reduction, employer-match contribution, tax-advantaged savings, near-term goal funding, and retained cash.
- Fixed, visible assumptions and deterministic calculations.
- Alternative comparison, not a single authoritative recommendation.

### Out of Scope

- Real household data, account connectivity, money movement, trading, or benefits elections.
- Individual security selection, return prediction, tax filing, legal advice, or eligibility conclusions.
- Unsupported jurisdiction rules, automated contribution-limit retrieval, or LLM-generated calculations.
- A production ranking or recommendation of one alternative as "best."

## Allocation Alternatives

Every brief presents the following alternatives. A strategy can state that an input category is unavailable or already satisfied, but it cannot silently replace it with an unstated assumption.

| ID | Alternative | Allocation priority | Core trade-off |
|---|---|---|---|
| CIB-ALT-01 | Safety first | Emergency reserve, employer match, high-cost debt, tax-advantaged savings, goal | More liquidity; slower debt, tax, and goal progress |
| CIB-ALT-02 | Match and debt first | Employer match, high-cost debt, emergency reserve, tax-advantaged savings, goal | Higher certain value; less immediately accessible cash |
| CIB-ALT-03 | Tax-advantaged first | Employer match, tax-advantaged savings, emergency reserve, high-cost debt, goal | Potential tax value; less flexibility and more rule dependence |
| CIB-ALT-04 | Near-term goal first | Goal, minimum reserve, employer match, high-cost debt, tax-advantaged savings | Greater goal-date confidence; deferred resilience and long-term value |
| CIB-ALT-05 | Balanced allocation | Spread feasible allocation across reserve, match, high-cost debt, tax-advantaged savings, and goal | Progress on several outcomes; no single outcome is maximized |
| CIB-ALT-06 | Resilience | Emergency reserve to a higher target, then employer match, high-cost debt, tax-advantaged savings, goal | Strongest shock absorption; lowest near-term acceleration elsewhere |
| CIB-ALT-07 | Debt acceleration | All supported debt, employer match, emergency reserve, tax-advantaged savings, goal | Faster deleveraging; can leave household exposed to cash shocks |

## Common Comparison Fields

The brief presents the following for every alternative under the same assumptions:

- Inflow reconciliation by allocation category and total retained cash.
- Liquid reserve amount and months of essential expenses covered.
- Estimated first-year interest avoided, labeled as an estimate rather than a payoff quote.
- Employer-match contribution and estimated match captured.
- Tax-advantaged contribution amount and estimated tax value, labeled with the supplied tax-rate assumption.
- Near-term goal funding and remaining goal need.
- Remaining supported debt balance.
- Principal risks, deferred outcomes, and binding capacity limits.
- The same scenario impacts for job loss, unexpected expense, market decline, and goal-cost increase.

## Functional Requirements

- **REQ-CIB-001 - Must:** Accept the required decision-contract inputs as typed, validated values with an explicit synthetic-data flag.
- **REQ-CIB-002 - Must:** Produce all seven allocation alternatives and a transparent waterfall baseline from the same input snapshot.
- **REQ-CIB-003 - Must:** Reconcile each plan so allocated categories plus retained cash equal the cash inflow exactly.
- **REQ-CIB-004 - Must:** Never allocate more than a debt balance, employer-match capacity, tax-advantaged room, or near-term goal need.
- **REQ-CIB-005 - Must:** Report the common comparison fields for each alternative, including an explicit deferred outcome or principal trade-off.
- **REQ-CIB-006 - Must:** Apply the same deterministic stress set to every alternative and retain the scenario assumptions with the result.
- **REQ-CIB-007 - Must:** Label all tax, return, and scenario values as assumptions or estimates. The prototype shall not select or present a single plan as personalized advice.
- **REQ-CIB-008 - Must:** Reject a non-synthetic case in the vertical slice and reject invalid monetary, debt, or expense inputs.
- **REQ-CIB-009 - Should:** Support an explicit risk-reviewer override of the default high-cost-debt threshold and reserve targets in a future governed configuration layer.
- **REQ-CIB-010 - Should:** Render the same result as a household-readable brief and a reviewer-readable record without changing the underlying calculations.

## Deterministic Prototype Assumptions

The vertical slice uses configuration values that are visible in each result:

- Safety target: three months of essential expenses.
- Resilience target: six months of essential expenses.
- Goal-first minimum reserve: one month of essential expenses.
- High-cost debt threshold: 7% annual interest rate.
- Job-loss stress: three months without income.
- Unexpected-expense stress: one month of essential expenses.
- Market-decline stress: 20% value decrease applied only to the model's long-term contribution exposure.
- Goal-cost stress: 10% increase in remaining goal cost.

These values are prototype defaults, not normative planning rules. They must migrate to governed, versioned configuration before any real-household pilot.

## Output Record

Each generated decision brief retains:

- Case identifier and synthetic-data status.
- Input snapshot and configured thresholds.
- Baseline and alternative allocation rows.
- Debt allocation by debt identifier.
- Metrics, scenario outcomes, and trade-off statements.
- Calculation version and result status.

The output belongs to the deterministic-calculation information class. It must not be represented as authoritative public rules, a household fact, or AI-generated narrative. This traces to [Spec 002](002-household-state-and-data-model.md) `REQ-DATA-001` through `REQ-DATA-004` and [Spec 004](004-capital-allocation-optimizer.md) `REQ-020` through `REQ-045`.

## Acceptance Criteria

- Seven alternatives and one baseline are produced for a valid synthetic case.
- Every plan conserves the inflow and satisfies every configured capacity constraint.
- At least one synthetic golden case demonstrates materially different liquidity, debt, tax, and goal outcomes across the alternatives.
- Every alternative contains four scenario impacts and at least one trade-off statement.
- Non-synthetic input and invalid case data are rejected.
- Tests verify reconciliation, capacity constraints, strategy differentiation, scenario coverage, and the prototype's synthetic-only boundary.

## Delivery Slices

1. **Slice A - Deterministic core:** data contract, seven alternatives, baseline, comparison metrics, stress records, synthetic demo, and unit tests.
2. **Slice B - Validation harness:** golden cases, property tests for cash conservation and caps, and structured reviewer annotations.
3. **Slice C - Decision-brief interface:** manual-entry form, comparable alternative table, assumption disclosure, and exportable artifact.
4. **Slice D - Governed pilot readiness:** jurisdiction coverage matrix, policy configuration, audit record, privacy/security review, and human review workflow.

