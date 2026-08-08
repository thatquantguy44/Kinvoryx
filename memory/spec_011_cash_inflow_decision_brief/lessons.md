# Spec 011 Cash-Inflow Decision Brief Lessons

## MEM-S011-20260808-001 - Use The Slice Order As A Safety Rail

- **Scope:** slice sequence
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** Spec 011, `src/kinvoryx/cash_inflow.py`, validation and rendering modules

The successful order was: deterministic core, validation harness, interface/export,
then governed pilot readiness. Future work should preserve this order when adding
new decision types: prove the calculation and validation evidence before making
the artifact feel productized.

## MEM-S011-20260808-002 - Validate Consistency, Not Advice Quality

- **Scope:** validation
- **Type:** pattern
- **Status:** active
- **Confidence:** high
- **Evidence:** `src/kinvoryx/cash_inflow_validation.py`, `tests/test_cash_inflow_validation.py`

Golden cases and property sweeps verify internal consistency: cash conservation,
category caps, debt caps, scenario coverage, and expected metric differentiation.
They do not prove a plan is right for a real household.

## MEM-S011-20260808-003 - Never Crown A Winner In Spec 011

- **Scope:** rendering
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `src/kinvoryx/cash_inflow_rendering.py`, `tests/test_cash_inflow_rendering.py`

The artifact should compare alternatives without using terms such as recommended,
optimal, best, selected, or execute. This is part of the product boundary, not
just copy polish.

## MEM-S011-20260808-004 - Reviewer Notes Gate Readiness, Not Math

- **Scope:** reviewer annotations
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `ReviewerAnnotation`, `unresolved_pilot_blockers`

Reviewer annotations are structured review evidence. Open high/blocker annotations
block pilot readiness, but they do not change the deterministic calculation unless
they identify a calculation defect that then flows back into the spec/code.

## MEM-S011-20260808-005 - Rendering Is Not A Second Engine

- **Scope:** rendering
- **Type:** pitfall
- **Status:** active
- **Confidence:** high
- **Evidence:** `BriefRenderContext`, household/reviewer rendering tests

Renderers must consume `HouseholdCase`, `DecisionBrief`, and optional validation
evidence. They should format values and disclosures, not recompute allocations,
scenario impacts, or metric leadership.

## MEM-S011-20260808-006 - Keep Manual Entry Synthetic And Local

- **Scope:** interface
- **Type:** pattern
- **Status:** active
- **Confidence:** high
- **Evidence:** `src/kinvoryx/cash_inflow_interface.py`, interface demo script

The local manual-entry interface is useful for demos because it has no extra
runtime dependencies and keeps the safety boundary visible. Do not add real data,
account connectivity, persistence, or production submission workflows until Slice
D defines governance, privacy, audit, and human review.

## MEM-S011-20260808-007 - Governance Evidence Must Fail Closed

- **Scope:** governed pilot readiness
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `src/kinvoryx/cash_inflow_governance.py`, `tests/test_cash_inflow_governance.py`, Spec 011

Pilot readiness is a conjunction, not a score. Reviewed jurisdiction coverage,
privacy/security controls, deterministic validation, human approval, and resolved
high-severity annotations must all pass. Audit records retain hashes and metadata,
not a second copy of raw case data.

## MEM-S011-20260808-008 - Gate The Evidence Graph, Not Summaries

- **Scope:** governed workflow lineage
- **Type:** decision
- **Status:** active
- **Confidence:** high
- **Evidence:** `docs/specs/012-governed-decision-brief-workflow.md`, `src/kinvoryx/cash_inflow_governance.py`, `tests/test_cash_inflow_governance.py`

Pilot readiness must be derived from one retained, case-bound evidence graph.
Boolean validation flags, annotation counts, and asserted review states lose
lineage and permit evidence from different calculations to be mixed. Fingerprint
each evidence node in the metadata-only audit record and recheck those bindings at
the gate.
