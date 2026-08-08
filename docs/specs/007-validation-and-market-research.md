# 007 Validation and Market Research

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 0-3  
**Related specs:** [001](001-product-foundation.md), [004](004-capital-allocation-optimizer.md), [008](008-professional-enterprise-workflows.md)

## Purpose

Define the discovery, market sizing, validation, metrics, and stop conditions needed before broad build-out.

## TAM/SAM/SOM Methods

Use three independent TAM methods and reconcile them:

- Bottom-up household subscription model: eligible households x problem incidence x annual willingness to pay.
- Adviser/CPA B2B2C model: addressable firms x eligible seats or households x annual contract value.
- Value-based model: addressable cases x verified annual value created x capturable share.

The market model must separate software revenue from asset pools and must deduplicate target segments.

## Required Research Deliverables

- Segment taxonomy with non-overlapping population estimates.
- Competitive feature and positioning matrix.
- TAM/SAM/SOM model with low, base, and high scenarios.
- Sensitivity table for incidence, price, retention, and conversion.
- Interview repository with coded pain and trust themes.
- Price-sensitivity study plus behavioral purchase tests.
- Unit-economics model covering data, compute, support, compliance, and acquisition.
- Recommendation on initial buyer, wedge, pricing unit, and channel.

## Market Gates

- **GATE-M1 — Problem:** At least 20 of 30 qualified discovery participants describe a recent relevant decision, unsatisfactory workaround, and material consequence.
- **GATE-M2 — Trust:** At least half of prototype users are willing to provide minimum viable data after reviewing privacy and control model.
- **GATE-M3 — Value:** At least 60% of qualified pilot users rate the decision artifact materially more useful than existing approach.
- **GATE-M4 — Payment:** Obtain behavioral evidence: paid pilot, refundable deposit, adviser LOI with budget, or employer pilot.
- **GATE-M5 — Economics:** Base-case gross margin and retention support selected acquisition channel.

## Validation Program

### Offline

- Synthetic edge cases reviewed by domain specialists.
- Property-based checks for cash conservation, constraint satisfaction, and monotonicity.
- Scenario sensitivity and adversarial household cases.
- Comparison with transparent heuristics.
- Subgroup performance and data-missingness analysis.

### Prospective

- Observe usefulness before integration-led actions.
- Pre-register pilot metrics and error classes.
- Separate recommendation acceptance from follow-through.
- Compare predicted and observed outcomes when consent and horizon allow.
- Investigate overrides as potential model information.

### Human Factors

- Users can state recommendation assumptions.
- Users can identify main trade-off and next-best alternative.
- Users do not over-trust precise forecasts.
- Couples perceive allocations as fair.
- Product reduces decision anxiety without increasing overconfidence.

## Success Metrics

- Verified household decision value per active case.
- Time from onboarding to first decision artifact.
- Input completion and correction rate.
- Percentage of cases with two or more feasible alternatives.
- Recommendation comprehension, acceptance, override, and follow-through.
- Captured employer match, avoided interest/penalty, liquidity improvement, goal shortfall reduction, estimated tax/benefit improvement.
- Material error rate, hard-constraint violation rate, unsupported-claim rate, stale data rate, severe privacy/security incidents.
- Paid conversion, retention, ARPA, gross margin, CAC/payback, reviewer capacity, expansion revenue.

## Stop Conditions

- Severe privacy/security incident.
- Unsupported regulated claim delivered to a user.
- Hard-constraint violation above pre-approved threshold.
- Recommendation instability above pre-approved threshold.
- Expert material-error rate above pre-approved threshold.
- Unit economics fail for selected channel after priced pilot.

## Acceptance Criteria

- TAM/SAM/SOM uses at least three methods with sensitivity ranges.
- Market validation includes behavioral payment evidence.
- Pilot reporting includes quality, comprehension, safety, economics, subgroup results, and professional corrections.

