# Kinvoryx Agent Guidance

## Agentic Workflow SDK Reference

- For substantial architecture, planning, spec-driven development, workflow design,
  financial/quant logic, data quality, validation, agent orchestration, memory,
  backtesting, optimization, ML, or documentation work, first check whether the
  reusable agentic workflow SDK has a relevant pattern:
  `/Users/joshualutkemuller/Documents/Quant Sandbox/agentic_workflows/qf_workflow_sdk_public/`.
- Treat that SDK as a read-only reference unless the user explicitly asks to edit it.
  Reuse its ideas, templates, checks, and agent roles where they fit this repo; do
  not vendor or copy large chunks blindly.
- Useful starting points in the SDK:
  - `instructions/spec_driven_development.md`
  - `instructions/engineering_principles.md`
  - `instructions/workflow_memory.md`
  - `instructions/data_quality.md`
  - `instructions/point_in_time.md`
  - `agents/agent_registry.yaml`
  - `memory/README.md`
- When a task introduces or changes meaningful product behavior, keep Kinvoryx's
  specs traceable: update the master handoff, add or update the next numbered spec
  under `docs/specs/`, and preserve stable requirement/feature IDs.

## Repository Memory Protocol

- Before substantial Kinvoryx work, prime from this file, the master handoff, and
  the relevant records under `memory/`. For Spec 011 work, read
  `memory/spec_011_cash_inflow_decision_brief/lessons.md` before changing code,
  tests, specs, or interface behavior.
- Use the SDK memory standard in
  `/Users/joshualutkemuller/Documents/Quant Sandbox/agentic_workflows/qf_workflow_sdk_public/instructions/workflow_memory.md`
  as the governing pattern: provenance always, metadata only, no secrets, no PII,
  no raw household data, honest confidence, and supersede instead of silently
  overwriting prior lessons.
- After substantial work, append or update repo memory when a durable lesson,
  decision, pitfall, validation result, or product nuance should help future
  sessions. Every memory record must include an ID, scope, type, statement,
  evidence, confidence, status, access level, and date.
- Treat memory as guidance, not source truth. Specs remain authoritative for
  product behavior; memory helps future agents find the right constraints,
  assumptions, and sharp edges faster.
- If a current observation contradicts existing memory, mark the older record
  stale or superseded in the relevant `index.yaml` and explain the new evidence
  in `lessons.md`.
