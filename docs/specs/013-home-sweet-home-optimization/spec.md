# 013 Home Sweet Home Optimization

**Status:** Comprehensive specification draft for collaborative review; not implemented or approved for pilot\
**Date:** September 27, 2026\
**Working product name:** Home Sweet Home\
**Branch:** `HomeSweetHomeOptimization`\
**Master feature:** FEAT-018\
**Portfolio phase:** 5, housing/location extension; research can precede admission, implementation remains gated by Spec 010\
**Related specs:** [002](../002-household-state-and-data-model.md), [003](../003-ai-orchestration-and-audit.md), [004](../004-capital-allocation-optimizer.md), [005](../005-product-labs-and-workflows.md), [006](../006-jurisdiction-intelligence.md), [007](../007-validation-and-market-research.md), [009](../009-monitoring-alerts-and-outcomes.md), [010](../010-extension-portfolio.md), [012](../012-governed-decision-brief-workflow.md)\
**Companions:** [DC-area first pilot](dc-area-pilot.md), [Ten pilot regions](pilot-regions.md), [Engineering, validation, and delivery handoff](engineering-handoff.md)

## 1. Product decision and intended outcome

> Given where we need to be, what we can spend, how we want to live, and what remains uncertain, which homes and areas deserve our attention—and what trade-offs would we make by buying, renting, staying, or waiting?

Home Sweet Home is a Kinvoryx housing decision workspace. It recommends towns, neighborhoods, and street segments to explore, then helps a household compare actual purchase and rental candidates using total costs, education, daily access, and additional job opportunities. It also works independently with a user-entered budget and preferences. Connecting household finances adds cash-flow, liquidity, and goal effects through an explicit snapshot; it is not required to begin searching.

The product optimizes a household-defined decision over the candidates and evidence available. It does not claim to find the objectively best neighborhood, certify affordability, guarantee school placement, or search every listing. Its primary output is a small, explainable set of feasible or explicitly provisional alternatives with a Housing Decision Brief, not a universal score or a transaction.

The differentiating hypothesis is that combining area discovery, total cost, daily travel, education, additional job access, household disagreement, and uncertainty reduces wasted search and reveals better trade-offs than filters plus a spreadsheet. This is a hypothesis to validate against the user's current process, not a demonstrated advantage.

## 2. Decision register and review status

| ID | Decision | Status / provenance |
|---|---|---|
| DEC-HOME-001 | Support both buying and renting in the first release, with distinct cost and eligibility inputs. | Confirmed by user, September 26, 2026 |
| DEC-HOME-002 | Pilot Boston, New York/North Jersey, Washington DC area, Atlanta, Chicago, Austin, Dallas, Seattle, Los Angeles, and San Francisco. | Region membership confirmed by user, September 26, 2026; precise footprints and activation waves proposed in companion |
| DEC-HOME-003 | Integrate with Kinvoryx household finances and retain standalone search. | Confirmed by user, September 26, 2026 |
| DEC-HOME-004 | Interpret “extension” as a product module/workspace, with no browser extension required. | Follows confirmed integrated-workspace direction |
| DEC-HOME-005 | Include optional detailed education: address-specific assignment, programs, enrollment uncertainty, travel time, childcare, and school metrics with source context. | Confirmed by user, September 26, 2026 |
| DEC-HOME-006 | Start with manual/synthetic candidates; add licensed discovery after source validation. | Original sequence proposal superseded by DEC-HOME-012 for the first data-test milestone; deterministic synthetic fixtures remain required |
| DEC-HOME-007 | Preserve hard constraints, individual preferences, and uncertainty before any optional ordering. | Proposed design, consistent with Specs 002 and 010 |
| DEC-HOME-008 | Initial consumer is a household with a move or lease decision in the next 3–12 months; payer hypothesis is the household. | Discovery hypothesis; employer/professional distribution later |
| DEC-HOME-009 | Include proximity and travel access to additional job opportunities, beyond the current workplace. | Confirmed by user, September 26, 2026 |
| DEC-HOME-010 | Recommend towns, neighborhoods, and streets/segments based on preferences to progressively narrow the search before evaluating homes. | Confirmed by user, September 26, 2026 |
| DEC-HOME-011 | Focus first on Washington DC and surrounding Virginia and Maryland (HOME-REG-003), retaining the other nine regions for later expansion. | Confirmed by user, September 27, 2026; core/outer-ring footprint and activation evidence remain proposals |
| DEC-HOME-012 | Make a limited live-data test the next research milestone for DC/VA/MD. | User-confirmed direction, September 27, 2026; source access, credentials and routing remain unresolved; spending is constrained by DEC-HOME-013; does not authorize purchases, private-household collection or public launch |
| DEC-HOME-013 | Use a zero-dollar source budget for the first live-data test, prioritizing public APIs and free developer quotas with hard caps. | Confirmed by user, September 27, 2026; free-tier availability and terms require source-specific verification and do not establish complete listing coverage |
| DEC-HOME-014 | Exclude RentCast from the required $0 setup unless a no-payment, no-overage path is verified. | User correction, September 27, 2026; RentCast official docs describe free monthly requests with overage fees, so it is not treated as required zero-dollar infrastructure |

Confirmed scope choices do not imply that formulas, implementation, commercial terms, pilot launch, or source contracts have been approved. Proposed architecture and backlog below are review aids; they become an executable plan after the spec and extension admission gate are approved.

## 3. Users, jobs, and baseline

| User / trigger | Job | Critical distinctions |
|---|---|---|
| Renter approaching renewal or moving for work | Compare staying, renewing, and available rentals | Lease dates, deposits, recurring fees, concessions, renewal uncertainty, transit |
| Buyer considering a primary residence | Compare homes without exhausting cash or disrupting other goals | Cash to close, all-in carrying cost, reserves, condition, financing assumptions |
| Household unsure whether to rent or buy | Compare tenure choices over the same horizon | Entry/exit costs, time in home, liquidity, uncertain resale and renewal |
| Multi-adult household with several destinations | Find workable locations and disclose uneven burdens | Separate commutes, schedules, vetoes, preference weights, caregiving trips |
| Household with education or accessibility needs | Find relevant access and verify feasibility | Address/year-specific school access, program admission, step-free features, transport |
| Relocating household unfamiliar with an area | Narrow areas before searching individual homes | Geographic coverage, local costs, travel network, verification tasks |

Baseline comparisons are: the household's current shortlist, price-only sorting of the same eligible candidates, and a simple hard-filter search. Include staying/renewing when permitted and known; an unavailable renewal is not a feasible baseline. “Wait” requires an explicit temporary-housing or continuing-housing plan and its costs. If current housing is unknown, label the baseline unavailable rather than inventing it.

Measure whether participants can explain trade-offs, identify missing evidence, and assemble a feasible shortlist faster. A move, purchase, higher-priced home, or referral conversion is not intrinsically a successful outcome.

## 4. Scope and non-goals

### First release target after admission

- Buying, renting, and comparing tenure for an owner-occupied primary home; USD and U.S. conventions.
- Register the ten-region roadmap from the start; focus initial regional research and pilot development on HOME-REG-003 (DC and surrounding VA/MD). Both tenure modes remain in scope for each region as it is admitted; the other nine remain in research until their own gates pass.
- Ordinary long-term rentals and purchases of single-family homes, townhomes, and condos whose costs and restrictions can be represented. User-entered candidates are supported without a live listing feed.
- Standalone mode, optional finance connection, multi-member preferences, town/neighborhood/street recommendations, candidate comparison, detailed education access, additional-job access, route estimates, scenario testing, shortlist, and review/export.
- Cash purchases and fixed-rate, fully amortizing mortgages; input-driven mortgage-insurance costs. Quotes and qualification come from lenders, not this module.
- Begin with permitted live-source feasibility checks alongside synthetic correctness fixtures. The first data-test milestone can use real public/licensed evidence with fictional household profiles; private household persistence, collaboration and alerts retain their later pilot controls. Clearly distinguish live inputs from synthetic fixtures.

### Deferred or unsupported

- Investment-property optimization, landlord/tenant scoring, tenant screening, mortgage underwriting, insurance binding, offers, applications, negotiation, bidding, contracts, payments, or automated outreach.
- International jurisdictions, co-ops, land leases, manufactured-home financing, shared ownership, rent-to-own, short-term lodging, subsidized-housing eligibility, complex construction/renovation, adjustable-rate/balloon/interest-only loans, and relocation tax optimization. Retain an unsupported candidate for notes if useful, but do not force it into a supported model.
- Automatic appreciation forecasts, school-placement probabilities, predictive crime models, protected-class neighborhood matching, universal “best school”/“safe area” scores, or inferred household identity.
- Browser scraping, paywall bypasses, unlicensed listing/image reuse, and silent retrieval from a pasted URL. A URL can be retained as a reference without fetching it.
- Full household scheduling, autonomous preference learning, marketplace referrals, commission-funded ordering, and automated decisions on behalf of another household member.

Deferred features require their own requirements and evidence. The first release's coverage must say exactly which property, cost, source, and decision types are supported.

## 5. End-to-end experience

1. **Start a search.** Select buy, rent, or compare both; one or more covered regions; move window; expected stay; and a monthly spending/cash envelope. Standalone users need no income, account, or employer connection. Do not infer a market from their device location.
2. **Set places and priorities.** Add named destinations and travel windows, space/property needs, accessibility and pet requirements, education interests, and must-haves versus preferences. Each adult can use a separate profile; education can be skipped entirely.
3. **Review the search contract.** Show hard constraints, optional objectives, weights if any, missing inputs, and scope. Explain what cannot yet be evaluated. Give examples of the consequences of tightening a constraint.
4. **Narrow places before listings.** Recommend towns/municipalities, neighborhoods, then street segments that fit declared priorities; show reasons, countervailing costs, job/education access, uncertainty, and representative verified evidence. Let users pin multiple areas, reject or compare them, and open homes inside them. Provide equivalent list navigation. Area statistics are discovery context, never substituted for a property's costs, school assignment, hazards, or availability. Pin the search area independently of map zoom.
5. **Add and discover homes.** Manual entry, permitted structured import, and approved feeds converge on one contract. Display source, exact unit where known, availability, asking terms, freshness, and de-duplication conflicts. A building-level “starting at” price is not a unit offer.
6. **Inspect feasibility.** Separate feasible, pending verification, infeasible, and unsupported candidates. Show the particular constraints and evidence responsible. Let users examine excluded candidates and explicitly change constraints; never relax a must-have automatically.
7. **Compare a shortlist.** Default to trade-off cards and side-by-side metrics. Offer price/cost/commute ordering and optional user-defined preference ordering with a visible basis. Compare 2–6 choices plus a valid baseline without hiding other nondominated candidates.
8. **Stress the decision.** Change horizon, rates before purchase, rent renewal, travel schedule, education access, repairs, insurance, income, or timing. Keep the scenario identical across compared candidates where semantically applicable.
9. **Verify the important unknowns.** Produce a prioritized checklist: obtain fee schedule, confirm address/year-specific school access, check peak-hour route, inspect step-free access, seek an insurance quote, or inspect property condition. The user performs or authorizes external actions.
10. **Retain a decision brief.** Save inputs, sources, alternatives, disagreements, assumptions, sensitivities, open questions, and user rationale. Sharing exposes only an intentionally chosen projection. Later changes create a new version and a visible difference report.

The top of the workspace answers: “What fits?”, “What would it cost?”, “What are we giving up?”, and “What needs checking?” Technical run IDs and hashes belong in the reviewer view. Loading, no-results, partial coverage, unavailable sources, ambiguous address, and expired listing states have explicit designs.

## 6. Decision dimensions and input policy

Every active dimension declares its unit, direction, source, freshness, permitted use, household owner, and whether it is a hard constraint, soft preference, or context only. Defaults are marked assumptions. A blank value is not zero, false, or “not applicable.”

| Dimension | Examples / representation | Handling |
|---|---|---|
| Purchase/rent terms | Asking price or contract rent, unit, date, tenure | Separate offer terms from area statistics and estimates |
| All-in monthly cash demand | Housing costs, essential transport, childcare needed for the location | Housing and location-induced expenses remain separate subtotals |
| Upfront liquidity | Deposit/down payment, fees, moving, overlap, emergency reserve | Calendar cash-flow check; refundable amounts remain assets |
| Multi-year cost | Discounted cash flows, exit proceeds, renewal/sale scenarios | Same horizon and conventions for buy/rent/stay |
| Location | User-selected geometry, destinations, max travel time | No demographic desirability inference or ZIP-level eligibility |
| Property fit | Beds, baths, interior area, layout, workspace, storage, outdoor space | Units explicit; listing assertions versus user/inspection verification |
| Access needs | Step-free path, elevator, door clearance, bathroom or parking needs | Describe functional requirements; do not require diagnosis |
| Daily travel | Per-person routes, mode, times, onsite days, transfers, cost | Round trips, reliability and schedule assumptions visible |
| Additional job access | User-selected occupations/industries, employers, current openings and employment hubs within travel budgets | Existing employment, active postings, role fit, and future opportunity remain separate |
| Education | Grade band/year, assignment, programs, enrollment, travel, tuition | Optional; program access and school performance distinct |
| Childcare | Hours, travel, price, licensed/provider facts, waitlist status | No available-slot claim without timely evidence |
| Daily services | Grocery, healthcare access, parks, transit, libraries, broadband | User selects relevant destinations/services; no medical advice |
| Property/environment exposure | Flood, heat, wildfire/smoke, noise, condition, outage exposure | Separate hazards and source scales; unknown is not low risk |
| Insurance/maintenance | Quote, deductible, exclusions, repairs, assessments | No guarantee of insurability; ranges and stress cases |
| Flexibility | Lease length, break cost, renewal uncertainty, resale costs, commute changes | Avoid assuming buying always builds more usable wealth |
| Restrictions and timing | Pets, move-in, parking, occupancy terms, HOA restrictions | Verify applicability; no legal interpretation from free text |
| Household goals | Reserve floor, debt obligations, savings commitments | Explicit finance snapshot and expense replacement map |
| Personal impressions | Visit notes, light, noise, comfort, preferences | User-authored subjective evidence, never inferred from demographics |

“Area” means explicit geography and access to the household's activities. Do not compress it into a universal neighborhood-quality number. Neighborhood names are labels, not reliable administrative or school boundaries.

## 7. Functional requirements

All requirements below are Must for the applicable release slice. A deferred slice is identified in the engineering companion; it is not silently omitted from the eventual pilot release.

| ID | Requirement | Owner role |
|---|---|---|
| REQ-HOME-001 | Support buy, rent, and mixed-tenure search with dates, horizon, baseline, supported-type checks, and explicit outcomes. | Product |
| REQ-HOME-002 | Offer standalone budget-envelope search and consented household-finance snapshots with provenance and an explicit replacement of existing housing expenses. | Product / Finance |
| REQ-HOME-003 | Separate hard constraints, aspirations, and soft preferences; preserve per-member vetoes, weights, and disagreements. | Product / Optimization |
| REQ-HOME-004 | Resolve search geometry and candidate/unit identity; expose address ambiguity, geography coverage, and duplicate/source conflicts. | Data |
| REQ-HOME-005 | Support manual candidates and licensed adapters through one contract; retain listing state, effective terms, attribution, and allowed uses. | Data |
| REQ-HOME-006 | Calculate itemized rent and ownership cash demand, upfront liquidity, and a dated cash-flow ledger without duplicate costs. | Finance |
| REQ-HOME-007 | Compare buy/rent/stay over common horizons with explicit terminal assets/debt, discounting, scenarios, and no unsupported tax or return assumptions. | Finance / Optimization |
| REQ-HOME-008 | Calculate per-person travel and access using destination, mode, day/time, frequency, and route evidence; separate measured, modeled, and user estimates. | Geospatial |
| REQ-HOME-009 | Model optional education access by address, grade, academic year, program, enrollment route, cost, and verification status without placement guarantees. | Education / Data |
| REQ-HOME-010 | Represent property fit, functional accessibility, amenities, childcare, restrictions, environment, and condition with source-specific uncertainty. | Product / Data |
| REQ-HOME-011 | Classify each candidate as feasible, pending verification, infeasible, or unsupported; retain reasons and propose explicit relaxation scenarios for empty results. | Optimization |
| REQ-HOME-012 | Produce transparent baselines, a nondominated set, and optional preference-based ordering with stable transformations, contributions, ties, and comparison scope. | Optimization |
| REQ-HOME-013 | Evaluate common stresses, preference sensitivity, uncertainty bounds, and result reversals; never invent probabilities or hide missing evidence in a score. | Model Risk |
| REQ-HOME-014 | Preserve household-member burden distributions and independently visible preferences; record consent to shared constraints or aggregated weights. | Product / Privacy |
| REQ-HOME-015 | Provide area/list/map discovery, candidate detail, a 2–6 item comparison, shortlist, and explicit failure/coverage states with an equivalent non-map path. | Design |
| REQ-HOME-016 | Produce household and reviewer briefs from one retained result with evidence, costs, rationale, excluded choices, source coverage, and verification tasks. | Reporting |
| REQ-HOME-017 | Version saved searches and shortlist changes; offer opt-in change alerts with freshness, materiality, deduplication, pause, and re-analysis rather than silent reranking. | Platform |
| REQ-HOME-018 | Register all ten pilot regions with separate geography, tenure, source, education, jurisdiction, owner, and admission status. | Product / Data Ops |
| REQ-HOME-019 | Enforce field-level source rights, provenance, freshness, as-of availability, join cardinality, and bounded missingness semantics. | Data / Security |
| REQ-HOME-020 | Enforce purpose-limited collection, private destinations/preferences, revocable collaboration, safe exports, and tested retention/deletion before real-household use. | Privacy / Security |
| REQ-HOME-021 | Exclude discriminatory targeting, ungrounded safety/school judgments, paid ranking influence, and autonomous external action; distinguish product policy from jurisdictional legal conclusions. | Compliance / Product |
| REQ-HOME-022 | Keep eligibility, calculations, constraints, and ordering deterministic; AI can draft structured inputs and explain evidence only after user confirmation and validation. | Platform / Model Risk |
| REQ-HOME-023 | Bind each result to immutable input/source/policy versions, validation, review, and coverage; reuse the Spec 012 evidence pattern without pretending cash-inflow records validate housing. | Platform |
| REQ-HOME-024 | Evaluate incremental user value, per-region coverage, operating cost, harm signals, and explicit rollout/stop criteria before expanding. | Research / Operations |
| REQ-HOME-025 | Evaluate access to additional employment using explicit role/industry preferences, travel budgets, deduplicated current openings when licensed, and separately labeled historical employment context. | Labor Data / Product |
| REQ-HOME-026 | Recommend and explain towns, neighborhoods, and street segments before property selection; support hierarchical drill-down, multiple pinned areas, sampling/coverage disclosure, and address-level revalidation. | Geospatial / Optimization |

## 8. Cost and affordability contract

### 8.1 Cash demand and financing

Model amounts as decimal USD with documented rounding; dates and annual/monthly rates have explicit conventions. Preserve unrounded calculation precision and round displayed currency to cents. Cost lines carry type, timing, payer, whether recurring/refundable/prepaid/financed, source, and uncertainty bounds.

Rental monthly housing demand includes contract rent, recurring property/amenity/pet/parking fees, renter insurance, and tenant-paid utilities. Show one-time application/move-in/broker fees separately where applicable and sourced. Refundable deposits reduce available cash but are not expenses unless a scenario explicitly models forfeiture. Prorated first/last month and free-rent concessions are assigned to actual months; effective rent cannot replace the maximum contractual monthly cash obligation. Model renewal as an assumption after lease expiry, never a guarantee.

Ownership monthly housing demand includes mortgage principal and interest, property tax, insurance, mortgage insurance when applicable, HOA/condo dues, utilities, and a maintenance allowance. Special assessments, planned repairs, moving, prepaid items, inspections, transaction fees, and dual-housing overlap enter at their actual dates. Principal is cash outflow and debt reduction, not an irrecoverable expense. A maintenance savings transfer is restricted liquidity; realized maintenance is expense. Do not count both as expense. Escrow payments and the underlying tax/insurance bills must reconcile without duplication.

For a supported fixed-rate loan with principal `L`, monthly contractual interest rate `r`, and `n` payments:

```text
payment = L * r / (1 - (1 + r)^(-n))   if r > 0
payment = L / n                        if r = 0
interest_t = balance_(t-1) * r
principal_t = payment_t - interest_t
balance_t = balance_(t-1) - principal_t
```

Adjust the final payment to close the balance under the chosen rounding convention. Reject non-finite values, negative principal, invalid terms, or unsupported loan structures; a cash purchase has zero loan and no mortgage payment. Contractual interest rate is distinct from APR and from projected investment return. No automatic refinancing, mortgage-insurance cancellation, homestead exemption, or tax deduction is assumed.

The CFPB describes housing costs beyond principal and interest and distinguishes closing costs from cash needed at closing; these support the cost categories, not numerical defaults. Local estimates and actual quotes remain required. [Housing budget](https://www.consumerfinance.gov/owning-a-home/prepare/figure-out-how-much-you-want-to-spend/), [Closing disclosure](https://www.consumerfinance.gov/owning-a-home/closing-disclosure/)

### 8.2 Liquidity and household connection

Report separately: total initial funding, incremental cash still due, maximum monthly demand, essential location-induced expenses, residual budget, liquid reserve after entry, and minimum liquid reserve over the modeled period. Earnest money already paid is a credit against closing, not a second expense. Financed fees increase debt once; prepaid housing is not charged again for the covered period.

In standalone mode, feasibility is relative to the user's spending and available-cash envelopes. If available cash is omitted, liquidity is unknown; if essential expenses are omitted, do not call the home affordable or report reserve months. A lender's estimated qualification is context, never a substitute for household feasibility.

In connected mode, map current housing, utilities, debt payments, transport, and childcare lines explicitly. Replace only costs that end; retain obligations that continue and any dated overlap. Mortgage principal must not appear both as a housing payment and an unchanged debt minimum. Housing equity, restricted funds, and assumed future sale proceeds are not immediately available cash. Changing a housing scenario never mutates the source household state. Applying a scenario creates a separately confirmed proposed state.

### 8.3 Common-horizon comparison

Use a shared start date, horizon `H` in months, inflation convention, financing assumptions, and scenario set. The default presentation offers editable 1-, 3-, 5-, and 10-year comparisons when inputs permit; these are scenario horizons, not predictions of how long to stay.

Define a **housing cash-cost NPV** (lower is better) from the household's external cash ledger:

```text
NPV = C0 + sum(Ct / (1 + d)^t, t=1..H) - AH / (1 + d)^H
d = (1 + annual_nominal_discount_rate)^(1/12) - 1
```

`C0` is entry cash paid from household funds; `Ct` is net housing/location cash outflow at month `t`; `AH` is terminal recoverable housing-related value not already credited in `Ct`. For an exit-sale scenario, `AH` includes sale proceeds net of selling costs and outstanding debt, and any recoverable deposits/escrow. A negative terminal net value remains negative. For rentals, model only explicitly recoverable deposits/prepayments and no home equity. If entry cash includes an asset transfer such as a deposit, the terminal recovery accounts for it once. Exclude a separate opportunity-cost charge when using discounting; do not add a competing-investment return on the same cash difference without a distinct reconciled wealth model.

Internal transfers into a household-owned maintenance reserve are excluded from this external cash-cost ledger; actual repair payments enter once when paid. Budget and available-liquidity views may still reserve that cash. Enforce annual discount rates greater than -100%, consistent nominal/real cash-flow conventions, positive horizons, and declared calculation precision.

Report this alongside cash demand and liquidity; NPV is not net worth, a forecast, or a complete welfare measure. An optional mark-to-market “still own at horizon” view is labeled distinctly from a liquidation comparison and is not spendable cash. Higher sale proceeds, appreciation, tax benefits, investment returns, renewal costs, and deposit recovery must be explicit scenarios or verified inputs. No cross-state after-tax comparison is generated from the current federal-only prototype rules. No break-even date is reported if none exists within the modeled horizon; multiple crossings are disclosed.

## 9. Optimization, uncertainty, and household agreement

### 9.1 Feasibility before preferences

For each candidate evaluate every hard constraint using `pass`, `fail`, `unknown`, or `unsupported`. For a supported candidate: any known failure makes it infeasible; otherwise any unknown makes it pending; all passes make it feasible. An unsupported decision model remains unsupported even if some individual constraints can be evaluated. Retain every known failure in all states. Listing unavailability is a feasibility failure for the requested date.

For a bounded interval and a maximum constraint: the entire interval below the limit passes, the entire interval above the limit fails, and an interval crossing the limit is unknown. Minimum constraints use the reverse rule. An unknown hard school assignment, accessibility feature, or all-in cost is never a pass. Users can revise constraints or request scenarios but cannot transform missing source evidence into verified fact by clicking “accept.”

When no candidate is feasible, show binding constraints and small explicit changes such as a larger search geometry or five additional commute minutes. Recompute those as separate scenarios with their burdens. Do not describe a conflict set as mathematically minimal unless the algorithm proves it.

### 9.2 Trade-off frontier and optional ordering

Compute the nondominated set over the feasible candidates and a declared set of comparable objectives, usually cost, travel burden, property fit, education access when enabled, and flexibility. “Nondominated” means no other evaluated feasible candidate is at least as good on every active objective and strictly better on one, under the declared tolerance. It means best trade-offs within this candidate universe and snapshot, not the whole market.

Unknown objective values yield intervals or an incomparable/provisional result; do not drop those candidates as dominated from missing data. Use conservative interval dominance only when one candidate's worst bound is no worse than the other's best bound on every active objective, with one strict improvement. Report point-estimate and interval comparisons distinctly. Confidence/coverage is a separate axis, not an invented utility bonus.

Optional member-specific utility uses confirmed, fixed anchor functions:

```text
U_m(candidate) = sum(w_mj * u_mj(x_j))
w_mj >= 0; sum(w_mj) = 1; u_mj is bounded in [0, 1]
```

Users choose meaningful anchors such as acceptable/ideal commute or budget. Do not fit min/max scales to the currently visible candidates: adding an irrelevant listing must not change an existing candidate's utility. Set group weight budgets so correlated submetrics (price versus total cost; drive time versus proximity; several school metrics) do not silently multiply one concern. Show the contribution of each group and the input lineage.

If a positively weighted value is missing, propagate its permitted utility interval; do not renormalize remaining weights per property, fill it with zero, or award an average score. Only compare point scores when every weighted input is present with a disclosed assumption status. Overlapping utility intervals and values within a proposed 0.01 utility tolerance are “no clear separation,” not a definitive winner. Deterministic candidate-ID order can stabilize rendering, but must not imply superiority. All-zero weights are invalid for weighted sorting; trade-off browsing remains available.

Keep each member's result visible. Household ordering is available only after members explicitly agree on aggregation weights; it never overrides vetoes. Report per-person weekly travel and who bears extra cost/time. Minimax regret or other negotiated aggregation is later research, not an implied default.

### 9.3 Scenarios and robustness

The first deterministic scenario library varies mortgage quotes before purchase, rent at renewal, insurance/tax/HOA costs, maintenance shocks, deposit recovery, move timing/overlap, holding period, resale value/sale costs, work attendance, route delay, loss of a desired school/program option, and household income when connected. Use explicit magnitudes in a versioned policy; no universal economic assumptions are established by this spec.

Separate pre-purchase interest-rate changes from an already fixed mortgage. Separate an individual's school access uncertainty from a population school metric. Preserve scenario correlations when changing several variables together. Only combine stresses when the scenario explicitly defines the combination.

Show which constraints fail, which comparisons reverse, and which inputs matter most. Weight sensitivity varies group weights by a proposed plus/minus 20% then renormalizes at profile level, preserving zero weights and hard constraints; enumerate one-at-a-time cases and report tested coverage, not an exhaustive robustness guarantee. If there are no plausible numerical bounds, report unavailable sensitivity rather than a fabricated interval. Do not use probabilistic language without a validated probability model.

Prioritize verification tasks by whether the unknown can change feasibility, reverse the shortlist, or materially affect cash/time. This is a deterministic priority rule, not a claimed monetary value of information.

## 10. Education, geography, and travel contract

### 10.1 Education and daily access

Education is optional and must serve the user's stated needs. A preference for a program, travel time, language offering, or functional support is not a license to infer protected traits. Capture grade bands and academic years, not children's names, exact dates of birth, diagnoses, or school records.

Represent five different concepts separately: nearby school, address-associated attendance boundary, eligibility route, actual enrollment/seat availability, and program fit. Store the relevant academic year, source date, grades served, school/district IDs, and boundary/version. Address lookup may identify an associated school while leaving enrollment or program availability unknown. Choice, lottery, magnet, charter, private, transfer, capacity, and future rezoning are not collapsed into a binary “assigned” field.

District/address-specific authoritative information takes precedence for school access; school directories support discovery, and third-party ratings are contextual source products. A ZIP code, nearest school, real-estate listing school name, district polygon, or national historical boundary layer cannot prove current school assignment. NCES describes SABS as an experimental attendance-boundary survey; it must not be treated as a current universal enrollment service. [NCES SABS](https://nces.ed.gov/programs/edge/SABS)

School metrics, when enabled, show metric definition, year, grade/population, missingness/suppression, and source. Avoid mixing incomparable state scales. No default scalar “school quality” utility exists. A user may explicitly select supported metrics with understood limitations; program availability and assignment remain separate constraints. Test scores are not a prediction of an individual child's outcomes or evidence of school value added. Missing or suppressed metrics are not low quality. Childcare seats, tuition, hours, and waitlists have separate verification.

For each destination record private label, location precision, day/time window, timezone, travel mode, trips per week, and accessibility needs. Return door-to-door components where available, transfers/walking/parking, toll/fare assumptions, effective schedule, and retrieval time. Calculate each member's round-trip weekly burden; simultaneous shared trips are not charged twice in household totals. Multi-stop school/care/work routes need a routed itinerary, not independent distances added as if compatible.

Historical reliability or percentile travel times require appropriate observations. A single routing estimate is not a p90. A scheduled transit route is not proof of service reliability or accessible operation. If only straight-line distance exists, label it as distance and do not satisfy a travel-time constraint with it. Cross-border routes may leave a covered region without making homes beyond that region supported candidates.

### 10.2 Access to additional jobs

Users may define target occupations, industries, skills, preferred employers, work arrangement, and an acceptable travel-time budget for each adult. Employer and role names are optional; no resume, employment account, or sensitive demographic profile is required. This adds a future-opportunity dimension alongside current commutes, with independent user-controlled weight.

Keep three evidence types distinct:

1. **Current opportunities:** authorized active job postings, with employer, role, worksite precision, onsite/hybrid/remote terms, dates, salary range only if sourced, source link, and status. Deduplicate syndicated postings and reposts; disclose unresolved duplicates. Count postings, not assumed vacancies. Remote-only opportunities are a separate list and do not boost the physical attractiveness of every town. A headquarters location is not a worksite.
2. **Employer and employment access:** verified employer sites and historical employment concentrations by industry within travel budgets. Census LODES describes geographic employment and commuting relationships; these counts are not current openings or a prediction of a user's job prospects. Exclude worker-demographic variables from housing desirability. [Census LODES documentation](https://lehd.ces.census.gov/data/lehd-code-samples/sections/lodes.html)
3. **Broader labor-market context:** regional occupation employment/wage estimates with vintage and geography. Do not assign metro wages or counts to a particular street or imply an expected offer. [BLS metropolitan occupation estimates](https://www.bls.gov/OES/current/oessrcma.htm)

For current postings, compute the count matching explicit filters whose route-time upper bound is within the travel cap, plus a separate count of potentially reachable/unknown-worksite postings. Do not merge those counts. Unknown hybrid frequency or worksite makes travel-dependent fit provisional. For historical industry counts, describe the unit and vintage and report approximate accessibility when geographic cells straddle route-time boundaries. No hidden “hireability” score, hiring probability, inferred skill fit, job-offer guarantee, or job application workflow is included.

Show how many distinct employers and job categories are reachable in each evaluated scenario, where the source supports those identities; employment aggregates cannot manufacture employer identities. A broader accessible market can be a user preference for resilience, but its benefit is not automatically monetized. Keep each adult's opportunity set separate, so a location that helps one career while restricting another exposes that trade-off. Missing local job feeds produce a historical-context view with an explicit current-openings gap.

Current-posting status should be rechecked within 24 hours, removed upon known closure/expiry, and marked unknown when worksite or role is ambiguous. Historical employment and wage data use a declared release vintage and latest-release check; daily retrieval does not make those observations current. All job feeds need source rights and a validated taxonomy mapping before contributing to ordering.

### 10.3 Town, neighborhood, and street recommendations

The discovery hierarchy is region → town/municipality or comparable place → neighborhood → street segment/corridor → property/unit. These geographies can overlap; the model is a graph of containment/intersection relationships, not an assumption that every neighborhood has one official parent. Users can start at any level or search several regions. Streets use a geospatial segment ID and explicit endpoints, side where relevant, geometry, and source/version; a street name alone is not unique.

Generate area candidates from licensed/official geography and a declared eligible residential search universe. Evaluate costs using observed comparable listings or appropriately labeled historical context, access from representative residential origins, and education/employment/service evidence at its actual resolution. Each area card contains:

- Why it fits the stated preferences and which member benefits or bears a burden.
- Observed rent/purchase ranges, sample sizes, period, property mix, and separately the current eligible-listing count by tenure; no claim that a market-wide median fits the budget.
- Per-destination travel ranges and accessible job evidence by type, with origin sampling and coverage.
- Relevant education/program/childcare discovery options, address-level unknowns, and upcoming verification needs.
- Competing areas and what changes if budget, travel time, education priority, or property needs change.
- Geometry and any internal variations, missing evidence, source dates, and a clear “explore this area” action.

Use the same explicit objectives, weights, interval comparisons, and explanations as property-level search, but label results **search-area recommendations**, not verified feasible homes. Do not average away a subarea's hard constraint failures or use a town centroid to declare all homes reachable. Cost summaries must be stratified by tenure and material property requirements. Sample origins across residential subareas, record a reproducible sampling scheme, and disclose the proportion meeting each access constraint. Do not claim that a sampled proportion is the probability a suitable home will be found.

Proposed sparse-data policy: fewer than 10 distinct current comparable offers within a town/neighborhood and rolling 30-day observation window suppresses numerical area cost-fit ordering; show sample evidence and a coverage gap. Deduplicate repeated snapshots and distinguish active-today counts from the observation window. Street segments require at least 3 distinct current comparable offers or a separately validated local property-cost model to produce a cost-fit estimate. Without that evidence, recommend a segment only for supported access/preferences with cost marked unknown, or recommend a broader area. These thresholds are reviewable quality policies, not statistical representativeness guarantees.

If live inventory is empty but geographic/access evidence supports a match, mark the area “worth monitoring; no matching current listings.” Keep it separate from areas with verified available candidates. Do not expand boundaries, impute favorable prices, inherit school assignment, or label absent observations as zero demand. Sampled routes, school boundaries, hazards, noise, tax jurisdictions, and street sides can vary within a segment; every selected address is re-evaluated before property feasibility.

The default discovery view presents 3–7 materially distinct areas with explanations, discloses the full qualifying/nondominated count, and supports expanding the view. Diversity means different cost/access/property trade-offs, never demographic composition. An area with weak data is provisional, not automatically “worse.” Clicking a town or segment carries the search contract forward and visibly identifies any changed geography; it does not reset member preferences or silently remove a constraint.

Illustrative output contract (entirely fictional): “Explore Example Town's Library Road between First and Third Streets: sampled routes fit your work travel window and three observed rentals fit your space and monthly envelope. Education assignment remains address-specific; job counts refer to last year's employment, not open roles. Compared with Example Town B, this corridor reduces Member A's travel while adding $200/month in the observed rental sample.” This is a format example, not a recommendation of real towns or streets.

## 11. Sources, coverage, and evidence

Each `SourcePolicy` declares ownership, source URL/ID, license and retention rights, display/derivative-use rules, attribution, refresh SLA, effective dates, geographic/tenure coverage, collection method, review owner, and status. Dataset grain and join keys are explicit. Pasted listings and source text are untrusted data, not agent instructions.

| Data class | Preferred evidence | Limitation / fallback |
|---|---|---|
| Sale and rental candidates | Licensed MLS/provider/property-manager feed; documented user entry | Standards do not confer data rights; manual candidates remain unverified |
| Property/unit facts | Parcel/unit identifiers, permitted listing facts, inspection/user verification | Parcel, building, unit and offer are different entities |
| Taxes and fees | Local assessor/collector, quote, lease/HOA schedule supplied with permission | Historical bill is not necessarily next owner's assessed tax |
| Financing and insurance | User-supplied quote with dates/expiry; explicit scenario | No inferred approval or current rate from stale averages |
| Education | District lookup, enrollment policy, state education data, school/program source | Directory discovery does not guarantee access or admission |
| Routing and transit | Licensed routing service and current agency schedules | Provider rights, coverage, schedules, and cost require validation |
| Employment and jobs | Authorized postings/employer sites; Census LODES and BLS context with vintage | Existing jobs, distinct employers, active postings and offers are different measures |
| Towns/neighborhoods/streets | Official/licensed polygons, street network, residential origin samples | Boundaries overlap; sample access cannot establish every address's feasibility |
| Environmental exposure | Official hazard source and separately reviewed specialist data | Geographic resolution and modeled horizon remain visible |
| Amenities/childcare/broadband | Official/provider datasets and permitted geospatial sources | Presence does not establish capacity, price, accessibility, or service |

RESO supplies standards, not MLS listing data; actual provider access and permitted use must be secured independently. FEMA's Map Service Center provides official NFIP flood-hazard information and notes that maps change; a map result is neither a property inspection nor a complete hazard/insurance assessment. [RESO Web API](https://www.reso.org/reso-web-api/), [FEMA MSC](https://msc.fema.gov/portal/home)

The following zero-dollar or public-source candidates should be tracked for the first
DC-area benchmark. They are supporting evidence sources, not substitutes for
licensed listing coverage or address-specific verification.

| Source candidate | Useful component | Access model / first check |
|---|---|---|
| [Trellistate](https://trellistate.com/docs) | Active public listing probe | No-key public reads; measure coverage, freshness, attribution and source quality before using in comparisons |
| [Census API](https://www.census.gov/data/developers.html) / [ACS](https://www.census.gov/programs-surveys/acs) | Area housing, commute, tenure, income and household context | Free Census key; use as context only, and never as demographic desirability scoring |
| [Census LODES](https://lehd.ces.census.gov/data/#lodes) | Workplace density, origin-destination and employment-hub context | Public downloads; historical employment, not current job openings or hiring probability |
| [BLS Public Data API](https://www.bls.gov/developers/) | Occupation, wage and labor-market context | Public API; use metro/occupation context separately from current postings |
| [USAJOBS Search API](https://developer.usajobs.gov/api-reference/get-api-search) | Active federal job postings | Free requested key; covers federal announcements only, with worksite/remote/deduplication caveats |
| [WMATA developer resources](https://www.wmata.com/about/developers.html) | Metro schedule, real-time, alerts and accessibility source checks | Free; test unauthenticated/public surfaces first and use portal key only where an endpoint requires it |
| [Maryland MTA developer resources](https://www.mta.maryland.gov/developer-resources), [Virginia DRPT GTFS clearinghouse](https://drpt.virginia.gov/data/gtfs-feed-clearinghouse/) | MARC, VRE and local transit coverage | Public transit feeds; schedule data is not door-to-door route reliability |
| [OpenStreetMap](https://www.openstreetmap.org/copyright), Overpass and Nominatim policy pages | Amenities, services, street network and basic geocoding tests | Open data with attribution and fair-use/service limits; do not rely on public endpoints for heavy production traffic |
| DC/VA/MD local open-data and ArcGIS portals | Address points, parcels, parks, libraries, schools, childcare, local services | Public geospatial APIs/downloads; each layer needs freshness, geometry, rights and join review |
| [FEMA NFHL / MSC](https://msc.fema.gov/portal/home) | Flood hazard context | Official NFIP source; not a complete property hazard or insurance assessment |
| [NWS API](https://www.weather.gov/documentation/services-web-api), [NOAA CDO](https://www.ncdc.noaa.gov/cdo-web/webservices/v2) | Weather alerts, observations, climate normals and historical weather context | NWS is open/free; NOAA CDO uses a free token with rate limits |
| [AirNow API](https://docs.airnowapi.org/) | Air quality and smoke context | Free account/key; use source definitions and avoid treating readings as property-specific health advice |
| [FCC National Broadband Map data](https://help.bdc.fcc.gov/hc/en-us/articles/10467446103579-How-to-Use-the-FCC-s-National-Broadband-Map) | Broadband availability/provider context | Public downloads/API documentation; advertised availability may not prove service at a unit |
| [NCES CCD](https://nces.ed.gov/ccd/) | School directory, grades served and institutional identifiers | Public-use data; directory facts do not prove address assignment, eligibility or enrollment |
| [DC Child Development Centers](https://catalog.data.gov/dataset/child-development-centers) and equivalent VA/MD sources | Childcare proximity and licensed-provider context | Public datasets where available; presence/capacity does not prove price, hours, openings or fit |
| [Zillow Research market data](https://www.zillow.com/research/market-data/), [Redfin Data Center](https://www.redfin.com/news/data-center/) | Aggregate market/rent/inventory context | Free aggregate downloads; not live listing APIs or individual-property evidence |

Potential freemium listing/property APIs, including providers that advertise no-card
free tiers, remain evaluation-only until terms, rights, overage behavior, source
lineage and retention are reviewed. A free tier is not enough to satisfy the
zero-dollar source policy if it can silently create spend or prohibits the
intended use.

Proposed maximum evidence ages for an active pilot are: listing price/status 24 hours; route estimates 7 days with matching travel window and valid schedule; education access rechecked within 30 days and valid for target academic year; quotes through their stated expiry or 7 days when unspecified; other costs within 90 days plus the correct billing period; annual hazard/administrative layers checked for current edition within 90 days. These are product policies to validate against source SLAs, not claims about refresh availability. A provider with stricter terms or shorter expiry wins. A timestamp cannot make an obsolete academic year or canceled service current.

Store `observed_at`, `effective_from/to`, `published_at` when known, `retrieved_at`, `available_at`, source/version, and status. An as-of result must not use later-available revisions. If history is not licensed or available, label historical replay unavailable rather than substituting today's data. If retention rights prohibit full replay, retain allowed evidence/fingerprints and explicitly mark the run as not fully replayable; do not claim reproducibility from hashes alone.

Deduplication keeps offers distinct by source listing ID, property, unit, tenure, and effective terms. Ambiguous matches remain separate and flagged. Conflicting prices/availability are shown; the household may confirm its intended offer without overwriting the source. Address/unit and school/parcel spatial joins have cardinality tests, precision thresholds, and an ambiguity state. No silent fuzzy assignment at a boundary.

## 12. Privacy, fairness, and AI boundaries

Consent is granular: search, exact destination routing, finance connection, household collaboration, export, and monitoring are separate purposes. A household budget can remain private to its owner while a partner sees an approved shared envelope. Do not send financial state, private notes, dependent details, or complete destination sets to listing or map vendors. Send only the minimum permitted route query after disclosure. Precise coordinates and low-entropy address hashes remain sensitive.

Before real-household pilot, implement authentication, tenant isolation, encryption, access revocation, audit access controls, export redaction, and deletion. Proposed retention: no saved profile without opt-in; inactive saved searches expire after 12 months with notice; deletion blocks access immediately, removes active copies within 30 days, and expires backups within 90 days unless a documented obligation requires a different disclosed policy. These are implementation targets subject to source rights and approved privacy policy. Repository memory and telemetry contain no real addresses, household budgets, private routes, or listing payloads.

Do not use race, color, religion, national origin, sex, familial status, disability, or demographic proxies as neighborhood desirability inputs. User-directed functional accessibility and education requirements remain supported. Do not infer “people like you,” family status, school needs, religion, or socioeconomic identity from names, locations, browsing, or property choices. No protected-group composition map or political/religious neighborhood matching is part of this spec. No hidden paid/referral influence enters search, frontier, or ordering.

This is product policy, not a claim that all school/crime information is unlawful. HUD's April 24, 2026 guidance specifically addresses sharing school and neighborhood crime information; counsel must review current federal, state, and local requirements and intended product behavior. This spec keeps crime scoring out of the first release and requires evidence-grounded, user-directed school comparisons. [HUD guidance announcement](https://www.hud.gov/news/hud-no-26-028)

AI may turn a user's description into a proposed preference form, summarize source-grounded trade-offs, and draft verification questions. Users confirm extracted financial constraints and preferences. Deterministic tools calculate costs, geographic checks, feasibility, and order. Treat listing descriptions/documents as prompt-injection surfaces; they cannot change policies, access secrets, select tools, or authorize actions. Escape rendered source content and validate links. If AI explanation fails, use the same structured deterministic result with template text. No contact, application, tour booking, purchase, or account change is performed by this module without a separately scoped user action and supporting workflow.

## 13. Housing Decision Brief

One retained result produces both views:

- **Household view:** stated decision and date; search scope; baseline; 2–6 chosen comparison candidates; feasible/provisional labels; monthly, upfront and horizon costs; per-person travel; education/access facts; principal trade-offs; assumption sensitivity; unanswered questions; user shortlist and rationale. Include a source link and “checked” date beside consequential claims.
- **Reviewer view:** the same values plus input snapshot/version, candidate universe and excluded IDs/reasons, source rights/freshness, utility definitions/contributions, scenario configuration, geography/education join evidence, validation results, coverage policy, approval history and permitted replay manifest.

Show selected candidates versus the full frontier count, and why any candidate was selected for display. No renderer recalculates values. Exports carry the as-of date and expiry/refresh warnings. A share/export preview defaults to omitting exact work/care addresses, private member notes, raw finance inputs, and dependent details; candidate listing addresses may be included when the user chooses and source rights permit. No publicly accessible share links by default.

## 14. Non-functional requirements

All thresholds are proposed pilot acceptance targets, not measured results.

| ID | Requirement | Owner / verification |
|---|---|---|
| NFR-HOME-001 | Identical canonical inputs, source snapshots, policies, engine versions, and seed if used produce identical numerical results and classifications; currency ledgers reconcile to $0.01. | Engineering / deterministic fixtures |
| NFR-HOME-002 | Every material displayed claim has provenance and status; every critical unknown blocks a definitive feasibility claim. | Data / adversarial missingness cases |
| NFR-HOME-003 | For 500 pre-enriched candidates, 20 active dimensions, 4 members and 12 scenarios on a declared 4-vCPU/8-GB reference host: cached preference recompute p95 <= 2 seconds and full deterministic comparison p95 <= 5 seconds over 100 runs. External enrichment has a 30-second budget and explicit partial results. | Engineering / benchmark |
| NFR-HOME-004 | Enforce household isolation, role/purpose permissions, revocation, and export/deletion policy with no raw household data in logs or repository artifacts. | Security / negative access and deletion tests |
| NFR-HOME-005 | Meet [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) for the released workflow, including keyboard, screen reader, contrast, chart alternatives and non-map access; mobile supports 360px viewport without losing comparison content. | Design / automated and manual review |
| NFR-HOME-006 | Source, adapter and AI failures degrade to clearly limited results or a closed gate; retries are bounded and idempotent; disabling a region/source halts affected recommendations and alerts. | Operations / fault injection |
| NFR-HOME-007 | Every live region has an accountable owner, itemized per-comparison data/compute cost, approved monthly budget, and hard spend/rate caps; no live source runs with an unset budget. | Operations / budget and load evidence |
| NFR-HOME-008 | Equivalent declared needs and evidence produce identical results regardless of irrelevant identity fields; explain all ordering, source coverage, and sponsorship exclusions. | Model Risk / invariance and expert review |

## 15. Acceptance, release gates, and validation status

The engineering companion maps every requirement and NFR to an acceptance criterion, test method, proposed task, and owner role. Tests do not exist yet; no criterion is claimed passed. Tests must cite the stable `AC-HOME-*` ID when implemented. Registry/gating fixtures cover all ten region IDs, including disabled/unsupported behavior. Detailed synthetic golden cases first cover the DC-area configuration, both tenure modes, household conflicts, sparse evidence, and incompatible eligibility/time assumptions; each later region needs its own equivalent evidence before admission.

| Gate | Required evidence | Current state |
|---|---|---|
| GATE-HOME-0 — Extension admission | Spec review; target job/buyer/baseline; incremental-value discovery; minimum-data rationale; domain/privacy boundaries; household conflict and fallback policies; semantic reuse review covering REQ-EXT-001 through REQ-EXT-007 | Open; this draft supplies a proposal, not proof |
| GATE-HOME-1 — Synthetic engine | Approved spec/plan; cost reconciliation; feasibility/frontier invariants; sensitivity; all core acceptance cases; no real household data | Not started |
| GATE-HOME-2 — Evidence and interface | Region/source registry, permitted data, education joins, accessible end-to-end workflow, exports and failures | Not started |
| GATE-HOME-3 — Region pilot admission | Named accountable owners; both-tenure coverage audit; privacy/security/legal review; budget; retention; independent correctness review; operations/rollback | Not started for all ten regions |
| GATE-HOME-4 — Expansion | Per-region usability and outcome evidence, coverage/cost within limits, no unresolved severe incident, documented change approval | Not started |

No all-ten-ready assertion follows from one successful market. DC-area work is the first priority; research in other regions is optional and does not block it. The [DC-area companion](dc-area-pilot.md) defines the proposed core footprint, source investigations, complete first search journey and local benchmark under existing requirement IDs. Parent Specs 007 and 010 remain authoritative for program-level expansion.

DEC-HOME-012 prioritizes read-only source feasibility before product implementation.
This research may inspect permitted live public data without asserting GATE-HOME-0
through GATE-HOME-3 are passed. A live source check does not establish accurate
rankings, complete listing coverage, household-data readiness or a live pilot.

## 16. Risks and decisions still needed

| ID | Risk | Mitigation / blocking evidence |
|---|---|---|
| RISK-HOME-001 | Sparse, duplicate, stale, or unlicensed listings create misleading choice sets. | Provider contracts, listing-state checks, candidate-universe disclosure, manual fallback; Data owner |
| RISK-HOME-002 | Cost omissions, double-counted principal/escrow, and inconsistent horizons reverse buy/rent conclusions. | Independent ledger fixtures, quote expiry, terminal reconciliation, same scenarios; Finance owner |
| RISK-HOME-003 | A school label implies admission or current boundaries that cannot be verified. | Address/year/grade evidence, explicit enrollment states, district review; Education owner |
| RISK-HOME-004 | Scores conceal value judgments, demographic proxies, or household disagreement. | User-defined objectives, frontier, invariance tests, vetoes, no universal area score; Model Risk owner |
| RISK-HOME-005 | Home/work/school coordinates, budgets, or exports expose private household information. | Minimized collection, consented queries, isolation, redaction, deletion and breach controls; Privacy owner |
| RISK-HOME-006 | Ten markets multiply source, local-rule, and operational work beyond capacity. | Independent gates, staged waves, data-rights audit, capped spend and clear unsupported coverage; Product owner |
| RISK-HOME-007 | Deterministic results look like guaranteed affordability, investment returns, or safe/ideal living conditions. | Precise estimate labels, bounded cases, no probabilistic certainty, explain missing evidence; Product/Domain owner |
| RISK-HOME-008 | Search experience becomes a large portal without improving decisions. | Compare with current process; track trade-off comprehension and wasted verification, not clicks; Research owner |
| RISK-HOME-009 | Current synthetic financial prototypes are mistaken for production privacy or local-tax infrastructure. | Explicit adapters and independent live-data gate; never flip synthetic flags to permit real data; Platform owner |
| RISK-HOME-010 | Provider corrections, license changes, or discontinued data break replay and alerts. | Permitted snapshot retention, source versioning, revocation controls, explicit replay limits; Data Ops owner |
| RISK-HOME-011 | Historical employment or duplicated postings imply current career opportunity at an exact street. | Separate evidence types, vintage/worksite checks, deduplication, conservative accessibility counts; Labor Data owner |
| RISK-HOME-012 | Town/street recommendations conceal variation, sparse inventory, or boundary errors. | Explicit segments, origin sampling, sparse-data suppression, independent address checks; Geospatial owner |

Open decisions for the next review:

1. Approve the core/outer-ring footprint and first activated capabilities for the confirmed DC-area focus; retain the other nine regions for subsequent sequencing after source audit.
2. Choose which objective inputs are enabled by default within the confirmed detailed education, job-access, and town/street scope. Proposed default: education and job interests optional, money/time/property fit visible, no prefilled household utility weights.
3. Select initial buyer/renter recruitment segments, accountable product/domain owners, and the target decision window.
4. Choose candidate feed, routing/geocoding, mapping, education, and hazard suppliers after rights, coverage, freshness, privacy, and cost evaluation; no contract is assumed.
5. Decide whether first controlled users need collaborative accounts immediately; synthetic prototype supports separate profiles locally, while live sharing waits for tested permissions.
6. Approve cost assumptions, source freshness policy, retention, operational budgets, and the measurable pilot thresholds in the companion.
7. Validate pricing as a search-period pass or subscription through research. Do not monetize ranking or treat vendor referral revenue as user value.

For the immediate live-data milestone, the user selected a $0 data/API budget.
Use public APIs, no-key reads, government/agency developer feeds and manual
authorized candidates only. Exclude any source that requires a paid billing path,
payment method, enabled overages or uncertain free-tier controls. Do not create
paid accounts, assume full active-listing coverage or continue queries after a
free quota is exhausted. The exact first source sample can use the proposed DC
core footprint without claiming that the full footprint or outer ring is
approved.

## 17. Source and repository provenance

Prepared from the master handoff, Specs 002–010 and 012, current Python household/optimizer/governance code, platform memory, and the read-only SDK's spec-driven development, engineering principles, memory, data-quality and point-in-time guidance. Existing Spec 011 behavior remains unchanged; this spec defines a separate housing result contract.

External primary sources linked in this spec and the pilot companion were researched September 26, 2026. They support specific data/behavior distinctions, not a completed vendor audit, legal determination, or validation of the ten-market business case. Recheck time-sensitive guidance before implementation or pilot.

The September 27 DC-area refinement adds the user's confirmed first-market priority and primary-source research in its companion. It changes sequencing, not the ten-region roster or stable requirement IDs.

The repository was clean and `main` equaled freshly fetched `origin/main` at `f8daefb` before creating `HomeSweetHomeOptimization`. This handoff adds documentation only. It does not collect household data, acquire providers, implement the engine, publish a service, or imply passed acceptance tests.
