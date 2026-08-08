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
