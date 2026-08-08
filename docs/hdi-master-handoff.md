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
| [011 Cash Inflow Allocation Decision Brief](specs/011-cash-inflow-allocation-decision-brief.md) | Synthetic decision brief for competing uses of a discrete cash inflow | 8, 18-20, 25 | Product, Optimization, Research |

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
| 1 | HCAO research prototype | Manual-input decision engine with baseline, alternatives, scenarios, trace, synthetic validation, and reviewable decision artifacts | 002, 003, 004, 005, 006, 007, 011 | Phase 1 Must requirements pass; 100% reconciliation on validation cases |
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
| FEAT-016 | Cash-inflow allocation decision brief | 0-1 | [011](specs/011-cash-inflow-allocation-decision-brief.md) | REQ-CIB-001-023, AC-CIB-001-013 |

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

## 8. Current Build State

As of August 8, 2026, Spec 011 has progressed through the first three vertical slices on branch `011-cash-inflow-allocation-decision-brief`.

| Slice | State | Primary Evidence | Notes |
|---|---|---|---|
| Slice A - Deterministic core | Implemented | [cash_inflow.py](../src/kinvoryx/cash_inflow.py), [test_cash_inflow.py](../tests/test_cash_inflow.py) | Synthetic-only data contract, transparent baseline, seven alternatives, shared scenario set, and acceptance-ID tests. |
| Slice B - Validation harness | Implemented | [cash_inflow_validation.py](../src/kinvoryx/cash_inflow_validation.py), [test_cash_inflow_validation.py](../tests/test_cash_inflow_validation.py) | Golden fixtures, deterministic property sweeps, reviewer annotations, and pilot-readiness blocker semantics. |
| Slice C - Decision-brief interface | Implemented | [cash_inflow_rendering.py](../src/kinvoryx/cash_inflow_rendering.py), [cash_inflow_interface.py](../src/kinvoryx/cash_inflow_interface.py), [test_cash_inflow_rendering.py](../tests/test_cash_inflow_rendering.py) | Household/reviewer Markdown and HTML exports plus a local synthetic manual-entry interface. |
| Slice D - Governed pilot readiness | Foundation implemented | [cash_inflow_governance.py](../src/kinvoryx/cash_inflow_governance.py), [test_cash_inflow_governance.py](../tests/test_cash_inflow_governance.py) | Versioned policy, explicit coverage, metadata-only audit fingerprints, privacy/security checklist, human-review state machine, and fail-closed composite gate. Accountable approval and real-household use remain out of scope. |

Current verification evidence is recorded by each committed slice. Slice D adds acceptance tests `AC-CIB-014` through `AC-CIB-017`; rerun the full unit-test, compile, and diff checks before relying on the current branch.

## 9. Repository Memory Protocol

Kinvoryx now has a repo-local memory protocol in [memory](../memory/README.md). Future work should use this protocol to retain durable lessons without storing private data.

The protocol is:

1. **Prime:** Read `AGENTS.md`, this handoff, `memory/manifest.yaml`, and relevant workflow lessons before substantial spec, architecture, validation, product, or interface work.
2. **Learn:** After meaningful progress, add metadata-only lessons that capture decisions, patterns, pitfalls, validation findings, and product-boundary nuances.
3. **Curate:** Mark stale records `stale` or `superseded`; do not silently overwrite lessons.
4. **Guard:** Never store credentials, raw household data, private household details, account records, or PII in memory.
5. **Trace:** Memory guides future sessions, but specs remain source truth for product behavior.

Seeded memory areas:

- [Platform lessons](../memory/kinvoryx_platform/lessons.md) for spec traceability, product boundary, repo workflow, and the external agentic SDK reference.
- [Spec 011 lessons](../memory/spec_011_cash_inflow_decision_brief/lessons.md) for slice sequencing, validation, rendering, reviewer annotations, and manual-entry scope.

## 10. Immediate Next Handoff Steps

1. Assign accountable owners to each numbered spec.
2. Convert Phase 0 and Phase 1 requirements into implementation tickets with requirement IDs.
3. Review and merge the Spec 011 branch after confirming Slice A-C artifacts meet the desired product posture.
4. Assign accountable domain, risk, privacy/security, and compliance owners to review the Slice D governance foundation.
5. Replace the prototype coverage example with an owner-approved first jurisdiction and decision-type coverage matrix before collecting real household data.
6. Approve pilot stop conditions, reviewer roles, retention controls, and an operational audit store before any controlled human pilot.
7. Validate the cash-inflow trigger, buyer, pricing hypothesis, and decision-brief usefulness before expanding the prototype beyond synthetic cases.
8. Continue the repository memory loop after each substantial spec slice: prime, learn, curate, and keep memory metadata-only.
