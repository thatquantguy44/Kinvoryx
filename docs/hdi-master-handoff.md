# Household Decision Intelligence Master Handoff

**Status:** Draft for spec-driven development  
**Date:** August 8, 2026  
**Source:** [Household Decision Intelligence Overview](Household%20Decision%20Intelligence%20Overview.md)  
**Initial product:** Household Capital Allocation Optimizer (HCAO)  
**Long-term category:** Household Decision Intelligence (HDI)

## 1. Purpose

This handoff turns the product overview into an executable specification map. It is the master document for product, research, design, engineering, domain review, compliance, and go-to-market planning.

The system starts with one measurable decision:

> Given this household's goals, constraints, accounts, debts, taxes, and uncertainty, what is the highest-value use of its next dollar?

The product must produce transparent, scenario-dependent allocation plans. It must not become a stock picker, trading assistant, generic chatbot, or autonomous financial adviser. AI orchestrates workflow and explanation; deterministic, versioned tools produce authoritative math, rules, reconciliation, optimization, validation, and monitoring outputs.

## 2. Spec Set

The numbered specs below are the canonical implementation handoff units. New specs should be added to [docs/specs](specs/README.md) using the next available number.

| Spec | Scope | Source Overview Sections | Primary Owners |
|---|---|---|---|
| [001 Product Foundation](specs/001-product-foundation.md) | Product thesis, beachhead, positioning, users, scope, phases | 1-8, 17, 23-25 | Product, Design, Compliance |
| [002 Household State and Data Model](specs/002-household-state-and-data-model.md) | Household facts, provenance, freshness, permissions, data quality | 7-9, 11, 16 | Engineering, Security, Privacy |
| [003 AI Orchestration and Audit](specs/003-ai-orchestration-and-audit.md) | AI/tool boundary, workflow plans, evidence lineage, reproducibility | 6B, 9, 21, 25 | AI, Platform, Model Risk |
| [004 Capital Allocation Optimizer](specs/004-capital-allocation-optimizer.md) | Baselines, objective research, allocations, scenarios, explanations | 8, 10, 18-19, 25 | Optimization, Product, Domain Review |
| [005 Product Labs and Workflows](specs/005-product-labs-and-workflows.md) | Lab workspaces and cross-lab decision flow | 6A, 16 | Product, Design, Engineering |
| [006 Jurisdiction Intelligence](specs/006-jurisdiction-intelligence.md) | U.S. rule coverage, source hierarchy, effective dating, state gates | 11A, 21, 25 | Tax/Legal, Data Ops, Engineering |
| [007 Validation and Market Research](specs/007-validation-and-market-research.md) | TAM/SAM/SOM, discovery, validation, metrics, stop conditions | 12-13, 18-20, 25 | Research, GTM, Product |
| [008 Professional Enterprise Workflows](specs/008-professional-enterprise-workflows.md) | Adviser/CPA/employer/CIO governance, review, approvals, operating metrics | 1, 6, 6A, 17, 22 | Enterprise Product, Compliance |
| [009 Monitoring Alerts and Outcomes](specs/009-monitoring-alerts-and-outcomes.md) | Drift detection, alert lifecycle, observed outcomes, plan updates | 6A, 8, 16, 18-19 | Product, Engineering, Support |
| [010 Extension Portfolio](specs/010-extension-portfolio.md) | Adjacent financial and cross-domain modules with admission gates | 14-16, 21, 24-25 | Product Strategy, Research |

## 3. Product Boundary

### Own

- Household capital allocation.
- Goal funding and trade-off analysis.
- Liquidity, debt, taxes, benefits, retirement, household risk, and major decision support.
- Scenario analysis, constraint diagnostics, opportunity cost, and decision artifacts.
- Professional review and organization-governed assumptions where applicable.

### Integrate

- Institutional capital-market assumptions.
- Tax and benefit rules.
- Account, debt, payroll, and benefit data.
- Planning policies and approved product catalogs.
- Later: calendar, housing, childcare, education, labor-market, and logistics data.

### Exclude

- Asset custody, money movement, trade execution, tax filing, legal representation, definitive insurance/fiduciary representation, individual-security selection, and autonomous account actions.
- LLM-authored authoritative calculations, eligibility decisions, unsupported jurisdiction rules, or fabricated recommendation narratives.

## 4. Phase Plan

| Phase | Name | Outcome | Primary Specs | Exit Gates |
|---:|---|---|---|---|
| 0 | Discovery and falsification | Pick a beachhead, trigger event, buyer, pricing hypothesis, and value proposition | 001, 007 | GATE-M1, GATE-M2, counsel issue map clear enough for prototype |
| 1 | HCAO research prototype | Manual-input decision engine with baseline, alternatives, scenarios, trace, and synthetic validation | 002, 003, 004, 005, 006, 007 | Phase 1 Must requirements pass; 100% reconciliation on validation cases |
| 2 | Controlled human pilot | Secure onboarding, limited real households, human review, payment evidence, override capture | 001-009 | GATE-M3, GATE-M4, no severe privacy/safety issue |
| 3 | Professional and employer distribution | Adviser/CPA workspace, org policy governance, review queue, batch monitoring, audit | 003, 005, 006, 008, 009 | GATE-M5; viable pipeline economics in at least two channel types |
| 4 | Adjacent financial modules | Add approved financial extensions one at a time | 006, 010 | REQ-EXT admission gates and module-specific validation pass |
| 5 | Cross-domain life decisions | Add resilience, major purchase, housing/location, and career-capital modules | 010 | Independent safety, market, data, and outcome gates pass |
| 6 | Household operating system | Add time, energy, family logistics, goal portfolio, and eventual digital twin integration | 010 | Cross-domain evidence supports integration without unacceptable privacy or overreach |

## 5. High-Level Feature Catalog

| Feature ID | Feature | First Phase | Spec | Trace IDs |
|---|---|---:|---|---|
| FEAT-001 | Household case onboarding and completeness review | 1 | [002](specs/002-household-state-and-data-model.md) | REQ-001-006, REQ-DATA-001-004 |
| FEAT-002 | Goal, preference, constraint, and fairness capture | 1 | [002](specs/002-household-state-and-data-model.md) | REQ-010-014, NFR-015 |
| FEAT-003 | Rules-based baseline allocation | 1 | [004](specs/004-capital-allocation-optimizer.md) | REQ-020, Required baselines |
| FEAT-004 | Feasible allocation alternatives | 1 | [004](specs/004-capital-allocation-optimizer.md) | REQ-021-027 |
| FEAT-005 | Stress scenarios and outcome ranges | 1 | [004](specs/004-capital-allocation-optimizer.md) | REQ-030-035 |
| FEAT-006 | Binding-constraint and opportunity-cost explanation | 1 | [004](specs/004-capital-allocation-optimizer.md) | REQ-040-045 |
| FEAT-007 | Reproducible decision record | 1 | [003](specs/003-ai-orchestration-and-audit.md) | REQ-AI-001-010, NFR-016-017 |
| FEAT-008 | Specialized product labs | 1-3 | [005](specs/005-product-labs-and-workflows.md) | REQ-LAB-001-064 |
| FEAT-009 | U.S. jurisdiction rule registry and coverage matrix | 1-4 | [006](specs/006-jurisdiction-intelligence.md) | REQ-JUR-001-013 |
| FEAT-010 | Proposal artifact and approval lifecycle | 2 | [005](specs/005-product-labs-and-workflows.md) | REQ-LAB-030-035, REQ-050-054 |
| FEAT-011 | Human/professional review queue | 2-3 | [008](specs/008-professional-enterprise-workflows.md) | REQ-LAB-050-054 |
| FEAT-012 | Monitoring, alerts, and re-analysis prompts | 2-3 | [009](specs/009-monitoring-alerts-and-outcomes.md) | REQ-LAB-040-045, REQ-052-054 |
| FEAT-013 | Organization policy, assumption, and audit governance | 3 | [008](specs/008-professional-enterprise-workflows.md) | REQ-LAB-050-064 |
| FEAT-014 | Market validation and TAM model | 0-3 | [007](specs/007-validation-and-market-research.md) | GATE-M1-M5, AC-010-011 |
| FEAT-015 | Extension admission and sequencing | 4-6 | [010](specs/010-extension-portfolio.md) | REQ-EXT-001-007 |

## 6. Cross-Cutting Architectural Contracts

1. Household facts, institutional assumptions, jurisdiction rules, observed state, and AI-generated narrative are separate information classes.
2. Every material field has source, owner, effective date, freshness, validation status, and permitted uses.
3. Every material recommendation is generated from a retained input snapshot, scenario, configuration, tool version, validation status, and approval state.
4. Every numerical claim in a proposal, research answer, or alert traces to a deterministic tool result or approved source.
5. A failed, infeasible, stale, unsupported, timed-out, or unvalidated run fails closed and cannot be narrated as a recommendation.
6. Human overrides are retained as overrides with reasons, not silently converted into source truth.
7. No material transfer, trade, election, application, cancellation, or schedule change executes without affirmative authorization.

## 7. Acceptance Rollup

The program is ready to move from specification to design when:

- A single Phase 0 beachhead, trigger event, buyer, pricing hypothesis, and primary job are approved.
- Phase 1 scope and unsupported cases are approved.
- Every Must requirement has an owner and verification method.
- Tax, legal, privacy, security, accessibility, incident-response, and model-risk owners are assigned.
- TAM/SAM/SOM methods, interview cohort, pilot metrics, and stop conditions are approved.
- State-rule coverage claims match the jurisdiction coverage matrix.
- Extension modules remain gated until they pass independent admission requirements.

## 8. Immediate Next Handoff Steps

1. Assign accountable owners to each numbered spec.
2. Convert Phase 0 and Phase 1 requirements into implementation tickets with requirement IDs.
3. Create synthetic household fixtures and golden-case validation criteria before building optimizer logic.
4. Define the first supported jurisdiction and decision-type coverage matrix.
5. Approve pilot stop conditions before collecting real household data.

