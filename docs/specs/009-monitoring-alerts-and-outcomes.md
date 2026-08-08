# 009 Monitoring Alerts and Outcomes

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 2-3  
**Related specs:** [002](002-household-state-and-data-model.md), [003](003-ai-orchestration-and-audit.md), [005](005-product-labs-and-workflows.md), [008](008-professional-enterprise-workflows.md)

## Purpose

Define plan monitoring, alerts, re-analysis prompts, and outcome measurement after an approved decision.

## Monitoring Contract

Monitoring evaluates versioned rules against refreshed household and institutional data. It does not execute actions. Its job is to decide whether a prior recommendation should be reviewed, superseded, or left alone.

## Requirements

- **REQ-050 — Must:** Material actions remain proposed until affirmatively approved by required household member or professional reviewer.
- **REQ-051 — Must:** Record recommendation version, input snapshot, assumptions, approval status, and subsequent user action.
- **REQ-052 — Must:** Detect material changes to income, balances, debts, goals, or assumptions and indicate whether re-analysis is warranted.
- **REQ-053 — Should:** Users can compare a new plan with prior approved plan and see exactly what changed.
- **REQ-054 — Could:** Read-only monitoring integrations may notify users of drift; they do not execute corrective actions.
- **REQ-MON-001 — Must:** Alerts identify observed change, breached rule or threshold, affected decision, materiality, confidence, and recommended review path.
- **REQ-MON-002 — Must:** Alert lifecycle includes new, acknowledged, snoozed, escalated, closed, superseded, and false-positive states.
- **REQ-MON-003 — Must:** Deduplication, severity, cooldown, acknowledgement, escalation, and closure are auditable.
- **REQ-MON-004 — Must:** Alert thresholds are versioned and tied to user or organization configuration.
- **REQ-MON-005 — Should:** Alerts are prioritized by impact and urgency rather than volume.
- **REQ-MON-006 — Should:** Outcome measurement distinguishes observed follow-through from estimated causal value.

## Outcome Measurement

Track:

- Whether approved actions occurred.
- Whether expected cash-flow, debt, liquidity, contribution, tax, or goal outcomes materialized.
- Whether the household rejected, delayed, or overrode a recommendation.
- Whether a professional correction materially changed the recommendation.
- Whether a later change made the plan stale.

## Acceptance Criteria

- No alert is presented as an executed action.
- A user can compare current, prior approved, and proposed replacement plans.
- Monitoring records preserve evidence, rule version, threshold, alert lifecycle, and closure reason.

