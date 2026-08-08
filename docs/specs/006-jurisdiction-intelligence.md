# 006 Jurisdiction Intelligence

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 1-4  
**Related specs:** [002](002-household-state-and-data-model.md), [003](003-ai-orchestration-and-audit.md), [004](004-capital-allocation-optimizer.md)

## Purpose

Define the U.S. jurisdiction rule layer for tax, benefits, insurance, property, residency, and other state-dependent planning rules.

## Strategic Boundary

The initial product supports the United States at the federal level and develops reviewed coverage across all 50 states by decision vertical. The product may not imply national support until each state-decision combination has authoritative sources, effective dates, golden cases, qualified review, and explicit coverage status.

## Rule Coverage Domains

- Individual income tax, brackets, deductions, credits, capital gains, interest, dividends, and alternative regimes.
- Residency, domicile, part-year residence, nonresident income, remote work, reciprocity, and income sourcing.
- Retirement-income exclusions, pension treatment, Social Security taxation, and retirement incentives.
- 529 deductions/credits, recapture provisions, eligible-plan restrictions, and state benefits.
- HSA conformity and federal-state tax differences.
- Estate, inheritance, gift, property, homestead, transfer tax, marital property, creditor protection, insurance, paid leave, childcare, education, and other supported rule domains subject to legal-review boundaries.

## Requirements

- **REQ-JUR-001 — Must:** Every jurisdictional rule retains jurisdiction, source, citation, type, effective-from, effective-to, published/reviewed date, interpretation status, reviewer, and supported decision uses.
- **REQ-JUR-002 — Must:** Distinguish enacted, effective, proposed, expired, repealed, administratively interpreted, and organization-policy states.
- **REQ-JUR-003 — Must:** Calculations use the rule version effective for the decision date and preserve that version in audit.
- **REQ-JUR-004 — Must:** Household model supports domicile, residence, work, property, and income-source jurisdictions separately.
- **REQ-JUR-005 — Must:** Multi-state cases identify overlapping claims, reciprocity, credits, source-income treatment, and unresolved ambiguity.
- **REQ-JUR-006 — Must:** Each supported decision type has a state-coverage matrix showing full, partial, unsupported, and expert-review-required status.
- **REQ-JUR-007 — Must:** Recommendations depending on unsupported or stale state rules are blocked, bounded, or routed for qualified review.
- **REQ-JUR-008 — Must:** Material rule changes trigger impact analysis for calculations, households, proposals, monitoring rules, and disclosures.
- **REQ-JUR-009 — Must:** State-rule content is reviewed through documented four-eyes process by qualified specialists.
- **REQ-JUR-010 — Must:** Product clearly communicates planning analysis versus legal conclusion or tax-return position.
- **REQ-JUR-011 — Should:** Compare current and alternative jurisdictions for explicit household decisions, including moving costs, non-tax effects, uncertainty, and residency requirements.
- **REQ-JUR-012 — Should:** Institutions can add reviewed interpretive guidance without overwriting public rule/source.
- **REQ-JUR-013 — Could:** District of Columbia and U.S. territories may be added through the same admission and coverage framework.

## Source Hierarchy

1. Statute, regulation, administrative code, official form, or official agency publication.
2. Official federal or state agency website and formal guidance.
3. Approved licensed data provider with contractual update obligations.
4. Reviewed secondary professional authority where primary text requires interpretation.
5. General web content for discovery only, never final authority.

## Rollout Strategy

1. Residency, income tax, retirement income, 529, and HSA conformity for all 50 states.
2. Multi-state employment, reciprocity, remote work, and part-year transitions.
3. Property, homestead, housing, and major-purchase rules.
4. Insurance, benefits, paid leave, childcare, education, and resilience programs.
5. Estate, inheritance, marital property, and creditor-protection decision support with tighter legal review.

## Gates

- **GATE-J1 — Source completeness:** Every material rule has controlling or approved source and effective date.
- **GATE-J2 — Calculation accuracy:** Golden cases for supported state and decision type match reviewed expected results.
- **GATE-J3 — Boundary accuracy:** Multi-state, part-year, remote-work, and conflicting-jurisdiction cases route correctly or stop safely.
- **GATE-J4 — Change operations:** Simulated rule change is ingested, reviewed, tested, approved, deployed, and traced.
- **GATE-J5 — Coverage honesty:** Product claims match actual coverage matrix.

## Acceptance Criteria

- Every state-decision combination has explicit status.
- Unsupported jurisdiction-dependent recommendations are blocked, bounded, or routed.
- A simulated state-rule change produces a traceable affected-household/proposal/alert list.

