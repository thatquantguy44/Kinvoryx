# Household Decision Optimization Differentiators

**Status:** Product and optimization strategy  
**Version:** 0.1  
**Date:** August 8, 2026  
**Related documents:** Household Decision Intelligence Master Product Specification; Competitive Positioning and Defensibility Strategy

## Purpose

This document defines optimization-native capabilities that could distinguish the platform from conventional financial-planning, portfolio-management, and AI-advisor products.

The central product thesis is that the platform should not merely calculate a financial plan. It should construct an adaptive household decision policy:

> What should the household do now, what should it defer, what information should it obtain, and how should its actions change as laws, markets, income, location, preferences, and family circumstances evolve?

These capabilities remain within the platform's core scope because they operate on the same household state, deterministic calculation tools, state-aware rule system, workflow orchestration, and audit graph already required by the product.

## Strategic recommendation

Prioritize the following differentiators:

| Priority | Capability | Strategic contribution |
|---:|---|---|
| 1 | Adaptive household policy optimization | Changes the product from static planning software into a household decision engine |
| 2 | Value-of-information optimization | Makes data collection and conversational workflows materially more intelligent |
| 3 | Binding-constraint and shadow-price analysis | Translates institutional optimization into understandable household guidance |
| 4 | Robustness, regret, and recommendation stability | Prevents brittle recommendations and improves trust |
| 5 | Household decision dependency graph | Connects rules, calculations, monitoring, and auditability |
| 6 | Optionality and irreversibility analysis | Improves decisions with timing, lock-in, or expiring rights |
| 7 | Attention and execution optimization | Optimizes for plans households will actually complete |
| 8 | Multi-objective preference frontier | Personalizes decisions without pretending that one universal objective exists |

## 1. Adaptive household policy optimizer

Most financial-planning systems compare static scenarios or estimate a probability of goal success. The platform should instead generate a conditional policy that specifies how actions change with the household state.

Let the household state at time \(t\) be:

\[
s_t = (\text{income},\text{assets},\text{liabilities},\text{tax attributes},\text{benefits},\text{location},\text{goals},\text{laws},\text{life events})
\]

The desired output is a policy:

\[
\pi^*(s_t)=\text{recommended action given household state }s_t
\]

Example policy rules include:

- Exercise stock options when concentration exceeds a configured limit and projected AMT remains within an approved range.
- Execute a Roth conversion up to a calculated amount unless year-to-date income crosses a specified threshold.
- Refinance only when the probability-weighted benefit exceeds closing costs, the household's hurdle rate, and its expected moving risk.
- Increase accessible liquidity when income volatility or employment risk rises.
- Reevaluate domicile when the multi-year benefit exceeds relocation costs and configured career, family, and lifestyle penalties.

### Required outputs

Each policy should include:

- Recommended action now
- Conditions that would reverse or modify the action
- Validity period
- Relevant deadlines
- Monitoring variables and thresholds
- Recalculation trigger
- Mathematical rationale
- Applicable federal and state rules
- Advisor overrides and approval state

## 2. Household optionality and irreversibility engine

Household actions should be classified by their reversibility and timing characteristics:

- Reversible
- Partially reversible
- Irreversible
- Time-limited
- Path-dependent
- Dependent on another action
- Valuable to delay pending additional information

Examples include option exercise, Social Security claiming, mortgage repayment, relocation, sale of concentrated equity, retirement, pension elections, and changes in employment.

The engine should estimate the value of waiting:

\[
V_{\text{wait}} = \mathbb{E}[V_{\text{future information}}] - \text{cost of delay} - \text{expiration risk}
\]

Possible recommendations are:

- Act now
- Wait until a specified date
- Wait for a defined signal
- Preserve flexibility
- Acquire additional information before acting

## 3. Value-of-information optimizer

The platform should determine which missing information can materially change a decision instead of forcing users or advisors to complete an exhaustive fact-find upfront.

For an uncertain input, calculate the expected value of sample information:

\[
\operatorname{EVSI}=\mathbb{E}[\text{decision value with additional information}]-\text{decision value with current information}
\]

The conversational layer can then prioritize questions, documents, and professional reviews according to decision value.

Example:

> Obtaining the latest private-company valuation is more decision-relevant than refining the household's long-run expected portfolio return because the valuation could change the option-exercise recommendation.

### Product implications

- Progressive rather than exhaustive onboarding
- Ranked list of missing information
- Quantified benefit of resolving uncertainty
- Document requests linked to specific decisions
- Explicit record of how new information changed the recommendation
- Advisor queue ordered by expected decision impact

## 4. Binding-constraint and shadow-price engine

The platform should treat household resources as scarce capacities rather than only balance-sheet fields. Potential constraints include:

- Accessible cash
- Time
- Credit capacity
- Tax-bracket capacity
- Risk capacity
- Household attention
- Geographic flexibility
- Caregiving capacity
- Employer-benefit capacity

For each binding constraint, calculate or approximate the marginal value of relaxing it. This converts a solver diagnostic into planner-grade guidance.

Example explanations include:

- An additional dollar of accessible liquidity is currently more valuable than an additional dollar of retirement contributions.
- The binding constraint is exposure to a two-year income interruption, not insufficient retirement wealth.
- The next unit of tax-bracket capacity should be allocated to a Roth conversion rather than realizing an additional capital gain.

### Required outputs

- Binding and nonbinding constraints
- Marginal value or shadow price
- Range over which the marginal value remains valid
- Recommended method for relaxing the constraint
- Decisions affected by the constraint
- Sensitivity to uncertain inputs

## 5. Multi-objective household decision frontier

There is no universally correct household utility function. The platform should expose tradeoffs rather than silently manufacture preferences.

Potential objectives include:

- Lifetime consumption
- Downside protection
- Liquidity
- Bequest
- Tax efficiency
- Goal attainment
- Career flexibility
- Simplicity
- Family time
- Geographic preference

The deterministic engine should calculate a Pareto frontier. The conversational layer should help the household understand and configure the tradeoffs.

This creates a deliberate division of labor:

- AI elicits, clarifies, and explains preferences.
- Deterministic optimization calculates feasible tradeoffs and recommended actions.
- The audit layer records which preferences and constraints produced the recommendation.

## 6. Recommendation stability, robustness, and regret

A mathematically optimal recommendation may be unsuitable when small changes in assumptions reverse it. Every material recommendation should be tested for stability.

### Required measures

- Sensitivity ranges
- Break-even values
- Probability of recommendation reversal
- Regret from acting under an incorrect assumption
- Regret from waiting
- Robust alternative
- Monitoring thresholds

A minimax-regret formulation may be used when appropriate:

\[
a^*=\arg\min_a\max_{\theta\in\Theta}\left[V(a^*(\theta),\theta)-V(a,\theta)\right]
\]

The user-facing result should distinguish among:

- Mathematically dominant recommendation
- Narrow recommendation sensitive to assumptions
- Robust recommendation with slightly lower expected value
- Decision for which additional information is warranted

## 7. Household decision dependency graph

Household decisions are interdependent. A job change can affect income, vesting, benefits, liquidity requirements, tax capacity, housing, and equity-compensation decisions.

The platform should maintain a computational dependency graph connecting:

- Household facts
- User preferences
- Legal and tax rules
- Deterministic calculations
- Optimization decisions
- Proposed actions
- Monitoring triggers
- Advisor approvals

The graph should answer:

- Which facts and rules produced this recommendation?
- Which other decisions depend on it?
- Which action must occur first?
- What becomes invalid when an input or rule changes?
- Which households are affected by a newly effective law or policy?

An advisor-facing impact analysis could report:

> A state-rule update affected 43 households, invalidated seven recommendations, and materially changed three proposed action plans.

This graph is also the foundation for the platform's audit trail and decision-validity monitoring.

## 8. Household attention and execution optimizer

Theoretical value is not realized when a household fails to complete the recommended actions. The platform should model execution capacity explicitly.

Relevant variables include:

- Number of actions
- Required sequence
- Cognitive difficulty
- Paperwork burden
- Required professionals
- Deadlines
- Emotional resistance
- Estimated completion probability
- Cost of partial or failed execution

Expected realized value can be represented as:

\[
\text{Realized value}=\text{theoretical value}\times P(\text{completion})
\]

The optimizer should be able to recommend a simpler, slightly lower-value action set when it has a materially higher probability of completion.

### Example

> The unconstrained plan produces an estimated $28,000 of value across nine actions. The recommended plan produces $25,000 across three actions and has substantially greater expected realized value.

## Integrated architecture

These capabilities should share a common decision pipeline:

1. Construct the effective-dated household state.
2. Identify feasible actions using federal, state, account, benefit, and user constraints.
3. Determine which missing information could alter the decision.
4. Generate multi-period policies rather than isolated recommendations.
5. Evaluate expected value, optionality, robustness, regret, and execution probability.
6. Calculate binding constraints and marginal values.
7. Present the efficient decision frontier and explain tradeoffs.
8. Record provenance, assumptions, approvals, and dependencies.
9. Monitor the policy's validity and trigger recalculation when relevant state changes.

## Scope boundaries

These capabilities are in scope because they deepen the existing household decision engine. They do not require the platform to become:

- A broker-dealer or autonomous trading system
- A tax-return preparation product
- A law firm or document-drafting service
- A medical or psychological decision system
- A general-purpose life assistant
- A replacement for professional judgment and required approvals

Nonfinancial preferences may be represented as configured constraints or objectives when they affect a household capital decision. Independent optimization of health, relationships, or general life choices should remain outside the initial domain.

## Defensibility thesis

No individual feature above is a durable moat. The defensible system is the compiled interaction among:

- Effective-dated federal and 50-state rules
- Normalized household state and preference ontology
- Deterministic calculation and optimization tools
- Adaptive decision policies
- Dependency and provenance graphs
- Advisor policies, overrides, and approvals
- Observed completion and outcome data
- Monitoring and rule-impact analysis

A competitor can reproduce a calculator, add a conversational interface, or retrieve a state law. Reproducing the accumulated behavior of this integrated decision system is substantially harder.

## Recommended product language

> A state-aware household decision operating system that optimizes not only what to do, but when to act, what information to gather, which constraints matter, and how the strategy should adapt as the household changes.

The platform should not compete to produce the largest number of financial scenarios. It should compete to identify the smallest number of high-confidence, high-impact actions that remain valid under real household uncertainty.

## Repository placement

Recommended path:

```text
docs/
  product/
    household-decision-intelligence-spec.md
  strategy/
    household-decision-intelligence-competitive-positioning.md
    household-decision-optimization-differentiators.md
```

This document belongs in `docs/strategy/` because it defines why the product can be differentiated and which optimization capabilities should guide its roadmap. Individual capabilities should later receive implementation-ready specifications under a separate `specs/` or `docs/product/features/` directory.

Suggested future specifications:

```text
specs/
  adaptive-policy-optimizer/
  value-of-information-engine/
  constraint-shadow-price-engine/
  robust-recommendation-engine/
  decision-dependency-graph/
  execution-optimizer/
```
