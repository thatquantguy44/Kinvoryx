# 003 AI Orchestration and Audit

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 1-3  
**Related specs:** [002](002-household-state-and-data-model.md), [004](004-capital-allocation-optimizer.md), [005](005-product-labs-and-workflows.md), [008](008-professional-enterprise-workflows.md)

## Purpose

Define the governed AI operating model, deterministic tool boundary, reproducibility contract, and audit record required for material decisions.

## Responsibility Separation

| Layer | Permitted | Prohibited |
|---|---|---|
| Conversational AI | Intent discovery, clarification, routing, evidence retrieval, tool selection, summarization, explanation, drafting, exception triage | Inventing facts, authoritative math, changing approved inputs, bypassing tools, approving actions |
| Deterministic tools | Tax/benefit calculations, cash-flow projection, constraint validation, reconciliation, optimization, eligibility rules, alerts | Unreviewed narrative interpretation, unsupported jurisdictions |
| Governed ML/statistical models | Forecasting uncertain inputs, prioritization, anomaly detection, calibrated scenario estimates | Presenting estimates as rules or facts, overriding hard constraints |
| Institutional policy | Approved assumptions, source data, planning rules | Silent household-specific modification |
| Household configuration | Goals, facts, preferences, restrictions, permissions, approvals | Modification of institutional source history |
| Human professional | Judgment, exception review, suitability assessment, client communication | Undocumented overrides or audit alteration |

## Workflow Requirements

- **REQ-AI-001 — Must:** AI constructs a typed workflow plan identifying question, required facts, jurisdictions, required tools, approvals, and expected output before a material recommendation.
- **REQ-AI-002 — Must:** Tool inputs and outputs are schema-validated; malformed, incomplete, stale, or unauthorized calls fail closed.
- **REQ-AI-003 — Must:** AI quotes or renders numerical results only from validated tool results or approved sources.
- **REQ-AI-004 — Must:** The system independently verifies reconciliation, hard constraints, rule coverage, and proposal-number consistency before delivery.
- **REQ-AI-005 — Must:** AI states uncertainty, missing information, unsupported scope, and required professional review without filling gaps through plausible language.
- **REQ-AI-006 — Must:** Wording, language model, or prompt changes cannot change deterministic results for identical approved inputs and tool versions.
- **REQ-AI-007 — Must:** The AI orchestration layer is replaceable without rewriting rule bases, deterministic engines, or audit history.
- **REQ-AI-008 — Must:** Every material AI step retains model identifier, orchestration version, evidence IDs, tool calls, validation status, artifact version, and approvals subject to retention policy.
- **REQ-AI-009 — Should:** Explanation variants can be comprehension-tested only after numerical and logical fidelity are locked.
- **REQ-AI-010 — Should:** The system detects narrative claims unsupported by the evidence graph before delivery.

## Audit Record

A material recommendation record must include:

- Household input snapshot ID.
- Institutional configuration and policy version.
- Jurisdiction rule version and coverage status.
- Scenario set and assumptions.
- Tool names, versions, inputs, outputs, validation result, and run status.
- Optimization tie-breaking policy.
- Narrative artifact version.
- Proposal state and approval trail.
- Human overrides and reasons.
- Subsequent observed outcomes and alerts.

## Reproducibility Contract

For identical approved input snapshot, institutional configuration, jurisdiction rule set, scenario, deterministic tool version, and tie-breaking policy, material calculations and recommended action sets must reproduce within approved tolerances.

If stochastic models participate, the record must retain model version, calibration window, seed or distributional inputs, and permitted tolerance.

## Acceptance Criteria

- Identical governed inputs reproduce deterministic golden-case outputs.
- Failed, infeasible, timed-out, stale, or unvalidated runs cannot create successful recommendation narratives.
- Every numerical proposal claim traces to a tool output or approved source.
- A reviewer can reconstruct a recommendation from retained snapshots, tool outputs, validation checks, narrative version, and approvals.

