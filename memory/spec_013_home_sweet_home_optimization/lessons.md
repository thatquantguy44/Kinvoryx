# Spec 013 Home Sweet Home Lessons

These are metadata-only pointers to the specification and user-confirmed product
scope. They contain no real household inputs, private destinations, listing rows,
or credentials. Specs remain authoritative. Record provenance and pseudonymous
attribution are maintained in [index.yaml](index.yaml).

## MEM-HOME-20260927-007 — Source Benchmark Is Implemented

- **Scope:** spec_013_source_benchmark_implementation
- **Type:** validation
- **Statement:** A metadata-only zero-dollar source benchmark now exists for
  Spec 013, with source contracts, a CLI runner, a runbook and six fictional
  DC-area profiles.
- **Evidence:** [source-check runbook](../../docs/runbooks/home-sweet-home-source-check.md), [housing source contracts](../../src/kinvoryx/housing_sources.py), [fictional DC profiles](../../data/home_sweet_home/dc_benchmark_profiles.json), September 27 local run.
- **Confidence:** high for runner execution and metadata evidence; no listing
  coverage, route correctness or recommendation readiness implied.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-27

The source check retained no raw API payloads, listings, addresses, keys or real
household data. The run produced 10 successful probes and one warning: WMATA
station predictions returned HTTP 401 without a key while the keyed request
succeeded. Trellistate responded but returned an empty tiny DC listing sample, so
listing coverage remains unproven. Python HTTPS uses Certifi for verified TLS;
do not disable certificate verification to make source probes pass.

## MEM-HOME-20260927-006 — Preserve Free Supporting-Variable Sources

- **Scope:** spec_013_zero_budget_supporting_sources
- **Type:** decision
- **Statement:** Track additional free/public sources beyond listings for the
  DC-area benchmark, including Census/ACS, LODES, BLS, USAJOBS, WMATA/GTFS, OSM,
  local open data, FEMA, NWS/NOAA, AirNow, FCC broadband, NCES, childcare
  datasets, Zillow Research and Redfin Data Center.
- **Evidence:** [Spec 013 source table](../../docs/specs/013-home-sweet-home-optimization/spec.md), [DC-area evidence table](../../docs/specs/013-home-sweet-home-optimization/dc-area-pilot.md), September 27 user request.
- **Confidence:** high for source-candidate preservation; source suitability remains untested.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-27

Treat these as supporting evidence for area context, jobs, transit, hazards,
broadband, education metadata, childcare and amenities. They do not establish
live listing coverage, school assignment, unit-level broadband, childcare
availability, health impact, insurability or a complete recommendation.

## MEM-HOME-20260927-005 — Exclude RentCast From the Required $0 Path

- **Scope:** spec_013_zero_budget_source_plan
- **Type:** decision
- **Statement:** The first DC-area live-data source test still uses a $0 budget,
  but RentCast is excluded from the required setup unless a no-payment,
  no-overage path is verified.
- **Evidence:** [DC-area source plan](../../docs/specs/013-home-sweet-home-optimization/dc-area-pilot.md), [local example config](../../config/home_sweet_home.sources.example.yaml), September 27 user correction.
- **Confidence:** high for source-budget decision; not a judgment on RentCast data quality.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-27

Use Trellistate as the no-key public listing probe and manual authorized
candidates for listing normalization. WMATA is free of charge; test no-key/public
surfaces first and use the portal key only where an endpoint requires it. Use
USAJOBS only after user-created keys are provided or locally configured. Treat
RentCast as excluded from the strict zero-dollar path because its official API
docs describe a free monthly allowance with overage fees; revisit only if a
no-payment, no-overage setup is proven.

## MEM-HOME-20260927-004 — First Live Source Budget Is Zero Dollars

- **Scope:** spec_013_zero_budget_source_plan
- **Type:** decision
- **Statement:** The first DC-area live-data source test uses a $0 budget:
  public APIs, no-key reads and free developer quotas only.
- **Evidence:** [DC-area key setup and listing path](../../docs/specs/013-home-sweet-home-optimization/dc-area-pilot.md), [engineering quota guards](../../docs/specs/013-home-sweet-home-optimization/engineering-handoff.md), September 27 user direction.
- **Confidence:** high for budget and intended source path, not source coverage.
- **Status:** superseded by MEM-HOME-20260927-005 on 2026-09-27
- **Access level:** repo
- **Date:** 2026-09-27

This record incorrectly treated RentCast as a usable zero-dollar listing probe.
The user corrected that RentCast costs money; MEM-HOME-20260927-005 supersedes
the setup path and removes RentCast from required keys/config.

## MEM-HOME-20260927-003 — Live Source Research Is the Next Milestone

- **Scope:** spec_013_live_source_research
- **Type:** decision
- **Statement:** The user selected a limited live-data test; the earlier
  synthetic-only-first proposal is superseded by DEC-HOME-012. Source evidence
  and household-profile origin must remain independently labeled.
- **Evidence:** [DC-area live-data milestone](../../docs/specs/013-home-sweet-home-optimization/dc-area-pilot.md), September 27 user direction and direct source-check record.
- **Confidence:** high for user direction and observed check, not market coverage.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-27

A read-only metadata/count/five-ID-status check of public DC address data passed;
it does not validate live listings, VA/MD coverage, school access or rankings.
No raw rows or household data were retained. The Python client failed certificate
verification in this session; system curl succeeded with TLS verification on.
Revalidate runtime trust setup before building an adapter, rather than disabling
certificate verification. Existing private-household guards remain in force.

The spending input for this milestone is now resolved by MEM-HOME-20260927-004:
$0 for the first source test.

## MEM-HOME-20260926-001 — Preserve the Full Confirmed Decision

- **Scope:** spec_013_confirmed_product_scope
- **Type:** decision
- **Statement:** Support buying and renting, both integrated and standalone use,
  detailed optional education, additional job access, and area recommendations
  down to towns/neighborhoods/street segments before individual homes.
- **Evidence:** [Spec 013 decision register](../../docs/specs/013-home-sweet-home-optimization/spec.md), user clarifications in the September 26, 2026 source session.
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
- **Status:** superseded by MEM-HOME-20260927-001 on 2026-09-27
- **Access level:** repo
- **Date:** 2026-09-26

Do not revert to the earlier suggested Raleigh–Durham/Denver mix. No previous
committed record contained that suggestion, so no supersession record is needed.
District source leads are not complete metro coverage or API rights. Every region
and capability needs independent readiness evidence.

The September 27 user message confirms DC/VA/MD as the first focus. The roster
remains valid, but this record's blanket characterization of activation order as
proposed is superseded. The previous Boston/Chicago/Austin-first proposal must
not drive implementation sequencing.

## MEM-HOME-20260926-003 — Keep Geographic and Evidence Precision Honest

- **Scope:** spec_013_evidence_precision
- **Type:** decision
- **Statement:** Area discovery, address feasibility, school enrollment, and job
  opportunity are separate evidence contracts.
- **Evidence:** [Spec 013 sections 9–11](../../docs/specs/013-home-sweet-home-optimization/spec.md), REQ-HOME-009/019/025/026.
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

## MEM-HOME-20260927-001 — DC and Surrounding VA/MD Come First

- **Scope:** spec_013_pilot_region_roster
- **Type:** decision
- **Statement:** Preserve the ten-region roster and prioritize HOME-REG-003;
  detailed core/outer-ring boundaries and later activation waves remain proposals.
- **Evidence:** [Spec 013 DEC-HOME-011](../../docs/specs/013-home-sweet-home-optimization/spec.md), user preference in the September 27 source session.
- **Confidence:** high for first-region priority; no footprint or launch approval implied.
- **Status:** active; supersedes MEM-HOME-20260926-002
- **Access level:** repo
- **Date:** 2026-09-27

Detailed data integrations and synthetic regional cases for the other nine
regions do not block DC work. Keep all ten registry identities with explicit
inactive/unsupported gates; validate each region before its eventual admission.

## MEM-HOME-20260927-002 — Make the First Regional Journey Testable

- **Scope:** spec_013_dc_area_planning
- **Type:** decision
- **Statement:** The proposed DC companion concentrates on a complete search
  journey, local source feasibility, concrete preference questions and twelve
  benchmark cases mapped to existing acceptance criteria.
- **Evidence:** [DC-area pilot companion](../../docs/specs/013-home-sweet-home-optimization/dc-area-pilot.md), primary-source leads researched September 27.
- **Confidence:** high for documented proposal; no runtime validation or vendor rights asserted.
- **Status:** active
- **Access level:** repo
- **Date:** 2026-09-27

Postal locality, governing jurisdiction and school authority cannot be one field.
Academic year and adopted boundaries must be explicit. Route windows and actual
worksites drive access; job postings, remote arrangements and historical
employment remain distinct. Source leads and proposed sample counts are not
evidence that these controls or coverage already work.
