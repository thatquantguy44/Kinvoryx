# Kinvoryx Repository Memory

This directory stores durable, metadata-only lessons that help future Kinvoryx
work start with the nuance already learned in prior sessions.

The governing protocol is adapted from the agentic workflow SDK:
`/Users/joshualutkemuller/Documents/Quant Sandbox/agentic_workflows/qf_workflow_sdk_public/instructions/workflow_memory.md`.

## How to Use This Memory

1. **Prime:** Before substantial work, read `manifest.yaml`, then read the
   workflow-specific `index.yaml` and `lessons.md` relevant to the task.
2. **Learn:** After meaningful progress, add lessons only when they are likely to
   help future sessions avoid a mistake, preserve a decision, or move faster.
3. **Curate:** If a lesson becomes stale or wrong, mark it `stale` or `superseded`
   in the relevant `index.yaml` and explain the replacement evidence.
4. **Report:** When memory materially influenced work, mention that in the handoff
   or final summary.

## Guardrails

- Metadata only. Never store real household details, credentials, connection
  strings, API keys, raw account data, private notes, or PII.
- Specs remain source truth. Memory captures working knowledge, decisions, and
  caution signs; it does not override `docs/specs/` or the master handoff.
- Provenance always. Every record needs evidence, date, confidence, access level,
  and status.
- No silent overwrite. Contradictions are resolved through supersession, not by
  deleting history.

## Current Memory Areas

- `kinvoryx_platform/` - platform-wide spec-driven development, repo workflow,
  and product-boundary lessons.
- `spec_011_cash_inflow_decision_brief/` - lessons for the cash-inflow allocation
  decision brief and its Slice A-C implementation.
