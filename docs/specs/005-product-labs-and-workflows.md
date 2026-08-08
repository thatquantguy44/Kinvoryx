# 005 Product Labs and Workflows

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 1-3  
**Related specs:** [003](003-ai-orchestration-and-audit.md), [004](004-capital-allocation-optimizer.md), [008](008-professional-enterprise-workflows.md), [009](009-monitoring-alerts-and-outcomes.md)

## Purpose

Define interoperable labs: focused decision environments with shared household state, permitted tools, output contracts, and audit requirements.

Labs share governed household state and decision history. They must not become disconnected mini-applications with conflicting facts.

## Lab Map

| Lab | Purpose | First Phase |
|---|---|---:|
| Conversational Research Lab | Investigate planning questions using grounded evidence | 1 |
| Household Planning Lab | Maintain balance sheet, cash flow, goals, liquidity, constraints | 1 |
| Scenario and Optimization Lab | Run reproducible what-if analysis and alternatives | 1 |
| Personalized Proposal Lab | Convert validated outputs into reviewable proposals | 2 |
| Monitoring and Alerts Lab | Detect plan drift and revisit triggers | 2 |
| Adviser and CIO Console | Govern assumptions, policies, workflows, cases, approvals | 3 |
| Governance and Audit Lab | Reconstruct recommendations and investigate lineage | 1-3 |

## Requirements

- **REQ-LAB-001 — Must:** Research answers material factual questions only from approved household data, institutional data, retrieved primary evidence, or labeled assumptions.
- **REQ-LAB-002 — Must:** Distinguish sourced facts, deterministic calculations, model estimates, preferences, and narrative interpretation.
- **REQ-LAB-003 — Must:** Every numerical claim links to a calculation result or approved source version.
- **REQ-LAB-004 — Must:** Conversation can initiate scenarios or proposals but cannot become the calculation engine.
- **REQ-LAB-005 — Should:** Research findings can be saved as evidence attached to a decision case.
- **REQ-LAB-010 — Must:** Planning lab exposes balance sheet, cash flow, goal map, liquidity, decision calendar, and unresolved data issues.
- **REQ-LAB-011 — Must:** Users configure household priorities, limits, exclusions, and preferences without changing institutional assumptions.
- **REQ-LAB-012 — Must:** Planning lab identifies binding constraints, conflicting goals, and marginal value of relaxing constraints.
- **REQ-LAB-013 — Should:** Planning lab maintains current plan and compares proposed revisions.
- **REQ-LAB-020 — Must:** Calculations and optimization come from registered, versioned deterministic tools or governed stochastic models.
- **REQ-LAB-021 — Must:** Each run retains inputs, configurations, assumptions, constraints, tool versions, outputs, validation, and status.
- **REQ-LAB-022 — Must:** Compare current plan, baseline, recommendation, and counterfactuals under identical scenarios.
- **REQ-LAB-023 — Must:** Failed, timed-out, infeasible, or unvalidated runs are never narrated as successful recommendations.
- **REQ-LAB-024 — Should:** Professionals can lock institutional assumptions while allowing permitted household overlays.
- **REQ-LAB-030 — Must:** Proposals are generated only from validated outputs and approved evidence.
- **REQ-LAB-031 — Must:** Proposals show goals, actions, timing, assumptions, trade-offs, alternatives, risks, disclosures, and approvals.
- **REQ-LAB-032 — Must:** Proposal numbers reconcile exactly with the decision record.
- **REQ-LAB-033 — Must:** Draft, reviewed, approved, delivered, superseded, and rejected states are distinct and auditable.
- **REQ-LAB-034 — Should:** Same verified result can render for household, adviser, committee, or compliance audience without changing meaning.
- **REQ-LAB-035 — Could:** Approved templates may add branding/disclosures while preserving lineage.
- **REQ-LAB-040 — Must:** Monitoring evaluates versioned rules against refreshed household and institutional data.
- **REQ-LAB-041 — Must:** Alerts state observed change, breached rule, affected decision, materiality, confidence, and review path.
- **REQ-LAB-042 — Must:** Alerts are never presented as executed actions.
- **REQ-LAB-043 — Must:** Alert deduplication, severity, cooldown, acknowledgement, escalation, and closure are auditable.
- **REQ-LAB-044 — Should:** Users and organizations configure thresholds within governed ranges.
- **REQ-LAB-045 — Should:** Alerts are prioritized by household impact and urgency.
- **REQ-LAB-050 — Must:** Authorized users manage approved assumptions, policy parameters, planning rules, constraints, thresholds, and effective dates.
- **REQ-LAB-051 — Must:** Institutional and household configuration are separated with precedence policy and change log.
- **REQ-LAB-052 — Must:** Professionals view cases needing review, stale data, failed calculations, policy exceptions, upcoming decisions, and unresolved alerts.
- **REQ-LAB-053 — Must:** Batch personalization preserves household-level constraints and does not replace required review.
- **REQ-LAB-054 — Should:** Console reports preparation time, exception volume, reviewer capacity, and recommendation consistency.
- **REQ-LAB-060 — Must:** Reviewers can reconstruct material recommendations from snapshots, config, tool calls, outputs, validation, narrative, and approvals.
- **REQ-LAB-061 — Must:** Expose lineage from source field through calculation and proposal claim.
- **REQ-LAB-062 — Must:** Compare decision versions and identify changed inputs, policy, assumptions, tools, or approvals.
- **REQ-LAB-063 — Must:** Record human overrides and reasons without treating override as model truth.
- **REQ-LAB-064 — Should:** Governance monitors tool reliability, explanation fidelity, exceptions, data quality, drift, and subgroup outcomes.

## Acceptance Criteria

- Labs share one household state and decision history.
- Cross-lab transitions preserve evidence, run state, and approval state.
- Proposal, monitoring, professional, and governance views render from the same decision record.

