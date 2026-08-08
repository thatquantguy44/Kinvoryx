# Household Decision Intelligence Specs

This directory is the numbered spec home for the Household Decision Intelligence platform. Specs are intentionally split by durable product and platform capabilities so implementation work can trace back to stable requirement IDs.

## Numbering Convention

- Specs use a three-digit prefix: `001-...`, `002-...`, `003-...`.
- New specs receive the next available number and existing specs are not renumbered.
- Requirement IDs from the overview are preserved wherever possible.
- New implementation requirements use the spec prefix, for example `REQ-STATE-001`.
- Deprecated specs remain in place with status changed to `Superseded`.

## Master Handoff

- [HDI Master Handoff](../hdi-master-handoff.md)
- [Source Overview](../Household%20Decision%20Intelligence%20Overview.md)

## Current Spec Set

| Spec | Capability | Primary Phase | Status |
|---|---|---:|---|
| [001 Product Foundation](001-product-foundation.md) | Product boundaries, personas, jobs, positioning, and phase gates | 0-2 | Draft |
| [002 Household State and Data Model](002-household-state-and-data-model.md) | Household facts, provenance, data quality, permissions, exports, deletion | 1-2 | Draft |
| [003 AI Orchestration and Audit](003-ai-orchestration-and-audit.md) | Governed AI responsibilities, deterministic tools, reproducibility, evidence lineage | 1-3 | Draft |
| [004 Capital Allocation Optimizer](004-capital-allocation-optimizer.md) | Baselines, allocation alternatives, scenarios, constraints, explanations | 1-2 | Draft |
| [005 Product Labs and Workflows](005-product-labs-and-workflows.md) | Research, planning, scenario, proposal, monitoring, console, governance labs | 1-3 | Draft |
| [006 Jurisdiction Intelligence](006-jurisdiction-intelligence.md) | U.S. federal/state rules, coverage matrix, source hierarchy, change operations | 1-4 | Draft |
| [007 Validation and Market Research](007-validation-and-market-research.md) | Discovery, TAM/SAM/SOM, market gates, validation program, success metrics | 0-3 | Draft |
| [008 Professional Enterprise Workflows](008-professional-enterprise-workflows.md) | Adviser, CPA, employer, CIO, approvals, org policy, operating metrics | 2-3 | Draft |
| [009 Monitoring Alerts and Outcomes](009-monitoring-alerts-and-outcomes.md) | Plan drift, alerts, outcome measurement, lifecycle states | 2-3 | Draft |
| [010 Extension Portfolio](010-extension-portfolio.md) | Adjacent financial modules, cross-domain modules, extension admission gates | 4-6 | Draft |
| [011 Cash Inflow Allocation Decision Brief](011-cash-inflow-allocation-decision-brief.md) | Synthetic cash-inflow alternatives, comparable trade-offs, stress records, and governance controls | 0-1 | Draft - Slices A-D foundation implemented |

## Traceability Rule

Every implementation ticket should cite:

1. One or more spec files.
2. One or more requirement IDs.
3. The phase or gate it supports.
4. Its acceptance or verification method.
