# 008 Professional Enterprise Workflows

**Status:** Draft  
**Source:** [Household Decision Intelligence Overview](../Household%20Decision%20Intelligence%20Overview.md)  
**Primary phases:** 2-3  
**Related specs:** [003](003-ai-orchestration-and-audit.md), [005](005-product-labs-and-workflows.md), [006](006-jurisdiction-intelligence.md), [009](009-monitoring-alerts-and-outcomes.md)

## Purpose

Define adviser, CPA, employer, platform, and CIO workflows for governed personalization at scale.

## Enterprise Value Proposition

Convert institutional research, approved assumptions, planning policies, and household configurations into personalized, reviewable strategies at scale without requiring professionals to repeat data gathering, calculations, proposal assembly, monitoring, and documentation for every client.

This claim must be measured through reduced preparation time, fewer manual handoffs, lower rework, and controlled exception rates.

## Professional Jobs

- Turn client conversation into complete, reviewable planning case without rekeying facts.
- Apply approved assumptions and policies consistently while preserving household configuration.
- Generate reproducible personalized proposals.
- Identify households requiring attention and why.
- Govern assumptions, policies, exceptions, approvals, and disclosures.

## Requirements

- **REQ-ENT-001 — Must:** Organizations can define roles for adviser/planner, CPA/tax reviewer, CIO/investment policy, compliance, support, and admin.
- **REQ-ENT-002 — Must:** Review queues show stale data, failed calculations, policy exceptions, unsupported jurisdictions, upcoming decisions, and unresolved alerts.
- **REQ-ENT-003 — Must:** Organization assumptions have effective dates, owners, approval status, and change logs.
- **REQ-ENT-004 — Must:** Institutional configuration is separated from household configuration and source rules.
- **REQ-ENT-005 — Must:** Batch personalization preserves household-level constraints and required review.
- **REQ-ENT-006 — Must:** Professional corrections are captured as structured review outcomes with reason codes.
- **REQ-ENT-007 — Must:** Proposal rendering can target household, adviser, committee, or compliance audiences without changing underlying numbers.
- **REQ-ENT-008 — Should:** Organization dashboards show preparation time, rekeying, manual handoffs, reviewer capacity, exception volume, correction rates, and recommendation consistency.
- **REQ-ENT-009 — Should:** Employers cannot access private employee household details beyond approved aggregate or consented views.
- **REQ-ENT-010 — Could:** API/white-label clients can call approved decision modules with organization-specific policies and retained evidence bundles.

## Pilot Requirements

- Human review required for all controlled human pilot recommendations unless legal/compliance signs off a narrower exception.
- Every reviewer action must be timestamped and attributable.
- Reviewer override must not alter source data unless separately confirmed by the household or authorized data owner.
- Professional correction rate and reviewer time are primary economics metrics.

## Acceptance Criteria

- Professional pilot measures preparation time, rekeying, handoffs, rework, material error, and exception burden.
- Role-based access prevents unauthorized policy changes and household-data access.
- Organization policy changes can be traced to affected decisions and proposals.

