# Spec 013 Home Sweet Home Lessons

These are metadata-only pointers to the specification and user-confirmed product
scope. They contain no real household inputs, private destinations, listing rows,
or credentials. Specs remain authoritative. Record provenance and pseudonymous
attribution are maintained in [index.yaml](index.yaml).

## MEM-HOME-20260926-001 — Preserve the Full Confirmed Decision

- **Scope:** spec_013_confirmed_product_scope
- **Type:** decision
- **Statement:** Support buying and renting, both integrated and standalone use,
  detailed optional education, additional job access, and area recommendations
  down to towns/neighborhoods/street segments before individual homes.
- **Evidence:** [Spec 013 decision register](../../docs/specs/013-home-sweet-home-optimization.md), user clarifications in the September 26, 2026 source session.
- **Confidence:** high for scope confirmation, not implementation quality.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-26

Do not reduce the module to ranking listing cards or commuting to the current
employer. The user explicitly wants help discovering where to focus a search and
understanding additional employment opportunities.

## MEM-HOME-20260926-002 — Ten Regions Are Confirmed; Coverage Is Not

- **Scope:** spec_013_pilot_region_roster
- **Type:** decision
- **Statement:** Preserve Boston, New York/North Jersey, Washington DC area,
  Atlanta, Chicago, Austin, Dallas, Seattle, Los Angeles, and San Francisco.
- **Evidence:** [Pilot-region companion](../../docs/specs/013-home-sweet-home-optimization/pilot-regions.md), user-selected roster in the source session.
- **Confidence:** high for membership; footprints/waves remain proposed.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-26

Do not revert to the earlier suggested Raleigh–Durham/Denver mix. No previous
committed record contained that suggestion, so no supersession record is needed.
District source leads are not complete metro coverage or API rights. Every region
and capability needs independent readiness evidence.

## MEM-HOME-20260926-003 — Keep Geographic and Evidence Precision Honest

- **Scope:** spec_013_evidence_precision
- **Type:** decision
- **Statement:** Area discovery, address feasibility, school enrollment, and job
  opportunity are separate evidence contracts.
- **Evidence:** [Spec 013 sections 9–11](../../docs/specs/013-home-sweet-home-optimization.md), REQ-HOME-009/019/025/026.
- **Confidence:** high that the draft requires these distinctions; runtime untested.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-26

A town's sampled travel or cost range cannot validate every address. A street can
cross school/jurisdiction boundaries. School association is not enrollment or
program availability. Historical jobs are not active openings; duplicate, remote,
and unknown-worksite postings need explicit handling. Missing fields remain
unknown, with provisional comparisons and verification tasks.

## MEM-HOME-20260926-004 — A Full Handoff Is Still a Draft

- **Scope:** spec_013_implementation_status
- **Type:** decision
- **Statement:** Documentation defines proposed behavior and validation; no
  housing code, passed acceptance tests, vendor access, or live pilot is implied.
- **Evidence:** [Engineering handoff](../../docs/specs/013-home-sweet-home-optimization/engineering-handoff.md), [master handoff](../../docs/hdi-master-handoff.md).
- **Confidence:** high for documentation status.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-26

The branch was created from main matching fetched origin/main at `f8daefb`.
Existing household and optimizer code remains synthetic. The design must not
reuse federal prototype assumptions as local housing rules, or use cash-inflow
governance approval to validate a different housing result. Spec 010 admission,
spec review, source rights, owners and live-data controls remain future work.
