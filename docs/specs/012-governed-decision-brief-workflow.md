# 012 Governed Decision-Brief Workflow

**Status:** Draft - initial vertical slice implemented  
**Phase:** 1 governed prototype foundation  
**Depends on:** Specs 002, 003, 006, 007, 008, and 011

## Purpose

The governed decision-brief workflow makes pilot readiness a property of one
retained evidence graph. A caller may not substitute summary booleans or counts
for the validation, annotation, privacy, review, audit, policy, and coverage
records that belong to the calculation under review.

This slice remains synthetic-only. It does not authorize real-household data or
replace accountable domain, privacy, security, or pilot approval.

## Requirements

- **REQ-GDB-001 - Must:** One service shall accept a `HouseholdCase`,
  `GovernedPolicy`, and `JurisdictionCoverage`, run the deterministic calculation,
  and return the calculation with its governed evidence.
- **REQ-GDB-002 - Must:** Validation evidence and reviewer annotations shall name
  the same case and retained calculation; cross-case or cross-calculation evidence
  shall fail closed.
- **REQ-GDB-003 - Must:** Human review evidence shall be an ordered, valid state
  transition chain with unique event identifiers, rather than a caller-supplied
  terminal-state assertion.
- **REQ-GDB-004 - Must:** The audit record shall fingerprint the household input,
  calculation output, validation evidence, annotations, privacy/security review,
  review events, and coverage record, and bind policy and jurisdiction identity.
- **REQ-GDB-005 - Must:** Pilot-gate evaluation shall derive validation status,
  unresolved blockers, privacy/security status, and final review state from the
  retained records. It shall not accept arbitrary readiness booleans or counts.
- **REQ-GDB-006 - Must:** Missing, mismatched, altered, unsupported, incomplete, or
  unapproved evidence shall produce explicit blockers and a closed pilot gate.

## Workflow Contract

`create_governed_decision_brief` is the entry point for governed use:

1. Convert the approved policy to deterministic engine settings.
2. Calculate one `DecisionBrief` from the supplied synthetic case.
3. Validate that retained brief and the supplied annotations without rebuilding a
   second authoritative result.
4. Derive review state from the ordered transition events.
5. Create one metadata-only audit record whose hashes cover every evidence node.
6. Evaluate pilot readiness from the completed `GovernedWorkflowEvidence` graph.

The underlying deterministic builder remains available for engine tests and
ungoverned research, but its output does not carry a pilot gate. Only the governed
service produces a `GovernedDecisionBrief`.

## Acceptance Criteria

| ID | Covers | Criterion |
|---|---|---|
| AC-GDB-001 | REQ-GDB-001, REQ-GDB-005 | A valid, approved evidence chain produces one governed brief whose pilot gate is ready without accepting summary booleans or counts. |
| AC-GDB-002 | REQ-GDB-002, REQ-GDB-004, REQ-GDB-006 | Altering coverage or mixing evidence after calculation causes identity and fingerprint blockers. |
| AC-GDB-003 | REQ-GDB-003, REQ-GDB-006 | Missing, duplicated, or invalid review transitions cannot produce an approved gate. |
| AC-GDB-004 | REQ-GDB-004 | Audit metadata contains hashes and identifiers, not raw duplicate household or brief payloads. |

## Security and Privacy Boundary

The workflow evidence object exists in process for deterministic evaluation. The
audit record is the persistence-safe metadata representation: it stores hashes,
versions, identifiers, jurisdiction, and review state, but not raw household or
decision-brief payloads. Persistence, deletion, access control, and accountable
pilot authorization remain operational work before any real-household pilot.
