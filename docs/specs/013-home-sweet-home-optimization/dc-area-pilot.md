# Home Sweet Home — Washington DC Area First Pilot

**Parent:** [Spec 013](spec.md)\
**Date:** September 27, 2026\
**Region:** HOME-REG-003\
**Status:** DC and surrounding Virginia/Maryland confirmed as first focus; detailed footprint and execution proposal remain under review\
**Scope:** Buying and renting; standalone and connected-finance modes; education, additional jobs, and town-to-street discovery\
**Related:** [Ten-region roadmap](pilot-regions.md), [Engineering handoff](engineering-handoff.md)

## 1. Planning improvements and first outcome

The broad specification already defines the feature set. The next improvement is a small, complete regional workflow with evidence we can inspect:

> Given a budget, property needs, work/care destinations, education interests and job-access preferences, identify 3–7 DC-area places worth exploring, narrow selected places to supported street segments, and compare 2–6 actual or synthetic homes with explicit costs and unknowns.

This is a proposed first useful demonstration, not an approved live pilot. It preserves the eventual Spec 013 scope while concentrating research, source validation and implementation sequencing on one region. The other nine regions remain on the roadmap; their data integrations and local audits do not block learning in DC.

Five improvements should precede substantial engineering:

1. **Freeze a bounded first geography.** Resolve authoritative jurisdiction, school system and geometry separately from town or postal names.
2. **Prove the data path.** Establish what can actually be obtained, retained, transformed and displayed for both sale and rental inventory, education, routes and jobs.
3. **Test preference elicitation.** Ask concrete budget/time/space trade-offs, show their effects, and require confirmation before turning them into constraints or weights.
4. **Build a local benchmark.** Retain challenging synthetic cases and independent source checks before optimizing a score or designing a large map interface.
5. **Deliver one complete search journey.** Area recommendation → street exploration → candidate comparison → verification checklist, with visible data limitations at each step.

### Immediate milestone: limited live-data test

The user selected live-data testing on September 27 (DEC-HOME-012). Advance
permitted source feasibility checks before waiting for the synthetic journey to
be built. Retain synthetic correctness fixtures in the engineering work. This is
an internal research milestone, not a consumer launch or a completed housing
recommendation engine.

Use public or explicitly permitted provider data and fictional household profiles
as the initial test design. Record actual source timestamps, jurisdiction, rights,
coverage and missingness; never label live source records as synthetic. Preserve
the existing finance prototype's real-household guard. No financial accounts,
dependent records or private work/home destinations are necessary for this source
test, and no provider purchase or external outreach is authorized by this choice.

| Dependency | What is needed | Work that can proceed now |
|---|---|---|
| Property listings | Zero-dollar source path: public read APIs, free developer quotas or manual authorized candidates | Test Trellistate public reads, RentCast free developer quota if an account/key is created, and manual candidate normalization; do not claim a complete active listing universe |
| Transit/jobs | Credentials for selected authenticated feeds; WMATA and USAJOBS document API-key requirements | Public documentation/source-shape checks and unauthenticated sources where available; prepare key setup steps |
| Routing | A selected permitted routing service, self-hosted/open-source routing stack, or explicit manual route estimates | Define origin/destination/time-window tests; a transit schedule alone is not door-to-door routing |
| Budget | User set the source budget to $0 for the first live-data test | No-cost read-only source checks only; configure hard caps and stop on exhausted free quotas or any required payment |
| Test profile | Fictional budget/preferences for source/engine testing; actual preferences only when intentionally supplied | Use synthetic profile fixtures without collecting personal household data |

Current evidence: a direct HTTPS smoke check of the DC Address Points service at
`2026-09-27T16:21:23Z` successfully queried metadata, a feature count and five
records restricted to ID/status fields. The service reported 144,426 features;
the five IDs were non-null and distinct, with status `ACTIVE`. No raw rows or
address payloads were retained. This validates limited connectivity/schema use,
not listing availability, field freshness, geographic completeness, school
assignment or housing recommendations. [DC GIS service](https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/0)

The initial Python HTTPS client failed certificate-chain verification. The same
check succeeded using the macOS system curl client with certificate verification
enabled. Resolve the runtime's trusted certificate configuration before a Python
adapter uses this source; do not disable TLS verification.

Still untested: live property listings, authenticated WMATA/USAJOBS feeds,
door-to-door routes, Virginia/Maryland source samples and cross-source joins.
The next evidence report should test a small permitted buy/rent sample across
DC/VA/MD for identity, costs, source age, school-year lookup and route/job joins,
with explicit blocked fields and no passing status inferred from missing data.

Zero-dollar listing path: use [Trellistate public listing search](https://trellistate.com/docs)
as a no-key public-read probe and [RentCast](https://help.rentcast.io/en/articles/7992900-rentcast-property-data-api)
as a small keyed free-quota probe if the user creates a developer account. RentCast
documents a free developer plan with 50 API requests/month and property listing
endpoints for sale and long-term rental listings; the first adapter must enforce
a local request cap below the free quota and disable overage or paid plans.
Trellistate documents public read endpoints, rate limits and attribution
expectations; because it is a user-submitted public listing exchange, coverage,
accuracy and DC-area inventory must be measured, not assumed. Bright MLS remains
a later licensed-source investigation rather than the $0 listing path.

## 2. Proposed geographic scope

DC-first is confirmed. Exact boundaries below are a proposed starting assumption, not a user-approved coverage promise.

| Stage | Property search geography | Admission condition |
|---|---|---|
| Core | District of Columbia | Valid address/geography, cost, education, source-rights and travel coverage |
| Core — Virginia | Arlington County, Fairfax County, and the independent cities of Alexandria, Fairfax and Falls Church | Each jurisdiction verified independently; incorporated towns and postal aliases retained |
| Core — Maryland | Montgomery County and Prince George's County | Municipal boundaries, school evidence and local costs resolved independently |
| Next expansion | VA: Loudoun and Prince William counties, plus separate Manassas/Manassas Park city review; MD: Howard, Anne Arundel and Frederick counties | Add after core-source and route validation; confirm the user's desired outer ring before expansion |

These eight core jurisdictions form one regional search, not eight additional pilot regions. All three state/district areas must be represented in the first regional evaluation. A capability may remain pending in a particular jurisdiction; do not describe that gap as complete DC-area coverage. Travel and job destinations may lie outside the property footprint, with destination-source coverage disclosed separately.

Store administrative locality, municipality, postal city, neighborhood, school authority, tax authority and source geography as different relationships. A mailing label cannot select the school or tax rules. Alexandria explicitly notes that some Alexandria postal addresses are in Fairfax County. [City of Alexandria locality guidance](https://alexandriava.gov/taxes/tax-guide-for-new-city-residents)

Fairfax City also illustrates why one jurisdiction is not necessarily one independent school-operation dataset: FCPS describes its operational relationship to city schools. Verify the actual service/assignment mapping rather than deriving it from a county-name match. [FCPS City of Fairfax School Board](https://www.fcps.edu/committee/city-fairfax-school-board)

## 3. First experience and preference design

The opening screen asks about the decision, not a favorite listing portal:

- Buy, rent, or compare both; move window; expected stay; property/space requirements.
- Monthly housing envelope and available move/down-payment cash, with an option to leave unknown fields explicitly unknown.
- Each adult's actual destination, arrival/departure window, acceptable modes, onsite days, and maximum tolerable commute. Use private labels; employer identity is optional.
- Optional grade/year, programs, childcare hours, and willingness to consider application-based education routes. Keep required access distinct from a preference.
- Optional job categories, industries or preferred employer sites and travel budgets for additional opportunities.
- Must-haves, flexible preferences and separate member vetoes. No prefilled definition of the “best” town.

Use a few concrete preference comparisons: “Would an additional $300/month be worth saving 20 minutes on each commuting day?” and “Would you trade a bedroom for a shorter trip?” These are elicitation examples, not recommended prices or universal conversions of time to money. Keep money and time separate in the result; only confirmed answers adjust a preference profile. A user can skip trade-off questions and use raw metric comparisons.

The area result shows reasons, trade-offs and evidence coverage, then lets the user pin several areas. A map pan does not change the search universe. Explain why an otherwise appealing area was not selected. A street result identifies segment endpoints and source resolution; school access and property feasibility are checked again for the chosen address. If evidence cannot support a precise street recommendation, retain useful area guidance and state the missing evidence.

For research only, use candidate examples across DC neighborhoods, Arlington corridors, Alexandria, Falls Church, Fairfax/Vienna/Reston, Bethesda/Rockville/Silver Spring, and College Park/Hyattsville/Bowie. These names define a diverse test set, not recommendations or validated commute/cost claims. Represent neighborhood, town, city and unincorporated-place semantics accurately. Do not select only higher-priced or familiar areas, and do not require a school preference to obtain useful results.

## 4. Regional evidence and source investigation

The following are primary-source leads reviewed on September 27, 2026. Their existence does not establish bulk access, licensing, completeness, implemented adapters, or tested answers. Source selection remains open, and no paid plan or account has been acquired.

| Capability | Evidence lead | Next investigation / deliverable |
|---|---|---|
| Listing discovery | $0 path: [Trellistate public listing API](https://trellistate.com/docs), [RentCast API setup](https://help.rentcast.io/en/articles/7992900-rentcast-property-data-api), [RentCast listing endpoints](https://developers.rentcast.io/reference/property-listings). Later licensed path: [Bright MLS developer portal](https://brightmls.portal.swaggerhub.com/) | For $0 testing, inspect a tiny permitted buy/rent sample, source age, fields, duplicate IDs, rights, attribution, and free-quota controls. Treat Trellistate as public/user-submitted coverage and RentCast as quota-limited provider coverage. Evaluate Bright MLS separately for licensed sale/rental access, necessary commercial relationship, permitted derived area summaries and exports. |
| Address/geography | [DC GIS address-point layer](https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Location_WebMercator/MapServer/0) plus locality GIS for VA/MD | Versioned polygons and address precision; rights/joins review. DC data does not validate Virginia or Maryland addresses. |
| Metro travel | [WMATA developer resources](https://www.wmata.com/about/developers.html), [license](https://developer.wmata.com/license) | Confirm key/license requirements, schedules, alerts, accessibility status and permitted caching. The feed is an input to route planning, not a full household door-to-door routing engine. |
| Regional/local transit | [Maryland MTA developer resources](https://www.mta.maryland.gov/developer-resources), [Virginia DRPT feed registry](https://drpt.virginia.gov/data/gtfs-feed-clearinghouse/) | Audit MARC/VRE and applicable local bus operators, active dates and modes. Keep unsupported connections explicit. |
| Current federal jobs | [USAJOBS Search API](https://developer.usajobs.gov/api-reference/get-api-search) | Authenticated announcement feed, source terms, worksite/remote fields, closing date and deduplication. It covers federal announcements, not the entire regional job market. |
| Broader job access | [Census LODES](https://lehd.ces.census.gov/data/lehd-code-samples/sections/lodes.html), [BLS occupation context](https://www.bls.gov/OES/current/oessrcma.htm), separately licensed current postings | Distinguish historical industry employment, regional wage context, employer sites and live openings. Identify current private/nonprofit/local-government coverage gaps. |
| Local cost | Local assessor/collector sources; example [Fairfax tax categories](https://www.fairfaxcounty.gov/taxes/node/295); actual lease/HOA and insurance evidence | Build jurisdiction-specific cost checklists, including property/municipal costs, vehicle ownership costs where applicable, parking, tolls, fees and childcare. No copied tax-rate defaults or automatic legal eligibility. |
| Environment/property | Parent Spec 013 official hazard leads plus condition/insurance evidence | Verify scale, vintage and exact address applicability; never infer insurability or indoor conditions from an area layer. |

Each source investigation produces a small evidence card: provider and authoritative domain; grain/keys; coverage; freshness; historical availability; rights for ingestion, cache, derivatives and exports; technical access; expected query spend; sample validation; owner; blockers and fallback. A lookalike domain or reseller claim is not treated as the provider's own terms. Model a denied API request, rights revocation and budget exhaustion before adopting an adapter.

### Key setup links for the $0 live test

These are account setup links for source research, not authorization to store
secrets in the repo or to exceed free plans.

| Source | Why we need it | Setup link |
|---|---|---|
| RentCast | Small sale/rental listing sample under the free developer quota | [RentCast API dashboard](https://app.rentcast.io/app/api) and [getting-started guide](https://help.rentcast.io/en/articles/7992900-rentcast-property-data-api) |
| WMATA | Official Metro schedule, real-time and accessibility feed access | [WMATA developer resources](https://www.wmata.com/about/developers.html), [developer portal](https://developer.wmata.com/), and [registration link](https://developer.wmata.com/signup) |
| USAJOBS | Current federal job announcements for additional-job access tests | [USAJOBS API request form](https://developer.usajobs.gov/apirequest/index) and [authentication guide](https://developer.usajobs.gov/guides/authentication) |

Trellistate public reads do not require a key. If we need write actions or agent
inquiries later, those are outside the first read-only source test. Routing can
begin with manual estimates or open-source tooling such as OpenTripPlanner over
GTFS/OpenStreetMap; a commercial routing key is not selected for the $0 test.

## 5. Education deserves a regional rule map

| System | Source lead | Distinction to validate |
|---|---|---|
| DC | [My School DC search tools](https://www.myschooldc.org/node/29536), [application guidance](https://www.myschooldc.org/node/65) | In-boundary, grade-specific right-to-attend, charter/out-of-boundary choice, pre-K, feeder and program routes are separate states. |
| Fairfax County / relevant Fairfax City mapping | [FCPS locator entry](https://www.fcps.edu/schools-centers), [boundary changes](https://www.fcps.edu/facilities-planning-future/school-boundary-adjustments) | Current versus adopted future boundaries, address precision, programs and target academic year. |
| Arlington | [APS boundary and registration guidance](https://www.apsva.us/registration/realtor/) | Neighborhood attendance versus optional program/transfer route; border-address resolution. |
| Alexandria City | [ACPS schools/locator](https://www.acps.k12.va.us/about-us/schools) | Select the target school-year boundaries explicitly; distinguish city addresses from postal aliases. |
| Falls Church City | FCCPS source investigation still required | Verify exact residency geography, registration and program rules; do not substitute FCPS based on the postal name. |
| Montgomery County | [MCPS enrollment and assignment tools](https://www.montgomeryschoolsmd.org/info/enroll/) | Address-based school lookup, choice/program exceptions, effective year and future boundary changes. |
| Prince George's County | [PGCPS School Finder](https://gis.pgcps.org/schoolfinder/findschool2.asp) | Address, academic year and school/program assignment; preserve unresolved cases. |

ACPS currently publishes school-year-specific locator guidance. Treat that as a concrete regression case: retrieving a page today does not make the displayed year's assignment appropriate for a future move. [ACPS boundary information](https://www.acps.k12.va.us/families/school-boundaries)

School metrics remain optional and retain source/year/context; do not compare state test percentages as if they share a single scale. Childcare must include hours, travel, prices and seat/waitlist uncertainty. Source identity, program eligibility, admission, transport eligibility, and actual enrollment remain separate. The household sees a short verification checklist, not a falsely definitive “best school” label.

## 6. Commute, job and cost cases to model

Evaluate actual travel windows and both directions, including walk/wait/transfer/parking time, toll/fare assumptions, service calendars and accessibility limitations. Proposed stress cases include 1/3/5 onsite days, an earlier arrival, later departure, missed connection, loss of a usable accessible route, school/childcare pickup deadline, and disruption of a river-crossing route. These are scenarios; no arbitrary delay becomes a measured percentile or a current traffic claim.

For two-adult households, retain separate workplace and future-job-access sets. Test downtown DC, Arlington, Tysons/Reston and Maryland destination clusters as search inputs rather than declaring the region a single employment center. Exact worksite matters. A job posted under a broad regional label is not a verified street destination, and remote/telework terms are not interchangeable. Posting qualification, clearance or hiring-path requirements may be displayed as sourced job attributes; do not collect sensitive identity data or decide the user's eligibility.

Costs should be compared in three visible layers: housing cash costs, location-induced transport/childcare costs, and optional verified household-finance effects. Include separately verified vehicle costs where applicable and actual lease/condo terms. A cross-border comparison with unmodeled income taxes must say that after-tax effects are not assessed; it cannot claim complete financial superiority. A separately confirmed user estimate can be modeled as an assumption. Comprehensive jurisdictional income-tax optimization remains outside Spec 013's first release.

## 7. Executable research sequence

These are proposed checkpoints under existing tasks and gates, not new requirements or evidence of completion. No product implementation starts before parent extension/spec admission. Under DEC-HOME-012, read-only live-source feasibility from DC-CP-03 begins during DC-CP-01; the full validation benchmark and pilot still depend on their required controls.

| Checkpoint | Deliverable | Existing tasks / acceptance | Exit evidence |
|---|---|---|---|
| DC-CP-01 — Scope and evidence feasibility | Core geography, jurisdiction-school map, source cards, first user tasks and budget estimate | T-HOME-001/008/009/018; AC-HOME-004/005/018/019/024 | Named owners, explicit coverage gaps and rights/cost decision; core vs outer ring reviewed |
| DC-CP-02 — Synthetic complete journey | Preferences → areas → segments → buy/rent comparisons → verification brief | T-HOME-002–014; AC-HOME-001–016/025/026 | Reproducible synthetic examples across DC/VA/MD; no critical unknown promoted to pass; accessible non-map path |
| DC-CP-03 — Permitted source benchmark | Address, school, travel, listing and job evidence with independent checks | T-HOME-008–013/018; AC-HOME-004–010/018/019/025/026 | Parent sampling floors met and local edge cases below covered; supplier rights and retention verified |
| DC-CP-04 — Controlled regional pilot | Private workspace, consent, cost caps, approved sources and monitored flow | T-HOME-015–019; AC-HOME-017/020–024/029–034 | GATE-HOME-3 passes for enabled jurisdictions/capabilities; accountable review and rollback drill |
| DC-CP-05 — Expansion decision | Core outcomes, missing needs, source costs, outer-ring and other-region priorities | T-HOME-018/019; AC-HOME-024 | Documented continuation/repair/stop decision; no automatic expansion from engagement alone |

Within the prototype, obtain useful feedback on area discovery before adding automated alerts or polishing every possible layer. That is a build order, not removal of confirmed education, jobs, buying/renting, or connected-mode requirements. A narrowed research demo is labeled as such and does not claim the full first release is complete. Live private data still requires the parent privacy and governance foundation.

## 8. Local benchmark and readiness evidence

Start with 12 synthetic search profiles: two profiles for each DC/VA/MD × buy/rent combination. Vary education on/off, childcare timing, single versus multiple adults, car/transit/accessibility needs, budget, move year, and current/future job access. Include mixed-tenure comparisons as additional scenarios. Profiles exercise preferences without representing demographic target groups or real households.

Use the parent 20-sale/20-rental source-review minimum for the region, distributed across all claimed core jurisdictions; disclose property/type/source gaps. School checks must meet both the parent minimum of 20 and at least three checks per supported school authority, including boundary/year/program exceptions. Retain at least 30 route checks spread across enabled modes, travel windows and DC/VA/MD origin-destination pairs; not every possible route is thereby validated. Audit at least ten area and ten street-segment results under the parent rules. Inspect at least 20 current postings if that capability is enabled; federal-only coverage remains labeled federal-only.

| Local case ID | Scenario | Existing acceptance criteria |
|---|---|---|
| HOME-DC-CASE-01 | Same Alexandria mailing label, different actual locality | AC-HOME-004/009/019 |
| HOME-DC-CASE-02 | Fairfax City and County identities with explicit school-service mapping | AC-HOME-004/009/018 |
| HOME-DC-CASE-03 | Falls Church postal alias versus Falls Church City school authority | AC-HOME-004/009 |
| HOME-DC-CASE-04 | DC in-boundary K–12 question versus pre-K/application-based option | AC-HOME-009/011 |
| HOME-DC-CASE-05 | Current-year versus future-year ACPS/other adopted boundary evidence | AC-HOME-009/019 |
| HOME-DC-CASE-06 | Attractive geographic distance but infeasible cross-river/time-window trip | AC-HOME-008/011/013 |
| HOME-DC-CASE-07 | Two adults with opposing current commute and additional-job priorities | AC-HOME-014/025 |
| HOME-DC-CASE-08 | Metro proximity but missing accessible first/last leg or schedule coverage | AC-HOME-008/010/011 |
| HOME-DC-CASE-09 | Historical jobs plus duplicate federal posting, broad worksite and remote role | AC-HOME-019/025 |
| HOME-DC-CASE-10 | Housing appears cheaper until verified parking, fees, vehicle/childcare costs | AC-HOME-006/007/013 |
| HOME-DC-CASE-11 | Sparse street inventory and opposite-side school boundary | AC-HOME-009/026 |
| HOME-DC-CASE-12 | Important unknown survives town-to-street-to-address drill-down | AC-HOME-015/026/028 |

For each case retain expected behavior, evidence or synthetic fixture, evaluator, result, issue and disposition. Zero completed cases are claimed here. Existing cost reconciliation, source-rights, privacy, fairness, accessibility, performance and stop gates still apply.

## 9. Decisions remaining and completion status

Immediate product choices: approve the core/outer-ring footprint; choose a first research cohort spanning buyers and renters; choose concrete default questions and comparison labels; and assign accountable roles. The first source-investigation spending limit is $0. Recruitment should include DC, Virginia and Maryland users, people with and without school needs, and multiple transport modes without requiring collection of protected traits.

The user has chosen live-data testing as the immediate milestone and selected a
$0 source budget. The first source decision is whether public/free listing,
transit, job and routing paths can support a useful source benchmark without
paid access. Limited live-source checks can proceed while the synthetic engine is
being specified; neither one-source connectivity nor a manual/synthetic
prototype establishes live inventory coverage. The first product decision test
is whether users can explain why an area fits, identify a meaningful alternative
and recognize what remains uncertain before touring or applying.

This document records planning improvements, researched source leads and the limited live-source check described above. It does not activate a pilot, sign contracts, contact providers, collect household data, implement product code or approve real-world recommendations.
