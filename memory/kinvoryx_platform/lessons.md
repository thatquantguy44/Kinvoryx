# Kinvoryx Platform Lessons

## MEM-KIN-20260808-001 - Keep The Traceability Spine Tight

- **Scope:** spec-driven development
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `docs/hdi-master-handoff.md`, `docs/specs/011-cash-inflow-allocation-decision-brief.md`

Stable IDs are the spine of this repository. Meaningful behavior should trace
from master handoff to numbered spec, requirements, acceptance criteria, code,
tests, demos, and final handoff notes.

## MEM-KIN-20260808-002 - Preserve The Decision-Support Boundary

- **Scope:** product boundary
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `docs/hdi-master-handoff.md`, Spec 011

The strongest product posture today was comparison, transparency, and deterministic
math. Do not let UI, wording, or ranking mechanics imply a selected plan,
personalized advice, execution, tax filing, legal advice, security selection, or
unsupported jurisdiction eligibility.

## MEM-KIN-20260808-003 - Stage Only The Active Slice

- **Scope:** repo workflow
- **Type:** pitfall
- **Status:** active
- **Confidence:** medium
- **Evidence:** unrelated local strategy doc observed during Spec 011 work

This repo may have user-created docs or strategy artifacts in flight. Before
commits, inspect `git status --short --branch` and stage only files tied to the
current user request.

## MEM-KIN-20260808-004 - Use The External SDK As A Pattern Library

- **Scope:** agentic workflow SDK
- **Type:** pattern
- **Status:** active
- **Confidence:** high
- **Evidence:** `AGENTS.md`, `memory/manifest.yaml`

The external SDK contains useful workflow standards for spec-driven development,
workflow memory, data quality, point-in-time reasoning, validation, and agent
roles. Treat it as a read-only reference unless the user asks to edit it.
