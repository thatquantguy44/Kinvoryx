# Home Sweet Home — Ten Pilot Regions

**Parent:** [Spec 013](spec.md)\
**Date:** September 27, 2026\
**Status:** Ten regions and DC-area first focus confirmed; detailed footprints, later waves, sources, and thresholds proposed\
**Trace:** REQ-HOME-004, REQ-HOME-009, REQ-HOME-018, REQ-HOME-019, REQ-HOME-024, REQ-HOME-025, REQ-HOME-026

## 1. Confirmed membership and proposed footprints

The user selected Washington DC and surrounding Virginia/Maryland as the first
focus on September 27, 2026. See the [DC-area first-pilot plan](dc-area-pilot.md)
for proposed core/outer-ring boundaries and local source/validation work. This
supersedes the September 26 proposal to start with Boston, Chicago and Austin;
the ten-region membership and stable IDs are unchanged.

These are product pilot boundaries, not claims to match Census metropolitan definitions. County/city membership must become versioned polygons with official geographic identifiers before use. A metro name alone never establishes a covered address. Neighborhoods and school districts require their own geometries. Crossing a region boundary for travel or job access does not silently enable property recommendations outside it.

Both buying and renting are in scope for every region. All ten start in `research_only`; no listings license, complete school coverage, routing service, local-rule review, or job-posting feed has been secured by writing this document. Proposed footprints may be narrowed transparently if source rights or validation cannot support them. Changing the user's ten-region membership requires a product decision, not an automatic fallback.

| ID | Confirmed region | Proposed initial property-search footprint | Product cases to test, not claims of market attractiveness |
|---|---|---|---|
| HOME-REG-001 | Boston | MA: Suffolk, Middlesex, Norfolk, Essex counties | Town-to-city search, regional transit, city choice versus suburban assignment, property carrying costs |
| HOME-REG-002 | New York/North Jersey | NY: five NYC borough counties and Westchester; NJ: Bergen, Essex, Hudson, Morris, Passaic, Union | Cross-state destinations and costs, unit identity, rent concessions, multiple enrollment systems |
| HOME-REG-003 | Washington DC area | DC; MD: Montgomery, Prince George's; VA: Arlington and Fairfax counties, independent cities Alexandria, Fairfax, Falls Church | Multi-jurisdiction travel, town/independent-city identity, separate adult destinations, current versus future school boundaries |
| HOME-REG-004 | Atlanta | GA: Fulton, DeKalb, Cobb, Gwinnett, Clayton | City-versus-district boundaries, time-of-day travel, household destinations and education access |
| HOME-REG-005 | Chicago | IL: Cook, DuPage, Lake | City/neighborhood/suburb comparisons, rail versus car scenarios, tax and recurring-cost variation |
| HOME-REG-006 | Austin | TX: Travis, Williamson, Hays | Job-site/industry access, purchase-cost assumptions, school district overlap and commute sensitivity |
| HOME-REG-007 | Dallas | TX: Dallas, Collin, Denton, Rockwall | Multiple employment centers, employer-site accuracy, district/city mismatch, rental/ownership costs |
| HOME-REG-008 | Seattle | WA: King, Snohomish, Pierce | Cross-water routes, mode-dependent travel, distinct job centers, street-level access variation |
| HOME-REG-009 | Los Angeles | CA: Los Angeles County | Multiple municipalities and employment centers, street/segment identity, school routes and insurance uncertainty |
| HOME-REG-010 | San Francisco | CA: San Francisco, San Mateo, Alameda, Contra Costa, Marin, Santa Clara counties | Bay-area town/corridor alternatives, bridges and transit, industry/job access, enrollment versus attendance-area distinction |

Explicit boundary notes: Boston does not automatically include New Hampshire or Rhode Island; New York does not automatically include Connecticut, Long Island beyond NYC, or all New Jersey; DC does not initially include all outer commuting counties; Chicago excludes Indiana/Wisconsin; Dallas treats Tarrant/Fort Worth as possible destinations but not initial property coverage; Los Angeles does not automatically include Orange/Riverside/San Bernardino counties. San Francisco's proposed footprint is a broad Bay Area test region, including South Bay; confirm that breadth before source procurement. These are reviewable footprint choices, not omissions from the confirmed ten-market list.

## 2. Area recommendation coverage

Each region registry must enumerate supported municipalities/places and attach independent neighborhood and street-network layers. Names are search aliases; geometry IDs are the join keys. Town recommendations may use municipal boundaries or a clearly labeled comparable geography where no town government exists. Unincorporated areas stay searchable rather than disappearing for lack of a city ID.

For each region, prepare at least five synthetic area candidates that differ in cost, education-access evidence, travel, job access, and inventory, plus at least two overlapping neighborhoods and two street segments with the same name in different municipalities. Include an opposite-side school-boundary case and a segment spanning two jurisdictions. These are validation fixtures; no actual town is declared preferred until a user's objectives and permitted source evidence are available.

The production coverage record distinguishes:

- Geometry coverage and source resolution.
- Area cost summaries, their tenure/property mix, vintage, and sample support.
- Route coverage from sampled residential origins by mode and time window.
- Education and childcare discovery versus verified address/year access.
- Historical industry employment, employer locations, and active job postings as separate capabilities.
- Property-level listings, fees, cost inputs, and status freshness.

Do not advertise “street-level intelligence” if only city/ZIP data exists. The UI may still identify a street on a map while labeling its decision evidence as area-level and unverified for the exact segment.

## 3. Initial education source leads

These official resources were located during September 26, 2026 research. They are initial discovery/review leads, not validated API integrations, redistribution permissions, or proof of region-wide coverage. Each lead covers only its own district/system. Every additional district within a pilot footprint needs a separately reviewed source and target-year policy.

| Region | Primary-source lead | Specific check required |
|---|---|---|
| Boston | [Boston Public Schools registration and eligibility](https://www.bostonpublicschools.org/enrollment/welcome-services/registration) | Preserve choice/eligibility distinctions; do not extrapolate BPS policy to other towns |
| New York/North Jersey | [NYC Find a School](https://schoolsearch.schools.nyc/) and [NYC enrollment help](https://www.schools.nyc.gov/enrollment/enrollment-help) | Grade-specific zoning/application process; NJ and Westchester need separate district sources |
| Washington DC area | [Fairfax County schools/locator](https://www.fcps.edu/schools-centers) and [boundary changes](https://www.fcps.edu/facilities-planning-future/school-boundary-adjustments) | Source academic year and proposed versus adopted changes; DC, MD, Arlington and city systems separately |
| Atlanta | [Atlanta Public Schools school zones](https://www.atlantapublicschools.us/about/school-zones) | City school system versus county school districts; address and grade-year joins |
| Chicago | [CPS School Locator](https://schoolinfo.cps.edu/schoollocator/) | Attendance boundaries versus application programs; independent suburban districts separately |
| Austin | [Austin ISD attendance areas](https://www.austinisd.org/planning-asset-management/attendance-area-boundaries) | AISD boundaries versus city/county boundaries; other ISDs and future boundary revisions separately |
| Dallas | [Dallas ISD SchoolSite Locator](https://www.dallasisd.org/departments/demographic-studies/find-your-school/schoolsite-locator-interactive-map) | Locator calls for verification; district street-directory authority and other ISDs separately |
| Seattle | [Seattle Public Schools Find Your School](https://www.seattleschools.org/enroll/find-your-school/) | Attendance options, assignment and service context; surrounding districts separately |
| Los Angeles | [LAUSD Resident School Identifier](https://rsi.lausd.net/ResidentSchoolIdentifier/) and [source support](https://facilities.lausd.org/apps/pages/finder-support) | Resident-assigned versus application-eligible schools; other county districts separately |
| San Francisco | [SFUSD School Finder](https://www.sfusd.edu/sm/schools/enroll/discover/school-finder) and [attendance-area policy](https://www.sfusd.edu/student-assignment-policy/tiebreakers/attendance-area) | Attendance-area relevance is not a placement guarantee; every other Bay Area district separately |

A public web form is not permission for automated bulk access. A district-only manual verification path can support a pending candidate while an API/data agreement is investigated. Do not transmit household/dependent identity to these sources as part of this documentation work.

## 4. Source readiness scorecard

Maintain one record per region × tenure × capability × sub-geography, with an accountable owner and an evidence link. An empty cell is `unknown`, not pass. Proposed states: `research_only`, `synthetic_ready`, `source_validated`, `pilot_approved`, `paused`, `retired`. State advancement requires retained evidence; no free-form boolean enables a region.

| Capability | Evidence needed before pilot | Initial status for all ten |
|---|---|---|
| Listings | Sale and rental rights, unit/offer identity, display/cache/export terms, status/price refresh, provider coverage denominators | Not assessed |
| Geography | Versioned county/city polygons, neighborhood limitations, street segments, geocode precision and boundary tests | Not assessed |
| Cost | Fee and tax source hierarchy, ownership/rental assumptions, quote expiry, unsupported rule list | Not assessed |
| Education | District inventory, address/year/grade coverage, choice/program rules, conflicts, source permissions | Leads identified; not validated |
| Routing | Modes, time windows, borders, schedule validity, accessibility limitations, quote/cost caps | Not assessed |
| Employment | Historical coverage/vintage, industry mapping, employer sites, current posting license/deduplication if offered | National source leads identified; local coverage unvalidated |
| Environment/services | Hazard vintage/scale, amenities/childcare evidence, uncertainty and missingness policy | Not assessed |
| Household data | Live-data authorization, privacy permissions, retention, isolation, safe exports and deletion | Not implemented |
| Operations | Named regional/domain owner, incident process, source revocation switch, budget and monitoring | Not assigned |

Do not collapse this scorecard into one percentage that can compensate for absent rights, missing critical school access, or an unsafe data path. Required source/behavior gates are independent.

## 5. Proposed validation sampling and activation order

For each region, after permitted source access exists, independently review at least 20 purchase and 20 rental offers across at least three distinct subareas and multiple price/property categories. This is a minimum diagnostic sample, not proof of complete inventory or statistical representativeness. Inspect property/unit identity, price/status age, fees, coordinates, duplicate handling, and allowed rendering. Keep identifiable source samples outside the committed repo under the source contract.

Review at least 20 address/grade/year school-access cases per region, including boundaries, choice/program routes, ambiguous addresses, and future-year queries; all critical access claims must match the authoritative evidence or remain unknown. Validate at least 20 route queries across enabled modes/time windows against source responses. Audit at least 10 town/neighborhood and 10 street-segment outputs per region for sampling disclosure, sparse-data behavior, and successful address-level revalidation. Where current jobs are offered, inspect at least 20 postings for deduplication, worksite, expiry and advertised role data; historical-only mode must never label aggregates as openings.

DC-first priority is confirmed; subsequent waves are proposals, subject to source readiness and available owners:

| Wave | Regions | Reason for sequencing hypothesis |
|---|---|---|
| A | Washington DC area, including the reviewed VA/MD footprint | User-confirmed first focus; validate one complete area-to-home workflow and cross-jurisdiction evidence |
| B | Boston, Chicago, Austin | Proposed subsequent markets after DC learning and source readiness |
| C | New York/North Jersey, Atlanta, Dallas | Proposed expansion using validated contracts; order remains open |
| D | Seattle, Los Angeles, San Francisco | Proposed subsequent coverage; order remains open |

All ten remain registered in the specification with explicit coverage states. Detailed source research, synthetic regional fixtures and implementation focus first on DC; work on the other nine is not a prerequisite. Waves govern activation, not deletion of the user's confirmed product scope. Later waves may change through an explicit product decision; a failed source audit must not be hidden by launching a smaller unannounced footprint.

## 6. Region-level stop and fallback rules

- Source rights lapse: stop ingestion/display/derivative use as required, disable the affected capability, and process deletion/revocation obligations. Previously saved briefs remain accessible only to the extent permitted and with their expiry status.
- Critical identity, school assignment, or cost integrity defect: pause affected recommendations and alerts; retain metadata-only incident evidence and revalidate before resuming.
- Feed failure or stale status: mark dependent property results pending and stop “new suitable home” alerts; permitted manual entry and unaffected discovery continue with their limitations.
- Inadequate street/cost evidence: show broader-area exploration or access-only provisional segments; do not manufacture a precise street ranking.
- Absent current job feed: show only permitted historical employment and known employer/destination context with dates; no active-opening counts.
- Out-of-region address: explain the exact coverage boundary and retain notes if allowed; do not silently substitute a nearby covered location.

Every pause has an owner, reason, scope, timestamp, remediation, and reactivation evidence. Users receive an understandable impact explanation; operations retains the technical record.
