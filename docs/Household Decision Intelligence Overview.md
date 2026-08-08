# Household Decision Intelligence Platform

## Master Product Specification and Research Roadmap

**Status:** Draft for product discovery and approval  
**Version:** 0.2  
**Date:** August 8, 2026  
**Initial product:** Household Capital Allocation Optimizer (HCAO)  
**Long-term category:** Household Decision Intelligence (HDI)

---

## 1. Executive decision

Build a household decision-intelligence platform that begins by answering one narrow, economically measurable question:

> Given this household's goals, constraints, accounts, debts, taxes, and uncertainty, what is the highest-value use of its next dollar?

The initial product must not behave like a stock picker, budgeting dashboard, robo-adviser, or autonomous financial adviser. It must generate transparent, scenario-dependent allocation plans; identify binding constraints; compare alternatives; quantify uncertainty; and leave consequential actions under user or professional control.

The financial product is the commercial wedge because value can be measured in dollars, willingness to pay can be tested, and recommendations can be validated. The longer-term platform can extend the same decision architecture across time, career, benefits, housing, family logistics, resilience, health-supporting routines, major purchases, location, and goal sequencing.

The central product thesis is:

> Households do not have separate money, calendar, career, and family problems. They have one constrained resource-allocation problem observed through different applications.

The platform operating thesis is:

> AI orchestrates the workflow; deterministic, versioned tools handle the math. Every material decision is grounded in approved institutional data and user-controlled configurations, with a complete audit trail from source to proposal to approval to monitoring.

This distinction is constitutional. A language model may discover intent, gather missing context, route work, retrieve evidence, summarize trade-offs, and explain verified results. It may not invent balances, tax rules, plan terms, eligibility, forecasts, constraints, calculations, optimized allocations, or monitoring outcomes. Those outputs must come from approved data sources and testable decision tools.

### Recommended initial beachhead

Launch with financially sophisticated but operationally underserved U.S. households:

- Ages approximately 28–50.
- Household income roughly $150,000–$500,000.
- Multiple account types, debts, benefits, or near-term goals.
- At least one complicating factor such as variable compensation, equity compensation, student debt, childcare, a home purchase, self-employment, or competing savings goals.
- Too complex for a simple calculator but below—or unwilling to pay for—the traditional private-wealth threshold.

### Recommended distribution strategy

Validate direct-to-consumer demand, but design for an eventual B2B2C distribution model through fee-only advisers, CPAs, employers, benefits platforms, and financial-wellness providers. Consumer acquisition can be expensive; a professional channel can supply trust, distribution, review, and higher-value cases.

### Domain positioning

The product should feel like an unusually rigorous financial planner with institutional decision infrastructure—not an investment analyst, portfolio expert, security-research terminal, or trading assistant.

Its primary object is the household rather than the portfolio. Investments are one resource inside a broader plan that also includes cash flow, debt, taxes, benefits, insurance, liquidity, housing, dependents, career decisions, time horizons, and life events. Portfolio construction is relevant only insofar as it supports household goals and constraints.

The domain boundary should remain narrow enough to build genuine expertise:

- **Own:** household capital allocation, goal funding, liquidity, debt, taxes, benefits, retirement decisions, major life decisions, household risk, and cross-domain trade-offs.
- **Integrate:** institutional capital-market assumptions, portfolio analytics, tax engines, benefit rules, account data, planning policies, and approved product catalogs.
- **Do not become:** a stock picker, earnings-research product, trading terminal, generic chatbot, social-investing network, or unconstrained “optimize my life” assistant.

### Core enterprise value proposition

For advisers, planners, wealth-management teams, and CIO organizations, the platform shall support a governed transformation:

> Convert institutional research, approved assumptions, planning policies, and household configurations into personalized, reviewable strategies at scale—without requiring professionals to repeat data gathering, calculations, proposal assembly, monitoring, and documentation for every client.

“Without adding operational burden” is a target that must be measured, not assumed. The product must demonstrate lower preparation time, fewer manual handoffs, reduced rework, and controlled exception rates before making that claim commercially.

---

## 2. Request restatement

Define a fully scoped, testable product and research program that launches a Household Capital Allocation Optimizer and deliberately expands it into a modular household and life optimization platform, including market-sizing research, validation gates, requirements, risks, success metrics, and future-module sequencing.

---

## 3. Problem statement

Households make interdependent decisions using fragmented tools. A retirement calculator may recommend increasing contributions without recognizing a fragile emergency reserve. A budgeting app may recommend surplus saving without valuing an employer match. A brokerage may optimize investments held on its platform without observing outside debt, benefits, tax constraints, childcare costs, or near-term goals. Calendar and productivity tools optimize task placement without reflecting the monetary or energy consequences of those choices.

The user therefore receives locally reasonable but globally inconsistent advice.

The initial use case is to allocate incremental and existing household financial resources across competing uses while respecting liquidity, taxes, risk, deadlines, household preferences, and uncertainty. The long-term use case is to optimize the household's broader portfolio of scarce resources—money, time, energy, attention, flexibility, and risk capacity—without pretending that subjective life choices have one objectively correct answer.

---

## 4. Research question versus engineering requirement

### Research question

Can an explainable, constraint-aware household optimizer produce recommendations that users judge to be more useful, trustworthy, and economically valuable than calculators, rules of thumb, or generalized financial-planning outputs?

### Engineering requirement

Create a secure and auditable decision system that converts verified household inputs and explicit preferences into feasible allocation alternatives, scenario results, binding-constraint explanations, and user-approved action plans.

### Business question

Is there a sufficiently large segment that experiences this problem frequently, trusts a product to analyze it, and will pay enough—directly or through an intermediary—to support customer acquisition, data connectivity, compliance, service, and model-governance costs?

---

## 5. Product principles

1. **Optimize decisions, not engagement.** Success is improved household outcomes, not screen time.
2. **Advice must be conditional.** Recommendations state the assumptions, preferences, and scenarios under which they are preferred.
3. **Feasibility precedes optimality.** A mathematically attractive but operationally impossible plan is a failure.
4. **The household controls its objective.** The system presents trade-offs and Pareto-efficient choices instead of inventing a universal definition of a good life.
5. **Uncertainty is visible.** Point forecasts cannot masquerade as certainty.
6. **No silent automation.** Material transfers, trades, elections, applications, cancellations, or schedule changes require affirmative authorization.
7. **Explanations are decision artifacts.** Every recommendation must identify its main drivers, binding constraints, opportunity cost, and important alternatives.
8. **Fairness is a constraint.** Household labor, inconvenience, risk, and flexibility cannot be assigned to the least vocal household member merely because doing so is efficient.
9. **Progressive data access.** Ask for the minimum data required for the current decision and earn access to more sensitive sources over time.
10. **Modules must stand alone.** Each extension requires an independent problem, buyer, validation test, safety boundary, and economic case.

---

## 6. Users, buyers, and jobs to be done

### Primary end user

An adult or couple with competing financial priorities who wants a defensible action plan rather than another account dashboard.

### Secondary users

- Fee-only financial planners and RIAs.
- CPAs and tax planners.
- Employer financial-wellness and benefits teams.
- Benefits brokers and platforms.
- Coaches operating within clearly defined non-regulated boundaries.

### Economic buyers

- Household subscription buyer.
- Adviser or CPA purchasing seats or household cases.
- Employer paying per eligible employee or active household.
- Platform purchasing an API or white-label decision module.

### Core jobs to be done

- “Tell me what to do with my next dollar and why.”
- “Show me what I give up when I fund one goal instead of another.”
- “Tell me which constraint is actually limiting the plan.”
- “Stress-test the plan before I commit.”
- “Update the recommendation when my life changes.”
- “Give me an explanation I can review with my spouse, adviser, or accountant.”

### Professional jobs to be done

- “Turn a client conversation into a complete, reviewable planning case without rekeying the same facts.”
- “Apply our approved assumptions and policies consistently across households while preserving individual configuration.”
- “Generate a personalized proposal whose numbers can be reproduced independently.”
- “Know which households require attention, why, and what changed.”
- “Give an adviser or CIO control over assumptions, policies, exceptions, and approvals without making them operate every workflow manually.”

---

## 6A. Product experience: specialized labs

The platform shall be organized into interoperable labs or workspaces. A lab is a focused decision environment with a defined purpose, inputs, permitted tools, output contract, and audit requirements. Labs share the same governed household state and decision history; they must not become disconnected mini-applications with conflicting facts.

### 1. Conversational Research Lab

Purpose: help households and professionals investigate planning questions using grounded evidence.

Representative questions:

- Should excess cash fund the mortgage, retirement accounts, or a home-purchase reserve?
- What changes if one partner stops working for two years?
- Which assumptions drive the Roth-versus-traditional recommendation?
- How would relocating change taxes, commuting, housing, childcare, and goal feasibility?

Requirements:

- **REQ-LAB-001 — Must:** The lab shall answer material factual questions only from approved household data, institutional data, retrieved primary evidence, or explicitly labeled assumptions.
- **REQ-LAB-002 — Must:** It shall distinguish sourced facts, deterministic calculations, model estimates, user preferences, and narrative interpretation.
- **REQ-LAB-003 — Must:** Every numerical claim shall link to a calculation result or approved source version.
- **REQ-LAB-004 — Must:** Conversation shall be able to initiate a scenario or proposal workflow but shall not itself become the calculation engine.
- **REQ-LAB-005 — Should:** Research findings shall be saveable as evidence attached to a household decision case.

### 2. Household Planning Lab

Purpose: create and maintain the household's whole-picture plan across capital, liabilities, benefits, goals, and constraints.

- **REQ-LAB-010 — Must:** The lab shall expose a household balance sheet, cash-flow view, goal map, liquidity position, decision calendar, and unresolved data issues.
- **REQ-LAB-011 — Must:** Users shall be able to configure household-specific priorities, limits, exclusions, and preferences without modifying institutional assumptions.
- **REQ-LAB-012 — Must:** The lab shall identify binding constraints, conflicting goals, and the marginal value of relaxing material constraints.
- **REQ-LAB-013 — Should:** The lab shall maintain a current plan and compare it with proposed revisions.

### 3. Scenario and Optimization Lab

Purpose: run reproducible what-if analysis and determine feasible, Pareto-efficient action alternatives.

- **REQ-LAB-020 — Must:** All calculations and optimization results shall be produced by registered, versioned deterministic tools or explicitly governed stochastic models.
- **REQ-LAB-021 — Must:** Each run shall retain inputs, configurations, assumptions, constraints, tool versions, outputs, validation results, and run status.
- **REQ-LAB-022 — Must:** The lab shall compare the current plan, transparent baseline, recommended alternative, and material counterfactuals under identical scenarios.
- **REQ-LAB-023 — Must:** A failed, timed-out, infeasible, or unvalidated run shall never be narrated as a successful recommendation.
- **REQ-LAB-024 — Should:** Professionals shall be able to lock approved institutional assumptions while allowing household-specific overlays within permissions.

### 4. Personalized Proposal Lab

Purpose: convert approved analysis into a client-ready plan or decision proposal.

- **REQ-LAB-030 — Must:** A proposal shall be generated only from validated outputs and approved evidence; prose generation may not alter calculated values.
- **REQ-LAB-031 — Must:** Every proposal shall show goals, recommended actions, timing, assumptions, trade-offs, alternatives, risks, disclosures, and required approvals.
- **REQ-LAB-032 — Must:** Proposal numbers shall reconcile exactly with the underlying decision record.
- **REQ-LAB-033 — Must:** Draft, reviewed, approved, delivered, superseded, and rejected states shall be distinct and auditable.
- **REQ-LAB-034 — Should:** The same verified result may be rendered for household, adviser, investment committee, or compliance audiences without changing its meaning.
- **REQ-LAB-035 — Could:** Organization-approved templates may provide branded narratives and disclosures while preserving evidence lineage.

### 5. Monitoring and Alerts Lab

Purpose: detect when observed state diverges from the approved plan or when a decision should be revisited.

- **REQ-LAB-040 — Must:** Monitoring shall evaluate versioned rules against refreshed household and institutional data.
- **REQ-LAB-041 — Must:** Alerts shall state the observed change, breached rule or threshold, affected decision, materiality, confidence, and recommended review path.
- **REQ-LAB-042 — Must:** An alert shall never be presented as an executed action.
- **REQ-LAB-043 — Must:** Alert deduplication, severity, cooldown, acknowledgement, escalation, and closure states shall be auditable.
- **REQ-LAB-044 — Should:** Users and organizations shall configure thresholds within governed ranges.
- **REQ-LAB-045 — Should:** The lab shall prioritize exceptions by household impact and urgency rather than generating a high-volume notification stream.

### 6. Adviser and CIO Console

Purpose: allow professional organizations to govern assumptions, policies, workflows, cases, exceptions, approvals, and client segmentation at scale.

- **REQ-LAB-050 — Must:** Authorized users shall manage approved capital-market assumptions, policy parameters, planning rules, product constraints, review thresholds, and effective dates.
- **REQ-LAB-051 — Must:** Institutional configuration shall be separated from household configuration, with an explicit precedence policy and change log.
- **REQ-LAB-052 — Must:** Professionals shall view cases requiring review, stale data, failed calculations, policy exceptions, upcoming decisions, and unresolved alerts.
- **REQ-LAB-053 — Must:** Batch personalization shall preserve household-level constraints and shall not replace individual suitability or required professional review.
- **REQ-LAB-054 — Should:** The console shall report operational burden, preparation time, exception volume, reviewer capacity, and recommendation consistency.

### 7. Governance and Audit Lab

Purpose: provide end-to-end evidence, reproducibility, approvals, controls, and investigation.

- **REQ-LAB-060 — Must:** An authorized reviewer shall reconstruct a material recommendation from its source snapshots, configurations, tool calls, outputs, validation, narrative version, and approvals.
- **REQ-LAB-061 — Must:** The lab shall expose lineage from institutional source and household field through calculation and proposal claim.
- **REQ-LAB-062 — Must:** It shall support comparison across decision versions and identify which input, policy, assumption, tool, or approval changed.
- **REQ-LAB-063 — Must:** It shall record human overrides and reasons without silently treating the override as model truth.
- **REQ-LAB-064 — Should:** Governance teams shall monitor tool reliability, explanation fidelity, policy exceptions, data quality, drift, and subgroup outcomes.

### Future lab candidates

- Benefits and Compensation Lab.
- Equity Compensation Lab.
- Retirement and Drawdown Lab.
- Household Resilience Lab.
- Housing and Location Lab.
- Career Capital Lab.
- Time and Family Logistics Lab.

Candidate labs remain subject to the extension admission requirements in Section 15.

---

## 6B. Governed AI operating model

### Separation of responsibilities

| Layer | Permitted responsibilities | Prohibited responsibilities |
|---|---|---|
| Conversational AI | Intent discovery, clarification, workflow routing, evidence retrieval, tool selection, summarization, explanation, drafting, exception triage | Inventing facts, performing authoritative math in free text, changing approved inputs, bypassing tools, approving actions |
| Deterministic tools | Tax and benefit calculations, cash-flow projection, constraint validation, reconciliation, optimization, eligibility rules, thresholds, alert evaluation | Unreviewed narrative interpretation, silent use of missing data, unsupported jurisdictions |
| Governed statistical/ML models | Forecasting defined uncertain inputs, classification, prioritization, anomaly detection, calibrated scenario estimates | Presenting estimates as rules or facts, overriding hard constraints, autonomous approval |
| Institutional data and policy | Approved assumptions, policies, source data, product constraints, planning standards | Silent household-specific modification |
| Household configuration | Goals, facts, preferences, restrictions, permissions, approvals | Modification of institutional source history or governing rules |
| Human professional | Judgment, exception review, suitability assessment where applicable, interpretation, approval, client communication | Undocumented overrides or retroactive alteration of the audit record |

### Workflow requirements

- **REQ-AI-001 — Must:** AI shall construct a typed workflow plan that identifies the question, required facts, applicable jurisdictions, required tools, approvals, and expected output before a material recommendation is generated.
- **REQ-AI-002 — Must:** Tool inputs and outputs shall be schema-validated; malformed, incomplete, stale, or unauthorized calls shall fail closed.
- **REQ-AI-003 — Must:** AI shall quote or render numerical results only from the corresponding validated tool result or approved source.
- **REQ-AI-004 — Must:** The system shall independently verify reconciliation, hard constraints, rule coverage, and proposal-number consistency before delivery.
- **REQ-AI-005 — Must:** AI shall state uncertainty, missing information, unsupported scope, and required professional review without attempting to fill gaps through plausible language.
- **REQ-AI-006 — Must:** A change in wording, language model, or prompt shall not change the underlying deterministic result for identical approved inputs and tool versions.
- **REQ-AI-007 — Must:** The AI orchestration layer shall be replaceable without rewriting the household rule base, deterministic calculation engines, or audit history.
- **REQ-AI-008 — Must:** Every material AI step shall retain model identifier, orchestration version, retrieved evidence identifiers, tool calls, validation status, generated artifact version, and human approvals subject to privacy and retention policy.
- **REQ-AI-009 — Should:** Multiple AI-generated explanations may be tested for comprehension only after numerical and logical fidelity are locked.
- **REQ-AI-010 — Should:** The system shall detect narrative claims not supported by the retained calculation or evidence graph before a proposal is delivered.

### Reproducibility contract

For an identical approved input snapshot, institutional configuration, jurisdiction rule set, scenario, deterministic tool version, and tie-breaking policy, material calculations and recommended action sets shall reproduce within defined tolerances. If a governed stochastic model participates, its model version, calibration window, seed or distributional inputs, and permitted tolerance shall be retained.

AI response reproducibility is not an acceptable substitute for decision reproducibility. Fluent consistency can still reproduce an incorrect calculation; the platform must test both consistency and correctness against independent expected results.

---

## 7. Scope

### Phase 1 in scope

- U.S. household use cases.
- Cash, taxable investments, retirement accounts, HSA, 529, common consumer debts, emergency reserves, and user-defined goals.
- Employer-match logic and configurable contribution limits.
- Federal and state tax estimation for only those decision-jurisdiction combinations marked supported in the reviewed coverage matrix, explicitly labeled with scope and effective date.
- Single-period prioritization plus multi-period scenario planning.
- Deterministic baselines and stochastic scenarios.
- Manual entry and file import before production-grade account connectivity.
- Individual and two-adult household modeling.
- User-specified liquidity, risk, and goal constraints.
- Recommendations, alternatives, constraint diagnostics, and action checklists.
- User approval and professional-review workflows.
- Research sandbox using synthetic households.

### Explicitly out of scope for Phase 1

- Custody of assets or money movement.
- Trade execution.
- Filing tax returns.
- Legal, tax, medical, insurance, or fiduciary representation.
- Individual-security selection or return prediction.
- Autonomous borrowing, refinancing, benefit election, or account opening.
- Full estate planning.
- Business treasury optimization.
- International tax and non-U.S. regulatory coverage.
- Definitive eligibility determinations where authoritative plan or government data are unavailable.
- Claims that the plan is uniquely optimal for the user's life.
- Allowing a language model to perform or overwrite authoritative calculations, optimization results, eligibility, rule selection, or reconciliation in free-form text.

---

## 8. Phase 1 functional requirements

Priority definitions: **Must** is required for the first controlled pilot; **Should** is expected before broad commercialization; **Could** is deferred unless evidence elevates it.

### Household state and onboarding

- **REQ-001 — Must:** The product shall represent household members, dependents, income sources, recurring expenses, liquid reserves, accounts, debts, benefits, tax profile, goals, and constraints with effective dates.
- **REQ-002 — Must:** The product shall distinguish user-entered, imported, inferred, defaulted, stale, and unavailable values.
- **REQ-003 — Must:** The product shall show a completeness and freshness assessment before optimization.
- **REQ-004 — Must:** Users shall be able to correct, exclude, or override any imported or inferred value.
- **REQ-005 — Should:** Two household members shall be able to express separate preferences, non-negotiable constraints, and approval rights.
- **REQ-006 — Should:** The product shall support reusable household templates for common profiles without representing synthetic defaults as user facts.

### Goals and preferences

- **REQ-010 — Must:** Users shall be able to define goals with target amount or outcome, target date or horizon, priority, minimum acceptable outcome, and flexibility.
- **REQ-011 — Must:** The product shall permit hard constraints, soft preferences, and aspiration targets to be distinguished.
- **REQ-012 — Must:** The product shall show users how recommendation changes when a preference or constraint changes.
- **REQ-013 — Should:** The product shall surface contradictory goals and request prioritization rather than silently resolving them.
- **REQ-014 — Could:** The system may learn preference suggestions from prior accepted decisions, but users must confirm any material inferred preference.

### Baseline and allocation alternatives

- **REQ-020 — Must:** The product shall generate a rules-based baseline using configurable ordering logic so the optimized plan can be compared with a transparent benchmark.
- **REQ-021 — Must:** The product shall allocate incremental cash across eligible uses while satisfying hard constraints.
- **REQ-022 — Must:** The product shall support a multi-period plan with user-selectable horizon and time step.
- **REQ-023 — Must:** The product shall produce at least three feasible alternatives when meaningful trade-offs exist: recommended, liquidity-preserving, and goal-acceleration variants.
- **REQ-024 — Must:** The system shall report infeasibility and identify the minimum conflicting constraint set or equivalent actionable diagnosis.
- **REQ-025 — Must:** Every output shall reconcile sources and uses of funds.
- **REQ-026 — Should:** The product shall support contribution limits, employer matches, debt minimums, prepayment rules, and configurable penalties.
- **REQ-027 — Should:** The product shall model transaction costs, taxes, lockups, settlement delay, and account access restrictions when relevant.

### Risk, uncertainty, and scenarios

- **REQ-030 — Must:** The product shall support user-defined deterministic stress scenarios for income loss, unexpected expense, market decline, inflation, and goal-cost increase.
- **REQ-031 — Must:** The product shall display outcome ranges and scenario failure rates rather than only expected values.
- **REQ-032 — Must:** Users shall be able to distinguish sourced assumptions, model estimates, and subjective judgments.
- **REQ-033 — Should:** Scenario dependencies shall support correlated shocks rather than assuming all events are independent.
- **REQ-034 — Should:** The product shall compare the recommended plan with current behavior and the rules-based baseline across the same scenarios.
- **REQ-035 — Could:** Personalized probabilistic forecasts may be introduced only after calibration, drift, and subgroup performance are measured.

### Explanation and decision support

- **REQ-040 — Must:** Every recommendation shall state the decision, amount, timing, expected benefit, main assumptions, principal risks, and next-best alternative.
- **REQ-041 — Must:** The product shall identify binding constraints and explain the marginal value of relaxing important constraints in plain language.
- **REQ-042 — Must:** The product shall show opportunity cost: which other goals or allocations receive less funding and why.
- **REQ-043 — Must:** Users shall be able to inspect the trace from household inputs to constraints, scenarios, and recommendation.
- **REQ-044 — Must:** The product shall generate a shareable decision summary suitable for review with a spouse or professional.
- **REQ-045 — Should:** Explanations shall be evaluated for fidelity to the actual decision model, not merely readability.

### Approval, monitoring, and change

- **REQ-050 — Must:** Material actions shall remain proposed until affirmatively approved by the required household member or professional reviewer.
- **REQ-051 — Must:** The system shall record recommendation version, input snapshot, assumptions, approval status, and subsequent user action.
- **REQ-052 — Must:** The product shall detect material changes to income, balances, debts, goals, or assumptions and indicate whether re-analysis is warranted.
- **REQ-053 — Should:** Users shall be able to compare a new plan with the prior approved plan and see exactly what changed.
- **REQ-054 — Could:** Read-only monitoring integrations may notify users of drift; they shall not execute corrective actions without explicit authorization.

### Research and administration

- **REQ-060 — Must:** Product researchers shall be able to run synthetic household cohorts through baseline and candidate decision policies.
- **REQ-061 — Must:** Every experiment shall retain model, rule, assumption, dataset, and evaluation versions.
- **REQ-062 — Must:** Product operators shall be able to disable a recommendation class, connector, model version, or module without disabling unrelated read-only functions.
- **REQ-063 — Should:** Reviewer tools shall support sampled decision audits and structured error classification.

---

## 9. Non-functional requirements

- **NFR-001 — Privacy, Must:** Collect only decision-relevant data; make permissions granular, revocable, and understandable.
- **NFR-002 — Security, Must:** Encrypt sensitive data in transit and at rest; enforce least privilege, strong authentication, environment separation, and auditable administrative access.
- **NFR-003 — Explainability, Must:** A recommendation must be reproducible from its retained input and versioned decision configuration.
- **NFR-004 — Reliability, Must:** No plan may be presented as feasible unless all declared hard constraints pass independent validation.
- **NFR-005 — Availability, Should:** User-facing read and scenario functions should meet a documented availability objective appropriate to a planning product; no life-critical dependency is implied.
- **NFR-006 — Latency, Must:** A standard household case should return an initial feasible plan quickly enough for an interactive session; exact service-level targets require prototype benchmarking before approval.
- **NFR-007 — Cost, Must:** Per-case compute and data cost shall be measured separately from acquisition and support costs before pricing is finalized.
- **NFR-008 — Capacity, Should:** The service shall support batch scenario analysis for adviser books without changing the meaning of household-level results.
- **NFR-009 — Accessibility, Must:** Core workflows and decision artifacts shall meet applicable accessibility standards and be usable without relying solely on color.
- **NFR-010 — Model governance, Must:** Learned models shall have documented purpose, training data, validation, limitations, monitoring, rollback, and owner.
- **NFR-011 — Auditability, Must:** Material calculations, policy changes, and user approvals shall be timestamped and attributable.
- **NFR-012 — Portability, Should:** Users shall be able to export their household inputs, assumptions, goals, and decision history in a usable format.
- **NFR-013 — Deletion, Must:** Users shall be able to request deletion consistent with legal retention requirements, with the retained exceptions disclosed.
- **NFR-014 — Safety, Must:** The product shall not generate definitive professional claims when required data, jurisdictional logic, or review authority is absent.
- **NFR-015 — Household fairness, Must:** Multi-person recommendations shall expose how costs, time, risk, and flexibility are distributed across members.
- **NFR-016 — Numerical reproducibility, Must:** Identical governed inputs and deterministic tool versions shall reproduce material calculations and action sets within approved tolerances.
- **NFR-017 — Narrative fidelity, Must:** Generated explanations and proposals shall not contradict or materially extend the validated evidence and calculation record.
- **NFR-018 — Jurisdiction freshness, Must:** Each decision type shall define maximum permitted rule age and a stop or review policy when that threshold is exceeded.
- **NFR-019 — Operational scalability, Must:** Adviser and CIO workflows shall measure preparation time, review time, exception volume, and manual handoffs at household and organization levels.

---

## 10. Decision-model research specification

This section establishes research requirements, not an approved implementation design.

### Candidate objective families

Research must compare—not prematurely select—at least the following:

1. Goal-attainment probability subject to liquidity and risk constraints.
2. Weighted goal shortfall minimization.
3. Expected lifetime utility with user-calibrated risk preferences.
4. Robust optimization against adverse but plausible parameter sets.
5. Multi-objective optimization producing a Pareto frontier.

### Required baselines

- User's current allocation behavior.
- Simple waterfall heuristic: minimum obligations, emergency reserve, employer match, high-cost debt, tax-advantaged savings, then taxable goals.
- Equal-priority allocation across goals.
- Deterministic point-estimate optimization.

### Required research comparisons

- Single-period versus multi-period decisions.
- Expected-value versus robust policies.
- Generic versus personalized risk and preference parameters.
- Independent versus correlated shocks.
- Exact, approximate, and heuristic decision policies where relevant.
- Financially optimized plan versus liquidity-first and simplicity-first plans.

### Evaluation metrics

- Feasibility rate.
- Goal-attainment probability and expected shortfall.
- Liquidity-failure probability.
- After-tax ending wealth or equivalent objective value.
- Regret relative to a hindsight benchmark, clearly labeled as retrospective.
- Sensitivity to assumption error.
- Stability of recommendations under small input changes.
- Explanation fidelity.
- User acceptance, override, and follow-through rates.
- Professional-review agreement and material-correction rate.
- Estimated and realized user value where measurable.
- Compute cost and time to usable result.

### Research rejection criteria

A candidate approach shall not advance if it:

- Produces unstable recommendations under immaterial input changes.
- Cannot explain important decision drivers faithfully.
- Improves expected wealth by sacrificing unacceptable liquidity or tail outcomes.
- Requires unavailable or unreliable inputs to outperform a simple heuristic.
- Creates personalization lift too small to justify additional sensitive data.
- Demonstrates systematic degradation for identifiable household segments without a safe fallback.

---

## 11. Data requirements and dependencies

### Minimum viable data

- Household members and dependents.
- Jurisdiction and filing assumptions.
- Net recurring and variable income.
- Essential and discretionary expenses.
- Cash and accessible reserves.
- Debt balances, rates, minimums, terms, and prepayment conditions.
- Account types, balances, contribution limits, and employer match.
- Goals, dates, priorities, and flexibility.
- Insurance deductibles or user-selected shock amounts.
- Liquidity and risk constraints.

### Enrichment data

- Tax lots and unrealized gains.
- Vesting schedules and variable compensation.
- Benefits plan documents.
- Mortgage, student-loan, and credit details.
- Historical household cash flows.
- Calendar, commute, and time-use data for later modules.
- Local housing, childcare, education, and transportation costs for later modules.

### Authoritative external dependencies to investigate

- Government contribution limits and tax parameters.
- Employer plan and benefit documents.
- Financial account and liability connectivity providers.
- Market and macroeconomic scenario data.
- Credit and lending data where the user authorizes access.
- Calendar and task platforms for later modules.

### Institutional data and configuration hierarchy

The platform shall distinguish and govern four information classes:

1. **Authoritative public rules:** federal and state statutes, regulations, agency guidance, limits, forms, and official program rules.
2. **Institutional research and policy:** approved capital-market assumptions, planning assumptions, risk policies, product eligibility, house views, and professional practice rules.
3. **Household configuration:** residency, employment locations, accounts, debts, goals, preferences, restrictions, benefits, and approvals.
4. **Observed state:** current balances, transactions, market data, plan progress, and triggering events.

- **REQ-DATA-001 — Must:** Each material field shall declare its information class, source, jurisdiction, effective date, freshness, owner, confidence or validation status, and permitted uses.
- **REQ-DATA-002 — Must:** The system shall apply a documented precedence policy when institutional policy, household configuration, and default assumptions differ.
- **REQ-DATA-003 — Must:** AI-generated narrative shall never be promoted into authoritative rules or household facts without a governed review or user confirmation process.
- **REQ-DATA-004 — Must:** Calculations shall fail safely or disclose a bounded assumption when a required authoritative rule or household configuration is absent.

### Data-quality requirements

- Freshness must be displayed at field and source level.
- Material contradictions must block or qualify the recommendation.
- Missing data must trigger a sensitivity range or a request for confirmation.
- Derived fields must retain lineage to raw input and transformation version.
- Future modules may not reuse sensitive data for unrelated purposes without explicit consent.

---

## 11A. United States jurisdiction intelligence moat

### Strategic requirement

The initial domain shall support the United States at the federal level and develop reviewed knowledge coverage across all 50 states. State coverage is not a static table of tax rates. It is an effective-dated decision layer that understands when a household's domicile, residence, work location, property location, account ownership, beneficiary, filing status, and life event change the analysis.

The jurisdiction layer can become a meaningful moat because useful household planning requires the intersection of many rule systems, while most consumer applications treat state as a superficial profile field. The moat, however, comes from reviewed rule coverage, change operations, testing, provenance, and decision integration—not from merely collecting state pages.

### Coverage domains

The 50-state research backlog shall evaluate, prioritize, and maintain rules relevant to supported decisions, including:

- Individual income taxes, brackets, deductions, credits, capital gains, interest, dividends, and alternative tax regimes.
- Residency, domicile, part-year residence, nonresident income, remote work, reciprocity, and income sourcing.
- Retirement-income exclusions, pension treatment, Social Security taxation, and state-specific retirement incentives.
- 529 deductions or credits, recapture provisions, eligible-plan restrictions, and state benefits.
- HSA conformity and other federal-state tax differences.
- Estate, inheritance, and gift-related state considerations within the approved planning boundary.
- Property tax, homestead programs, primary-residence benefits, transfer taxes, and relevant homeowner incentives.
- Community-property, equitable-distribution, tenancy, marital-property, and account-ownership implications where they affect a supported financial calculation.
- Creditor protection, bankruptcy-related state exemptions, homestead protection, and protected-account treatment, subject to legal-review boundaries.
- Insurance regulation, product availability, guaranty frameworks, and state program differences through appropriate approved sources.
- Paid leave, unemployment, disability, childcare, education, energy, and other state programs that materially affect household capital decisions.
- State and local benefit interactions where reliable coverage and operational maintenance are feasible.

Not every domain must launch simultaneously. Coverage must be declared per decision type and jurisdiction; “all 50 states” may not be claimed until the approved coverage matrix and tests pass for every state.

### Jurisdiction model requirements

- **REQ-JUR-001 — Must:** Every jurisdictional rule shall retain jurisdiction, legal or agency source, citation, rule type, effective-from date, effective-to date when applicable, published or reviewed date, interpretation status, reviewer, and supported decision uses.
- **REQ-JUR-002 — Must:** The system shall distinguish enacted, effective, proposed, expired, repealed, administratively interpreted, and organization-policy states.
- **REQ-JUR-003 — Must:** Calculations shall use the rule version effective for the decision date and shall preserve that version in the audit record.
- **REQ-JUR-004 — Must:** The household model shall support domicile, residence, work, property, and income-source jurisdictions as separate attributes.
- **REQ-JUR-005 — Must:** Multi-state cases shall identify overlapping claims, reciprocity, credits, source-income treatment, and unresolved ambiguity rather than assuming one state controls everything.
- **REQ-JUR-006 — Must:** Each supported decision type shall have a published state-coverage matrix showing full, partial, unsupported, and expert-review-required status.
- **REQ-JUR-007 — Must:** A recommendation that depends on an unsupported or stale state rule shall be blocked, bounded, or routed for qualified review.
- **REQ-JUR-008 — Must:** Material rule changes shall trigger impact analysis identifying affected calculations, households, proposals, monitoring rules, and disclosures.
- **REQ-JUR-009 — Must:** State-rule content shall be reviewed through a documented four-eyes process by appropriately qualified tax, legal, benefits, insurance, or planning specialists.
- **REQ-JUR-010 — Must:** The platform shall clearly communicate when it is providing planning analysis rather than a legal conclusion or tax-return position.
- **REQ-JUR-011 — Should:** The system shall compare current and alternative jurisdictions for an explicit household decision while showing moving costs, non-tax effects, uncertainty, and residency requirements.
- **REQ-JUR-012 — Should:** Institutional organizations shall be able to add reviewed interpretive guidance without overwriting the underlying public rule or source.
- **REQ-JUR-013 — Could:** District of Columbia and U.S. territories may be added through the same admission and coverage framework after the 50-state scope is validated.

### Source hierarchy

The default hierarchy shall be:

1. Statute, regulation, official administrative code, official form, or official agency publication.
2. Official federal or state agency website and formal guidance.
3. Approved licensed data provider with contractual update obligations.
4. Reviewed secondary professional authority used only when primary text requires interpretation.
5. General web content used solely for discovery, never as final authority for a material rule.

The IRS maintains links to official state government websites, while the NAIC maintains a directory of state insurance departments; these are useful discovery maps, not substitutes for retrieving and reviewing the controlling state material.[^irs-states][^naic-states]

### 50-state rollout strategy

Coverage shall be built by decision vertical, not by attempting a shallow “complete state profile” one state at a time.

Recommended order:

1. Residency, income tax, retirement income, 529, and HSA conformity for all 50 states.
2. Multi-state employment, reciprocity, remote work, and part-year transitions.
3. Property, homestead, housing, and major-purchase rules.
4. Insurance, benefits, paid leave, childcare, education, and resilience programs.
5. Estate, inheritance, marital property, and creditor-protection decision support, subject to tighter legal review.

### State coverage validation gates

- **GATE-J1 — Source completeness:** Every material rule used by a decision has a controlling or approved authoritative source and effective date.
- **GATE-J2 — Calculation accuracy:** Golden cases for every supported state and decision type match independently reviewed expected results.
- **GATE-J3 — Boundary accuracy:** Multi-state, part-year, remote-work, and conflicting-jurisdiction cases route correctly or stop safely.
- **GATE-J4 — Change operations:** A simulated rule change can be ingested, reviewed, tested, approved, deployed, and traced to affected households.
- **GATE-J5 — Coverage honesty:** Product claims and user interfaces match the actual coverage matrix with no implied national support where gaps remain.

### Moat metrics

- Percentage of state-decision cells with reviewed full coverage.
- Median days from authoritative publication to reviewed effective-dated update.
- State-rule golden-case pass rate.
- Number and severity of stale-rule or jurisdiction-selection defects.
- Percentage of recommendations whose state-specific advantage materially changes the plan.
- Professional time saved on state-rule research and documentation.
- Cross-state scenario usage and conversion.

---

## 12. Market and TAM research program

### Market definition

Measure the annual U.S. revenue pool for software-assisted household decision optimization, not the value of household assets and not all financial-advice revenue. Report asset pools only as evidence of economic stakes, never as software TAM.

### Initial evidence anchors

- U.S. retirement assets were $47.6 trillion at March 31, 2026 and represented 34% of household financial assets. This supports the magnitude of household capital but does not establish software revenue.[^ici-retirement]
- At year-end 2025, IRAs and defined-contribution plans held $19.2 trillion and $14.2 trillion respectively.[^ici-factbook]
- In the Federal Reserve's 2025 household survey, only 63% of adults could cover a hypothetical $400 emergency expense using cash or its equivalent, while 35% of non-retirees believed retirement saving was on track. These findings support simultaneous liquidity and long-horizon planning pain.[^fed-2025]
- The Census Bureau reported 29.8 million nonemployer businesses for 2022, supporting a potentially large variable-income and self-employed extension segment.[^census-nonemployer]

### TAM methods

Use three independent methods and reconcile them.

#### A. Bottom-up household subscription model

For each target segment:

\[
\text{TAM} = \text{eligible households} \times \text{problem incidence} \times \text{annual willingness to pay}
\]

Segments must be mutually exclusive or deduplicated:

- Complex mass-affluent households.
- Equity-compensated employees.
- Variable-income and self-employed households.
- Pre-retirement households.
- Young families with multiple competing goals.
- Households facing a major decision within 24 months.

#### B. Adviser/CPA B2B2C model

\[
\text{TAM} = \text{addressable firms} \times \text{eligible seats or households per firm} \times \text{annual contract value}
\]

Research must distinguish registered investment advisers, financial planners, CPA firms, tax preparers, and employee-benefits intermediaries rather than applying one price to all.

#### C. Value-based model

\[
\text{Revenue ceiling} = \text{addressable cases} \times \text{verified annual value created} \times \text{capturable share}
\]

Value categories may include avoided interest, captured employer match, avoided penalties, improved tax timing, reduced idle cash, lower insurance or benefit cost, and reduced professional preparation time. Investment returns should not be assumed or marketed as guaranteed value.

### SAM definition

The initial SAM should include U.S. households that:

- Meet the selected beachhead profile.
- Have at least three competing allocation uses.
- Can supply minimum viable data.
- Are reachable through the chosen consumer or professional channel.
- Fall within the supported tax, account, debt, and benefit rules.

### SOM method

Estimate a three-year obtainable market using channel capacity rather than a fixed percentage of TAM:

\[
\text{SOM} = \sum_c \left(
\text{qualified leads}_c
\times \text{conversion}_c
\times \text{retention}_c
\times \text{ARPA}_c
\right)
\]

Channels should include organic decision tools, paid acquisition, employer pilots, adviser/CPA partnerships, and platform/API partnerships.

### Required research sources

- Federal Reserve Survey of Consumer Finances and SHED microdata.
- U.S. Census household, income, self-employment, and business-owner data.
- Bureau of Labor Statistics compensation and benefit data.
- IRS Statistics of Income, contribution/tax parameters, and filing patterns.
- SEC and adviser registration data.
- ICI retirement and household investment ownership data.
- Public pricing and product-capability audits of competitors.
- Primary interviews, pricing tests, and landing-page experiments.

### Primary market-research questions

1. How frequently does the target household face a decision complex enough to require optimization?
2. Which trigger event produces the highest urgency: bonus, RSU vest, new child, home purchase, job change, tax season, inheritance, or retirement transition?
3. Does the customer pay for ongoing monitoring, a one-time decision, or professional review?
4. Which value proof converts best: dollars improved, risk reduced, time saved, or conflict reduced?
5. Which inputs are users willing to provide before seeing value?
6. Which recommendation types require a trusted professional in the loop?
7. What is the willingness to pay for consumer, adviser, employer, and API offerings?
8. How much implementation and support cost does each channel create?

### Research deliverables

- Segment taxonomy with non-overlapping population estimates.
- Competitive feature and positioning matrix.
- TAM/SAM/SOM model with low, base, and high scenarios.
- Sensitivity table for incidence, price, retention, and channel conversion.
- Interview repository with coded pain and trust themes.
- Van Westendorp or equivalent price-sensitivity study, supplemented by behavioral purchase tests.
- Unit-economics model including data, compute, support, compliance, and acquisition cost.
- Recommendation on initial buyer, wedge, pricing unit, and channel.

### Market-validation gates

- **GATE-M1 — Problem:** At least 20 of 30 qualified discovery participants describe a recent relevant decision, an unsatisfactory workaround, and a material consequence.
- **GATE-M2 — Trust:** At least half of prototype users are willing to provide the minimum viable data after reviewing the privacy and control model.
- **GATE-M3 — Value:** At least 60% of qualified pilot users rate the decision artifact materially more useful than their existing approach.
- **GATE-M4 — Payment:** Obtain behavioral evidence—paid pilot, refundable deposit, adviser LOI with budget, or employer pilot—not survey intent alone.
- **GATE-M5 — Economics:** Base-case gross margin and retention must support the selected acquisition channel; thresholds require a priced pilot.

---

## 13. Competitive research taxonomy

Do not define competition only as another optimizer. The alternative is often a spreadsheet, spouse discussion, CPA, adviser, search engine, rules-of-thumb article, or doing nothing.

Audit competitors across these categories:

- Budgeting and cash-flow applications.
- Robo-advisers and broker planning tools.
- Retirement and Social Security calculators.
- Debt repayment and refinancing tools.
- Tax planning and tax-loss products.
- Equity-compensation platforms.
- Adviser financial-planning software.
- Employer financial-wellness platforms.
- Personal AI assistants and calendar optimizers.
- Human financial planners, CPAs, coaches, and benefits counselors.

Score each on:

- Decision scope and household coverage.
- Optimization versus rules/calculation.
- Multi-period and uncertainty support.
- Tax, debt, liquidity, and benefit integration.
- Data portability.
- Explanation and constraint diagnostics.
- Human review.
- Execution capability and conflicts of interest.
- Pricing and target wealth level.
- Regulatory posture.
- Evidence of outcomes.

The desired white space is not “more features.” It is coordinated decisions across domains with transparent trade-offs and verified feasibility.

---

## 14. Extension portfolio

Each extension below is a candidate module, not an approved commitment. It must pass its own market, safety, data, and incremental-value gates.

| Module | Core decision | Initial buyer | Primary method | Key risk | Suggested sequence |
|---|---|---|---|---|---:|
| Tax-aware portfolio transition | How to move from current holdings to target exposures | Consumer/RIA/CPA | Multi-period optimization | Tax accuracy/advice boundary | 2 |
| Equity compensation and concentrated wealth | When and how to diversify RSUs/options or concentrated assets | Employee/RIA/employer | Stochastic optimization | Securities/tax regulation | 2 |
| Retirement drawdown | Account withdrawals, Roth conversions, claiming and spending | Pre-retiree/RIA/CPA | Dynamic programming/scenarios | Tax and longevity assumptions | 2 |
| Variable-income operating system | Taxes, reserves, retirement and safe spending under uncertain income | Self-employed/CPA | Robust optimization/forecasting | Noisy data | 2 |
| Benefits and compensation | Compare plans, benefits, job offers and household value | Employee/employer | Constraint and scenario analysis | Plan-document accuracy | 2 |
| Household resilience | Cheapest portfolio of liquidity, insurance, credit and contingencies | Consumer/adviser | Tail-risk optimization | Fear-based UX | 3 |
| Major-purchase timing | Whether and when to buy a home, vehicle, solar, education, etc. | Consumer/partner | Optimal stopping/scenarios | Referral conflicts | 3 |
| Housing and location | Where to live given cost, commute, schools, family and option value | Consumer/employer | Multi-objective/location optimization | Bias and subjective data | 3 |
| Career capital | Which job, skill, degree or path maximizes earnings, fit and option value | Consumer/employer | Real-options/scenarios | Labor-market bias | 3 |
| Time and energy | Allocate tasks to periods with appropriate time and predicted capacity | Consumer/employer | Scheduling/contextual prediction | Surveillance/health inference | 4 |
| Family logistics | Allocate childcare, chores, errands and shared time fairly | Household | Multi-agent scheduling | Reinforcing unequal labor | 4 |
| Goal portfolio | Select, sequence, pause or abandon competing goals | Consumer/coach | Portfolio/multi-objective optimization | Normative overreach | 4 |
| Health-supporting routines | Choose sustainable non-clinical routines and schedules | Consumer/employer | Bandits/causal research | Medical boundary/safety | 5 |
| Travel and routing | Optimize itineraries across money, time, energy and family needs | Consumer/partner | Routing/constraint optimization | Crowded market | Optional |
| Household digital twin | Simulate cross-domain life events using a unified state | Consumer/professional | Simulation/causal scenarios | False precision/privacy | Platform horizon |

---

## 15. Extension requirements

### Shared admission requirements

- **REQ-EXT-001 — Must:** A module shall define one consequential decision, target user, buyer, trigger event, baseline, and measurable outcome.
- **REQ-EXT-002 — Must:** A module shall demonstrate incremental value over the capital optimizer or current best alternative.
- **REQ-EXT-003 — Must:** A module shall specify the minimum additional data required and why each field is necessary.
- **REQ-EXT-004 — Must:** A module shall define its professional, regulatory, ethical, and autonomy boundaries before pilot.
- **REQ-EXT-005 — Must:** A module shall preserve household preference conflicts rather than combining them into an unexplained average.
- **REQ-EXT-006 — Must:** A module shall include a safe fallback when data, model confidence, or supported jurisdiction is insufficient.
- **REQ-EXT-007 — Should:** A module should reuse the household state and scenario definitions only where semantic equivalence is verified.

### Life-event simulator

- **REQ-LIFE-001 — Must:** Users shall compare at least two named life-event alternatives against a no-change baseline.
- **REQ-LIFE-002 — Must:** Results shall separately display money, time, risk, flexibility, and goal effects; the system shall not collapse them into one score by default.
- **REQ-LIFE-003 — Must:** The system shall identify which conclusions are robust and which reverse under plausible assumptions.
- **REQ-LIFE-004 — Must:** The product shall not issue normative directives on marriage, fertility, medical care, or other intimate decisions.

### Time, energy, and household coordination

- **REQ-TIME-001 — Must:** Users shall define protected time, non-negotiable obligations, recovery constraints, and fairness rules.
- **REQ-TIME-002 — Must:** The system shall quantify schedule fragility and retain buffers rather than optimizing all capacity away.
- **REQ-TIME-003 — Must:** Both affected adults shall approve recurring responsibility assignments.
- **REQ-TIME-004 — Should:** Predictions of task duration or energy fit shall expose uncertainty and allow correction.

### Career capital

- **REQ-CAR-001 — Must:** Comparisons shall include compensation, benefits, taxes, commute, flexibility, learning, stability, and user-defined values.
- **REQ-CAR-002 — Must:** The system shall separate sourced labor-market evidence from inferred future opportunity.
- **REQ-CAR-003 — Must:** Protected characteristics shall not be used to reduce recommendations or opportunity estimates.
- **REQ-CAR-004 — Should:** The module shall represent option value and path dependence rather than only next-year salary.

### Health-supporting routines

- **REQ-HLT-001 — Must:** The module shall be limited to non-diagnostic, non-treatment planning unless an appropriate regulated workflow and clinical oversight are established.
- **REQ-HLT-002 — Must:** Safety exclusions and escalation guidance shall be reviewed by qualified domain experts.
- **REQ-HLT-003 — Must:** The product shall not optimize engagement, weight, sleep, or exercise in a way that encourages compulsive or unsafe behavior.

---

## 16. Cross-module platform capabilities

The following are enduring product capabilities to validate and eventually design; they are not approval of a specific technical architecture.

### Household state

A time-indexed representation of people, resources, obligations, accounts, goals, constraints, preferences, permissions, and provenance.

### Scenario library

Reusable events such as job loss, bonus, market decline, new child, relocation, home purchase, medical expense, caregiving, education, and retirement. Scenario assumptions must remain editable and visible.

### Decision registry

Each decision type should define eligible actions, constraints, objective components, evidence requirements, explanation requirements, and approval rules.

### Preference and fairness model

Support individual preferences, household-level commitments, vetoes, minimum fairness constraints, and unresolved disagreement.

### Constraint diagnostics

Identify infeasibility, binding constraints, marginal values, conflicts, and actions that most efficiently relax the household's limiting constraint.

### Decision memory

Retain what was known, recommended, approved, rejected, and observed without assuming that a past preference remains valid forever.

### Outcome measurement

Measure whether approved actions occurred and whether the expected outcome materialized, while distinguishing causal evidence from correlation.

---

## 17. Phased roadmap and gates

Timing is evidence-dependent; phases are sequenced by learning, not calendar promises.

### Phase 0 — Discovery and falsification

Deliverables:

- 30–50 problem interviews across consumers, advisers, CPAs, and employers.
- Competitive workflow audit.
- Synthetic household corpus and decision taxonomy.
- Rules-based baseline.
- TAM v1 with explicit ranges.
- Regulatory issue map prepared with qualified counsel.
- Clickable decision-artifact prototype.

Exit gate:

- One beachhead, trigger event, buyer, pricing hypothesis, and measurable value proposition are selected.
- GATE-M1 and GATE-M2 pass.
- No unresolved regulatory issue makes the intended pilot impermissible.

### Phase 1 — Household capital allocation research prototype

Deliverables:

- Manual-input household case.
- Goal and constraint definition.
- Baseline and candidate allocation alternatives.
- Scenario and stress testing.
- Binding-constraint and opportunity-cost explanation.
- Reproducible decision record.
- Expert-reviewed synthetic evaluation suite.

Exit gate:

- All Phase 1 Must requirements pass on the supported case types.
- Optimized outputs are feasible and reconcile in 100% of validation cases.
- Expert material-error rate is below a threshold approved before testing.
- Recommendation instability is measured and acceptable.

### Phase 2 — Controlled human pilot

Deliverables:

- Secure onboarding and consent.
- Limited supported household profiles.
- Human review queue.
- User feedback and override capture.
- Paid or budget-backed pilot.

Exit gate:

- GATE-M3 and GATE-M4 pass.
- No severe unmitigated safety or privacy incident.
- Support burden and compute/data costs are measured.
- A repeat-use trigger is observed or the product is explicitly repositioned as a one-time decision service.

### Phase 3 — Professional and employer distribution

Deliverables:

- Adviser/CPA workspace.
- Role-based review and approval.
- Batch case monitoring.
- Organization-level audit and governance.
- Configurable policy boundaries.

Exit gate:

- At least two channel types show viable pipeline economics.
- Professional corrections improve outcomes without making delivery uneconomic.
- GATE-M5 passes.

### Phase 4 — Adjacent financial modules

Candidate order:

1. Equity compensation/concentrated wealth.
2. Tax-aware portfolio transition.
3. Retirement drawdown.
4. Variable income.
5. Benefits and total compensation.

Each requires separate approval and admission requirements.

### Phase 5 — Cross-domain life decisions

Introduce household resilience, major purchases, housing/location, and career capital. These remain scenario and decision modules rather than continuous autonomous control.

### Phase 6 — Household operating system

Only after cross-domain evidence exists, introduce time, energy, family logistics, and goal-portfolio coordination. The household digital twin is an emergent integration layer—not an MVP feature.

---

## 18. Validation program

### Offline validation

- Synthetic edge cases reviewed by financial-planning, tax, optimization, security, and compliance specialists.
- Property-based checks for conservation of cash, constraint satisfaction, and monotonicity where theoretically required.
- Scenario sensitivity and adversarial household cases.
- Comparison with transparent heuristics.
- Subgroup performance and data-missingness analysis.

### Prospective validation

- Observe decision usefulness before enabling any integration-led action.
- Pre-register primary pilot metrics and error classes.
- Separate recommendation acceptance from actual follow-through.
- Compare predicted and observed cash-flow or goal outcomes when consent and time horizon allow.
- Investigate overrides as potential model information rather than automatically treating them as user error.

### Human-factors validation

- Can users correctly state what the recommendation assumes?
- Can users identify the main trade-off and next-best alternative?
- Do users over-trust precise forecasts?
- Do couples perceive allocations as fair?
- Does the product reduce or increase decision anxiety?

### Red-team themes

- Missing account or debt.
- Incorrect plan document.
- Sudden income loss.
- Contradictory spouse preferences.
- Manipulated imported data.
- Overconfident tax estimate.
- Recommendation that changes dramatically around a threshold.
- User seeks medical, legal, or regulated advice through a general interface.
- Referral revenue conflicts with recommendation quality.

---

## 19. Success metrics

### North-star candidate

**Verified household decision value per active case**, reported with its composition and uncertainty rather than as one opaque score.

### Product metrics

- Time from onboarding to first decision artifact.
- Input completion and correction rate.
- Percentage of cases with at least two feasible alternatives.
- Recommendation comprehension.
- Acceptance, override, and follow-through rate.
- Repeat analysis triggered by a genuine household change.
- Household-member agreement or unresolved-conflict rate.

### Outcome metrics

- Captured employer match.
- Avoided high-cost interest or penalty.
- Improvement in liquidity coverage.
- Goal shortfall reduction.
- Estimated tax or benefit improvement, separately labeled.
- Reduced professional preparation time.
- User-reported decision confidence without increased overconfidence.

### Safety and quality metrics

- Material recommendation error rate.
- Hard-constraint violation rate.
- Unsupported-claim rate.
- Data freshness and contradiction rate.
- Severe privacy/security incidents.
- Professional correction and escalation rates.
- Stability under small input perturbations.
- Performance and error disparities across supported groups.

### Business metrics

- Paid conversion and retention by trigger event.
- Average revenue per household, adviser, employer, and API client.
- Gross margin after data, compute, review, and support.
- Customer acquisition cost and payback.
- Cases per professional reviewer.
- Expansion revenue from independently valuable modules.

---

## 20. Pricing hypotheses to test

Do not commit to one model before behavioral testing.

- Consumer subscription: recurring monitoring and re-optimization.
- Per-decision: home purchase, job offer, RSU sale, or retirement transition.
- Premium reviewed decision: software plus adviser or CPA review.
- Adviser/CPA platform: per seat, household, or completed case.
- Employer benefit: per eligible or activated employee.
- API/white-label: platform fee plus decision volume.

Avoid asset-based pricing in the initial product: it creates conflicts, narrows access, and makes a decision tool resemble conventional asset management.

---

## 21. Constraints and risks

- **RISK-001 — Regulatory perimeter:** Personalized recommendations may constitute regulated financial, tax, insurance, or other advice depending on product behavior and jurisdiction. **Mitigation:** obtain qualified counsel; restrict initial scope; define review and execution boundaries.
- **RISK-002 — False precision:** Long-horizon forecasts can look more certain than they are. **Mitigation:** ranges, scenario reversals, assumption visibility, and robust alternatives.
- **RISK-003 — Objective misspecification:** The mathematically optimized objective may not represent household welfare. **Mitigation:** multi-objective outputs, elicited preferences, vetoes, alternatives, and overrides.
- **RISK-004 — Data incompleteness:** Missing debts, accounts, benefits, or obligations can invalidate a plan. **Mitigation:** completeness checks, safe fallbacks, sensitivity bounds, and qualified recommendations.
- **RISK-005 — Automation bias:** Users may over-trust the system. **Mitigation:** decision education, human review, explicit uncertainty, and no silent execution.
- **RISK-006 — Privacy concentration:** A household digital twin creates an unusually sensitive data asset. **Mitigation:** progressive permissions, minimization, segmentation, deletion, strict access, and local/on-device evaluation where justified.
- **RISK-007 — Household fairness:** Efficiency may shift unpaid labor or risk to one member. **Mitigation:** member-level burden metrics, fairness constraints, shared approval, and disagreement preservation.
- **RISK-008 — Distribution economics:** Consumer acquisition may exceed lifetime value. **Mitigation:** event-driven wedges and B2B2C channels; prove payment before broad build-out.
- **RISK-009 — Incumbent bundling:** Brokerages and planning platforms can copy visible features. **Mitigation:** cross-domain constraint system, outcome data, professional workflow, portability, and audited decision quality.
- **RISK-010 — Recommendation instability:** Small changes may produce large action changes. **Mitigation:** stability penalties, tolerance bands, hysteresis, and user-visible sensitivity.
- **RISK-011 — Referral conflict:** Revenue from financial, insurance, real-estate, or lending partners may bias outputs. **Mitigation:** separate optimization from monetization; disclose and test conflicts; prefer subscription/platform revenue.
- **RISK-012 — Health and intimate decisions:** Later modules risk normative or medical overreach. **Mitigation:** explicit exclusions, expert review, and separate approval gates.
- **RISK-013 — LLM calculation leakage:** Conversational AI may answer directly instead of invoking governed tools. **Mitigation:** typed workflow plans, tool-required claim classes, output validation, unsupported-claim detection, and fail-closed delivery gates.
- **RISK-014 — Stale jurisdiction rules:** State law, agency guidance, limits, or interpretations may change after analysis. **Mitigation:** effective-dated registry, source monitoring, freshness thresholds, expert review, impact analysis, and decision re-evaluation.
- **RISK-015 — Multi-state ambiguity:** Domicile, residence, work, and income sourcing may not resolve deterministically. **Mitigation:** separate jurisdiction attributes, ambiguity detection, scenario comparison, and qualified legal or tax review.
- **RISK-016 — Shallow national coverage:** Marketing “50-state support” before decision-level validation could create material consumer harm. **Mitigation:** public coverage matrix, vertical rollout, golden cases, and claim controls.
- **RISK-017 — Institutional policy conflict:** House assumptions may conflict with public rules or household facts. **Mitigation:** information-class separation, precedence policy, effective dates, disclosure, and exception review.

---

## 22. Stakeholders and sign-offs

### Required before design approval

- Product owner: problem, beachhead, scope, metrics, and roadmap.
- Optimization/research lead: baselines, evaluation, stability, and decision validity.
- Financial-planning domain reviewer: household logic and workflow realism.
- Tax-domain reviewer: supported calculations and disclaimers.
- State-jurisdiction research owner: 50-state coverage matrix, source hierarchy, effective dating, and change operations.
- Qualified state tax/legal/benefits/insurance reviewers: sign-off for their supported rule domains.
- Privacy and security: data inventory, permissions, retention, threat model.
- Legal/compliance: regulatory perimeter, communications, professional review, and distribution model.
- UX research: comprehension, trust, household fairness, and accessibility.

### Required before controlled pilot

- Engineering owner.
- Model-risk or independent validation reviewer.
- Incident-response owner.
- Customer-support owner.
- Channel owner for consumer, adviser, CPA, or employer pilot.

---

## 23. Definition of done for this specification

This specification is ready to hand to product design only when:

- The initial beachhead and trigger event are approved.
- Phase 1 in-scope and out-of-scope boundaries are approved.
- All Must requirements have an owner and proposed acceptance method.
- The regulatory research questions have assigned counsel or compliance owners.
- Minimum viable data and unsupported cases are agreed.
- Market-research plan, interview cohort, and TAM definitions are approved.
- Primary pilot metrics and stop conditions are approved before testing.
- Open questions that could materially alter the product are resolved or explicitly deferred.

This document specifies WHAT and WHY. Detailed technical architecture, interface contracts, data schemas, solver selection, implementation tasks, and test plans should be produced only after specification approval and must trace to the stable requirement IDs.

---

## 24. Open questions

### Product and market

1. Which initial trigger is strongest: surplus cash, bonus, RSU vest, new child, home purchase, job change, tax season, or retirement transition?
2. Is the first economic buyer the household, adviser, CPA, employer, or platform?
3. Is the recurring product valuable enough to retain users, or should the wedge be sold per decision?
4. What minimum quantifiable benefit is needed for users to pay and provide sensitive data?
5. Should the initial positioning emphasize wealth improvement, resilience, reduced conflict, or decision confidence?

### Scope and regulation

6. Which recommendations can be offered as education or decision support, and which require registration, licensing, or professional review?
7. Which states and tax situations can be supported in the first pilot?
8. What records and disclosures must be retained for each distribution model?
9. Can employer sponsorship preserve employee privacy and perceived independence?

### Research and modeling

10. What objective representation is most comprehensible without sacrificing decision quality?
11. How should household members negotiate conflicting preferences and vetoes?
12. What stability threshold should prevent recommendation churn?
13. Which scenario probabilities can be estimated responsibly, and which should remain user-defined stresses?
14. How will realized value be attributed when many decisions and external events interact?

### Data and trust

15. Which data should be entered manually before account connectivity is justified?
16. What level of data freshness is required by decision type?
17. Which calculations should be performed locally or with privacy-preserving methods?
18. How will users correct a recommendation after discovering an omitted obligation?

### Extensions

19. Which financial extension creates the strongest cross-sell without expanding the regulatory perimeter disproportionately?
20. Which nonfinancial module has a measurable outcome and natural payment event?
21. At what point does cross-domain personalization create more privacy risk than user value?
22. What evidence would justify building a household digital twin rather than a set of loosely coupled decision modules?

### AI orchestration and professional workflow

23. Which numerical and rule-based claim classes always require a deterministic tool result?
24. Which decisions require adviser, planner, CPA, CIO, compliance, or household-member approval?
25. What reproducibility tolerances apply to optimized action sets when multiple solutions are economically equivalent?
26. Which institutional assumptions may households override, and how should precedence be disclosed?
27. What operational-burden baseline will be used to validate the enterprise value proposition?

### United States jurisdiction coverage

28. Which decision vertical supplies the best first 50-state coverage wedge: income tax, retirement, 529, benefits, or housing?
29. Which rule domains require licensed data, and which can be maintained from primary public sources?
30. What freshness thresholds and emergency update process apply by rule materiality?
31. How will local rules be handled when city or county treatment materially changes a decision?
32. Which multi-state cases must be routed to a qualified professional rather than calculated automatically?

---

## 25. Acceptance criteria

- **AC-001:** The approved pilot has one named beachhead, buyer, trigger event, and primary job to be done.
- **AC-002:** Every Phase 1 Must requirement has a documented test method and accountable owner.
- **AC-003:** All supported test cases produce plans that reconcile funds and satisfy declared hard constraints.
- **AC-004:** Unsupported, incomplete, contradictory, or infeasible cases generate a qualified result or safe refusal rather than a fabricated recommendation.
- **AC-005:** Each recommendation identifies assumptions, outcome range, binding constraints, opportunity costs, risks, and at least one alternative when an alternative exists.
- **AC-006:** A retained input and decision-version snapshot reproduces the material recommendation.
- **AC-007:** Users can correct data, change preferences, compare scenarios, reject recommendations, and export a decision artifact.
- **AC-008:** No material external action occurs without the required affirmative approval.
- **AC-009:** Independent domain review finds the material-error rate within the threshold approved before pilot launch.
- **AC-010:** The TAM/SAM/SOM analysis uses at least three methods, separates asset pools from revenue, deduplicates segments, exposes assumptions, and includes sensitivity ranges.
- **AC-011:** Market validation includes behavioral payment evidence, not stated interest alone.
- **AC-012:** Privacy, security, legal/compliance, accessibility, and incident-response reviews are complete before real household data enter a controlled pilot.
- **AC-013:** Every extension module passes REQ-EXT-001 through REQ-EXT-007 and receives explicit approval before development.
- **AC-014:** Pilot reporting includes decision quality, user comprehension, safety, economics, subgroup results, and professional corrections.
- **AC-015:** The product is paused or narrowed if severe safety incidents, infeasible recommendations, unsupported regulated claims, or unacceptable recommendation instability exceed pre-approved stop thresholds.
- **AC-016:** Identical approved inputs, configurations, jurisdiction rules, tool versions, and deterministic tie-breaking reproduce material calculations and recommendations within approved tolerances across repeated runs and supported interfaces.
- **AC-017:** Every numerical claim in research answers, proposals, and alerts traces to a validated tool output or approved source; unsupported claims are blocked before delivery.
- **AC-018:** The AI orchestration layer can be changed without altering deterministic golden-case results or historical audit reconstruction.
- **AC-019:** Each supported state-decision combination has authoritative sources, effective dates, independent golden cases, qualified review, and explicit coverage status.
- **AC-020:** Multi-state test cases distinguish domicile, residence, work, property, and income-source jurisdictions and either calculate within validated scope or route safely for review.
- **AC-021:** A simulated state-rule change produces a traceable impact list and re-evaluation path for affected households, proposals, and alerts.
- **AC-022:** The professional pilot measures whether the platform reduces preparation time, rekeying, manual handoffs, and rework without increasing material error or exception burden.

---

## Source notes

[^ici-retirement]: Investment Company Institute, “Retirement Assets Total $47.6 Trillion in First Quarter 2026,” June 18, 2026: https://www.ici.org/statistical-report/ret_26_q1
[^ici-factbook]: Investment Company Institute, *2026 Investment Company Fact Book: Quick Facts Guide*: https://www.ici.org/system/files/2026-04/2026-factbook-quick-facts-guide.pdf
[^fed-2025]: Board of Governors of the Federal Reserve System, *Economic Well-Being of U.S. Households in 2025*, May 2026: https://www.federalreserve.gov/publications/files/2025-report-economic-well-being-us-households-202605.pdf
[^census-nonemployer]: U.S. Census Bureau, “Telling the Story of the Nation’s Smallest Businesses,” May 6, 2025: https://www.census.gov/library/stories/2025/05/smallest-businesses.html
[^irs-states]: Internal Revenue Service, “State government websites,” updated October 10, 2025: https://www.irs.gov/businesses/small-businesses-self-employed/state-government-websites
[^naic-states]: National Association of Insurance Commissioners, “Insurance Departments”: https://content.naic.org/state-insurance-departments
