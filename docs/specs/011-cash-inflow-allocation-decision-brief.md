# 011 Cash Inflow Allocation Decision Brief

**Status:** Draft - Slices A-C implemented; Slice D next
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
- **REQ-CIB-011 - Must:** Maintain a synthetic golden-case fixture set that covers materially different household shapes and names the validation purpose for each fixture.
- **REQ-CIB-012 - Must:** Validate every golden case against cash conservation, allocation capacity limits, required alternatives, scenario coverage, and expected strategy differentiation.
- **REQ-CIB-013 - Must:** Run deterministic property sweeps across synthetic edge cases for inflow size, liquidity state, debt availability, employer-match capacity, tax room, and goal need.
- **REQ-CIB-014 - Must:** Store reviewer annotations as structured records with reviewer role, target case, target strategy when applicable, category, severity, trace IDs, note, and disposition.
- **REQ-CIB-015 - Must:** Reject malformed reviewer annotations and treat unresolved high-severity annotations as blockers for pilot readiness, not as calculation failures.
- **REQ-CIB-016 - Should:** Report validation results as evidence for reviewer and product learning without representing the harness as proof of personalized financial-advice quality.
- **REQ-CIB-017 - Must:** Render a household-readable artifact from the retained `DecisionBrief` without adding, removing, or recalculating allocation values.
- **REQ-CIB-018 - Must:** Render a reviewer-readable record from the same `DecisionBrief`, including the input snapshot, assumptions, validation evidence, reviewer annotations, and trace IDs.
- **REQ-CIB-019 - Must:** Present alternatives in a comparable table with common metrics and no selected winner, ranking, or single-plan call to action.
- **REQ-CIB-020 - Must:** Provide a synthetic manual-entry interface for the required decision-contract inputs, including supported debt rows.
- **REQ-CIB-021 - Must:** Reject invalid manual-entry submissions with field-level errors and without producing a decision brief.
- **REQ-CIB-022 - Must:** Show the synthetic-only, estimate-only, no-execution, and no-personalized-advice safety boundary in the household artifact, reviewer record, and manual-entry interface.
- **REQ-CIB-023 - Should:** Export household and reviewer artifacts as Markdown and HTML from the same rendering context.

## Slice B Validation Harness

Slice B makes the deterministic core reviewable. It does not expand the product into real-household data, professional advice, jurisdiction eligibility, or recommendation ranking.

### Golden-Case Fixture Set

The fixture suite must include at least the following synthetic household shapes:

- Bonus with high-cost debt, employer match, tax room, and a meaningful near-term goal.
- No supported debt.
- Underfunded emergency reserve.
- Already-funded emergency reserve.
- Employer match capacity capped below the inflow.
- Tax-advantaged contribution room exhausted.
- Near-term goal need larger than the inflow.
- Oversized inflow that exceeds all modeled category caps.

Each fixture states its case identifier, validation purpose, household input snapshot, expected strategy leaders where appropriate, and any reviewer annotations used as review evidence.

### Validation Evidence

The validation harness checks:

- Required seven alternatives plus the transparent baseline.
- Exact inflow reconciliation for every plan.
- Capacity compliance for each category and each debt balance.
- Scenario coverage and consistent scenario names across alternatives.
- Expected metric differentiation where the fixture makes that expectation meaningful, such as liquidity, interest avoided, tax value, or goal funding.
- Reviewer annotation shape, traceability, and unresolved-blocker status.

Property sweeps are deterministic grids, not randomized fuzzing. They are meant to catch invariant breaks across edge cases without introducing nondeterministic tests.

### Reviewer Annotation Defaults

Reviewer annotations are structured product and risk review records, not calculation inputs. The initial categories are `assumption`, `risk`, `usefulness`, `compliance`, and `calculation`. The initial severities are `low`, `medium`, `high`, and `blocker`. The initial dispositions are `open`, `accepted`, `deferred`, and `resolved`.

Open `high` or `blocker` annotations block pilot readiness. They do not make the deterministic calculation invalid unless the annotation identifies a calculation defect.

### Decisions and Nuances

- Golden cases prove the engine is internally consistent for representative synthetic cases; they do not prove a plan is financially appropriate for a real household.
- Property sweeps assert invariants and capacity boundaries; they do not assert that one alternative is universally better than another.
- Strategy-leader expectations should be used only when the fixture is designed to make that leader unambiguous.
- Reviewer annotations should capture why a human reviewer trusts, questions, or rejects a brief, while preserving the deterministic output unchanged.
- The first harness uses in-repo synthetic fixtures. Real data, account exports, or private household details remain out of scope.

## Slice C Decision-Brief Interface

Slice C packages the deterministic output for review and demonstration. It still accepts synthetic manually entered data only and must preserve the same comparison-first posture.

### Household Artifact

The household-readable artifact must include:

- Case identifier and generated calculation boundary.
- Plain-language safety disclosure.
- The transparent baseline and seven alternatives.
- A comparable allocation and metric table.
- Assumptions and scenario summaries.
- Trade-off statements for each alternative.

It must not label any alternative as recommended, optimal, best, or selected.

### Reviewer Record

The reviewer-readable record must include everything in the household artifact plus:

- Full input snapshot and supported debt rows.
- Validation status, pilot-readiness status, validation issues, and blocker annotations when supplied.
- Reviewer annotations with role, category, severity, disposition, strategy, note, and trace IDs.
- Spec trace IDs for the rendering requirements.

Reviewer records are evidence packages for product/risk review. They are not household-facing advice letters.

### Manual-Entry Interface

The initial manual-entry interface may be local and dependency-free. It must:

- Capture required fields for one synthetic household case.
- Accept supported debts as explicit rows or a documented row format.
- Return field-level errors for invalid values.
- Generate the household and reviewer views from the deterministic engine when valid.
- Keep the safety boundary visible before and after submission.

### Interface Decisions and Nuances

- Markdown and HTML exports are both useful: Markdown is reviewable in git; HTML is easier for product demos.
- The interface should optimize comparison and traceability over visual flourish.
- Manual-entry data remains synthetic even when a user types realistic-looking numbers.
- Rendering code must not become a second calculation engine.

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

| ID | Covers | Criterion |
|---|---|---|
| AC-CIB-001 | REQ-CIB-001, REQ-CIB-008 | Non-synthetic input and invalid case data are rejected. |
| AC-CIB-002 | REQ-CIB-002 | Seven alternatives and one baseline are produced for a valid synthetic case. |
| AC-CIB-003 | REQ-CIB-003, REQ-CIB-004 | Every plan conserves the inflow and satisfies every configured capacity constraint. |
| AC-CIB-004 | REQ-CIB-005, REQ-CIB-006 | Every alternative contains four scenario impacts and at least one trade-off statement. |
| AC-CIB-005 | REQ-CIB-005, REQ-CIB-012 | At least one synthetic golden case demonstrates materially different liquidity, debt, tax, and goal outcomes across alternatives. |
| AC-CIB-006 | REQ-CIB-011, REQ-CIB-012 | The golden-case suite covers the required household shapes and passes the validation harness. |
| AC-CIB-007 | REQ-CIB-013 | Deterministic property sweeps verify cash conservation, category caps, debt caps, and scenario coverage across synthetic edge cases. |
| AC-CIB-008 | REQ-CIB-014, REQ-CIB-015 | Reviewer annotations validate required fields, trace IDs, target references, and pilot-readiness blocker status. |
| AC-CIB-009 | REQ-CIB-007, REQ-CIB-016 | Validation output is labeled as synthetic evidence and is not represented as financial-advice quality proof. |
| AC-CIB-010 | REQ-CIB-017, REQ-CIB-019, REQ-CIB-022 | The household artifact includes the baseline, all seven alternatives, common metrics, assumptions, scenario summaries, and safety disclosure without selecting a winner. |
| AC-CIB-011 | REQ-CIB-018, REQ-CIB-022 | The reviewer record includes input snapshot, validation evidence, reviewer annotations, trace IDs, and safety disclosure from the same calculation output. |
| AC-CIB-012 | REQ-CIB-020, REQ-CIB-021 | The manual-entry interface accepts valid synthetic inputs, parses supported debt rows, and rejects invalid submissions with errors. |
| AC-CIB-013 | REQ-CIB-023 | Markdown and HTML exports are generated from the same rendering context and preserve calculation values. |

## Delivery Slices

1. **Slice A - Deterministic core:** data contract, seven alternatives, baseline, comparison metrics, stress records, synthetic demo, and unit tests.
2. **Slice B - Validation harness:** golden cases, deterministic property tests for cash conservation and caps, structured reviewer annotations, validation evidence records, and traceable acceptance-test names.
3. **Slice C - Decision-brief interface:** manual-entry form, comparable alternative table, assumption disclosure, and exportable artifact.
4. **Slice D - Governed pilot readiness:** jurisdiction coverage matrix, policy configuration, audit record, privacy/security review, and human review workflow.
