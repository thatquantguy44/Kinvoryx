"""Validation harness for the synthetic Spec 011 cash-inflow brief."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from kinvoryx.cash_inflow import (
    AllocationPlan,
    Debt,
    DecisionBrief,
    HouseholdCase,
    PrototypePolicy,
    Strategy,
    ZERO,
    build_decision_brief,
)


VALID_SCENARIO_NAMES = frozenset(
    {"job_loss", "unexpected_expense", "market_decline", "goal_cost_increase"}
)
VALID_ANNOTATION_CATEGORIES = frozenset(
    {"assumption", "risk", "usefulness", "compliance", "calculation"}
)
VALID_ANNOTATION_SEVERITIES = frozenset({"low", "medium", "high", "blocker"})
VALID_ANNOTATION_DISPOSITIONS = frozenset({"open", "accepted", "deferred", "resolved"})
TRACE_PREFIXES = ("REQ-CIB-", "AC-CIB-")


@dataclass(frozen=True)
class MetricExpectation:
    """A fixture-level expectation about which strategies should lead a metric."""

    metric_name: str
    direction: str
    expected_strategies: tuple[str, ...]
    trace_ids: tuple[str, ...] = ("REQ-CIB-012", "AC-CIB-005")

    def __post_init__(self) -> None:
        if self.direction not in {"max", "min"}:
            raise ValueError("metric expectation direction must be max or min")
        if not self.expected_strategies:
            raise ValueError("metric expectation requires at least one expected strategy")


@dataclass(frozen=True)
class ReviewerAnnotation:
    """Structured human review evidence for a synthetic decision brief."""

    annotation_id: str
    case_id: str
    reviewer_role: str
    category: str
    severity: str
    note: str
    trace_ids: tuple[str, ...]
    disposition: str = "open"
    strategy: str | None = None


@dataclass(frozen=True)
class GoldenCaseFixture:
    """A synthetic case plus the behavior Slice B expects to validate."""

    fixture_id: str
    purpose: str
    household: HouseholdCase
    metric_expectations: tuple[MetricExpectation, ...] = ()
    reviewer_annotations: tuple[ReviewerAnnotation, ...] = ()


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    trace_ids: tuple[str, ...]
    case_id: str
    strategy: str | None = None


@dataclass(frozen=True)
class ValidationEvidence:
    """Deterministic validation evidence for one golden fixture."""

    fixture_id: str
    case_id: str
    passed: bool
    pilot_ready: bool
    issues: tuple[ValidationIssue, ...]
    blocker_annotations: tuple[ReviewerAnnotation, ...]
    brief: DecisionBrief


def golden_case_fixtures() -> tuple[GoldenCaseFixture, ...]:
    """Return the canonical synthetic golden-case set for Slice B."""
    return (
        GoldenCaseFixture(
            fixture_id="bonus-full-tradeoff",
            purpose="Bonus with liquidity, debt, match, tax, and goal trade-offs.",
            household=HouseholdCase(
                case_id="golden-bonus-full-tradeoff",
                cash_inflow="20000",
                monthly_essential_expenses="5000",
                liquid_reserves="5000",
                debts=(
                    Debt("credit_card", "6000", "0.24"),
                    Debt("student_loan", "12000", "0.055"),
                ),
                employer_match_contribution_room="6000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="7000",
                estimated_marginal_tax_rate="0.24",
                near_term_goal_remaining="15000",
            ),
            metric_expectations=(
                MetricExpectation("liquidity_months", "max", (Strategy.RESILIENCE.value,)),
                MetricExpectation(
                    "estimated_first_year_interest_avoided",
                    "max",
                    (Strategy.DEBT_ACCELERATION.value,),
                ),
                MetricExpectation(
                    "estimated_tax_value",
                    "max",
                    (Strategy.TAX_ADVANTAGED_FIRST.value,),
                ),
                MetricExpectation(
                    "near_term_goal_funded",
                    "max",
                    (Strategy.NEAR_TERM_GOAL_FIRST.value,),
                ),
            ),
            reviewer_annotations=(
                ReviewerAnnotation(
                    annotation_id="rvw-bonus-001",
                    case_id="golden-bonus-full-tradeoff",
                    strategy=Strategy.TAX_ADVANTAGED_FIRST.value,
                    reviewer_role="product-reviewer",
                    category="usefulness",
                    severity="medium",
                    note="Confirms the brief exposes the liquidity trade-off in the tax-forward path.",
                    trace_ids=("REQ-CIB-014", "AC-CIB-008"),
                    disposition="accepted",
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="no-supported-debt",
            purpose="No supported debt should not break debt metrics or comparisons.",
            household=HouseholdCase(
                case_id="golden-no-supported-debt",
                cash_inflow="5000",
                monthly_essential_expenses="3000",
                liquid_reserves="6000",
                debts=(),
                employer_match_contribution_room="2000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="2000",
                estimated_marginal_tax_rate="0.22",
                near_term_goal_remaining="4000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "estimated_tax_value",
                    "max",
                    (Strategy.TAX_ADVANTAGED_FIRST.value,),
                ),
                MetricExpectation(
                    "near_term_goal_funded",
                    "max",
                    (Strategy.NEAR_TERM_GOAL_FIRST.value,),
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="underfunded-emergency-reserve",
            purpose="A household with no reserve should expose liquidity-first behavior.",
            household=HouseholdCase(
                case_id="golden-underfunded-emergency-reserve",
                cash_inflow="7000",
                monthly_essential_expenses="4000",
                liquid_reserves="0",
                debts=(Debt("credit_card", "2000", "0.22"),),
                employer_match_contribution_room="1000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="0",
                estimated_marginal_tax_rate="0.20",
                near_term_goal_remaining="3000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "liquidity_months",
                    "max",
                    (Strategy.SAFETY_FIRST.value, Strategy.RESILIENCE.value),
                ),
                MetricExpectation(
                    "near_term_goal_funded",
                    "max",
                    (Strategy.NEAR_TERM_GOAL_FIRST.value,),
                ),
            ),
            reviewer_annotations=(
                ReviewerAnnotation(
                    annotation_id="rvw-reserve-001",
                    case_id="golden-underfunded-emergency-reserve",
                    reviewer_role="risk-reviewer",
                    category="risk",
                    severity="high",
                    note="Pilot copy must avoid implying zero-reserve households should choose a single path.",
                    trace_ids=("REQ-CIB-016", "AC-CIB-009"),
                    disposition="resolved",
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="already-funded-reserve",
            purpose="Safety reserve already funded; alternatives should still respect caps.",
            household=HouseholdCase(
                case_id="golden-already-funded-reserve",
                cash_inflow="6000",
                monthly_essential_expenses="2000",
                liquid_reserves="8000",
                debts=(Debt("personal_loan", "5000", "0.18"),),
                employer_match_contribution_room="3000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="4000",
                estimated_marginal_tax_rate="0.24",
                near_term_goal_remaining="6000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "estimated_first_year_interest_avoided",
                    "max",
                    (Strategy.DEBT_ACCELERATION.value,),
                ),
                MetricExpectation("liquidity_months", "max", (Strategy.RESILIENCE.value,)),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="employer-match-capped",
            purpose="Employer match room is small relative to the inflow.",
            household=HouseholdCase(
                case_id="golden-employer-match-capped",
                cash_inflow="12000",
                monthly_essential_expenses="4000",
                liquid_reserves="4000",
                debts=(Debt("auto_loan", "10000", "0.12"),),
                employer_match_contribution_room="500",
                employer_match_rate="1.00",
                tax_advantaged_contribution_room="10000",
                estimated_marginal_tax_rate="0.24",
                near_term_goal_remaining="10000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "estimated_first_year_interest_avoided",
                    "max",
                    (
                        Strategy.MATCH_AND_DEBT_FIRST.value,
                        Strategy.DEBT_ACCELERATION.value,
                    ),
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="tax-room-exhausted",
            purpose="Tax contribution room is unavailable and should remain capped at zero.",
            household=HouseholdCase(
                case_id="golden-tax-room-exhausted",
                cash_inflow="10000",
                monthly_essential_expenses="3000",
                liquid_reserves="6000",
                debts=(Debt("credit_card", "3000", "0.19"),),
                employer_match_contribution_room="3000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="0",
                estimated_marginal_tax_rate="0.24",
                near_term_goal_remaining="8000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "near_term_goal_funded",
                    "max",
                    (Strategy.NEAR_TERM_GOAL_FIRST.value,),
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="goal-larger-than-inflow",
            purpose="Near-term goal need exceeds the full inflow.",
            household=HouseholdCase(
                case_id="golden-goal-larger-than-inflow",
                cash_inflow="8000",
                monthly_essential_expenses="4000",
                liquid_reserves="4000",
                debts=(),
                employer_match_contribution_room="1000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="1000",
                estimated_marginal_tax_rate="0.22",
                near_term_goal_remaining="50000",
            ),
            metric_expectations=(
                MetricExpectation(
                    "near_term_goal_funded",
                    "max",
                    (Strategy.NEAR_TERM_GOAL_FIRST.value,),
                ),
            ),
        ),
        GoldenCaseFixture(
            fixture_id="oversized-inflow",
            purpose="Inflow exceeds all modeled caps and should create retained cash.",
            household=HouseholdCase(
                case_id="golden-oversized-inflow",
                cash_inflow="50000",
                monthly_essential_expenses="3000",
                liquid_reserves="9000",
                debts=(Debt("credit_card", "5000", "0.20"),),
                employer_match_contribution_room="3000",
                employer_match_rate="0.50",
                tax_advantaged_contribution_room="6000",
                estimated_marginal_tax_rate="0.24",
                near_term_goal_remaining="7000",
            ),
        ),
    )


def validate_golden_case(
    fixture: GoldenCaseFixture,
    policy: PrototypePolicy = PrototypePolicy(),
) -> ValidationEvidence:
    """Validate one fixture and return deterministic evidence."""
    brief = build_decision_brief(fixture.household, policy)
    issues = list(_brief_invariant_issues(fixture, brief, policy))
    issues.extend(_metric_expectation_issues(fixture, brief))
    issues.extend(
        validate_reviewer_annotations(
            fixture.reviewer_annotations,
            valid_case_ids=(fixture.household.case_id,),
            valid_strategies=_strategy_ids(brief),
        )
    )
    blockers = unresolved_pilot_blockers(fixture.reviewer_annotations)
    return ValidationEvidence(
        fixture_id=fixture.fixture_id,
        case_id=fixture.household.case_id,
        passed=not issues,
        pilot_ready=not issues and not blockers,
        issues=tuple(issues),
        blocker_annotations=blockers,
        brief=brief,
    )


def validate_all_golden_cases(
    fixtures: Iterable[GoldenCaseFixture] | None = None,
    policy: PrototypePolicy = PrototypePolicy(),
) -> tuple[ValidationEvidence, ...]:
    """Validate the full canonical golden-case suite by default."""
    selected = golden_case_fixtures() if fixtures is None else tuple(fixtures)
    return tuple(validate_golden_case(fixture, policy) for fixture in selected)


def property_sweep_cases() -> tuple[HouseholdCase, ...]:
    """Return deterministic synthetic edge cases for invariant property sweeps."""
    cases: list[HouseholdCase] = []
    inflows = ("100", "2500", "15000", "50000")
    reserve_states = ("0", "5000", "20000")
    debt_profiles = (
        (),
        (Debt("high_cost_card", "3000", "0.24"),),
        (
            Debt("high_cost_card", "3000", "0.24"),
            Debt("lower_rate_loan", "12000", "0.055"),
        ),
    )
    match_rooms = ("0", "2000")
    tax_rooms = ("0", "6000")
    goals = ("0", "12000")

    case_number = 1
    for inflow in inflows:
        for reserves in reserve_states:
            for debts in debt_profiles:
                for match_room in match_rooms:
                    for tax_room in tax_rooms:
                        for goal in goals:
                            cases.append(
                                HouseholdCase(
                                    case_id=f"property-sweep-{case_number:03d}",
                                    cash_inflow=inflow,
                                    monthly_essential_expenses="5000",
                                    liquid_reserves=reserves,
                                    debts=debts,
                                    employer_match_contribution_room=match_room,
                                    employer_match_rate="0.50",
                                    tax_advantaged_contribution_room=tax_room,
                                    estimated_marginal_tax_rate="0.24",
                                    near_term_goal_remaining=goal,
                                )
                            )
                            case_number += 1
    return tuple(cases)


def validate_reviewer_annotations(
    annotations: Iterable[ReviewerAnnotation],
    valid_case_ids: Iterable[str],
    valid_strategies: Iterable[str],
) -> tuple[ValidationIssue, ...]:
    """Validate annotation shape and traceability without changing calculations."""
    case_ids = set(valid_case_ids)
    strategies = set(valid_strategies)
    issues: list[ValidationIssue] = []

    for annotation in annotations:
        trace_ids = annotation.trace_ids or ("REQ-CIB-014", "AC-CIB-008")
        if not annotation.annotation_id:
            issues.append(_annotation_issue("annotation_id", "annotation_id is required", trace_ids, annotation))
        if annotation.case_id not in case_ids:
            issues.append(_annotation_issue("case_id", "annotation case_id is not valid", trace_ids, annotation))
        if annotation.strategy is not None and annotation.strategy not in strategies:
            issues.append(_annotation_issue("strategy", "annotation strategy is not valid", trace_ids, annotation))
        if not annotation.reviewer_role:
            issues.append(_annotation_issue("reviewer_role", "reviewer_role is required", trace_ids, annotation))
        if annotation.category not in VALID_ANNOTATION_CATEGORIES:
            issues.append(_annotation_issue("category", "annotation category is not supported", trace_ids, annotation))
        if annotation.severity not in VALID_ANNOTATION_SEVERITIES:
            issues.append(_annotation_issue("severity", "annotation severity is not supported", trace_ids, annotation))
        if annotation.disposition not in VALID_ANNOTATION_DISPOSITIONS:
            issues.append(_annotation_issue("disposition", "annotation disposition is not supported", trace_ids, annotation))
        if not annotation.note:
            issues.append(_annotation_issue("note", "annotation note is required", trace_ids, annotation))
        if not annotation.trace_ids:
            issues.append(_annotation_issue("trace_ids", "at least one trace ID is required", trace_ids, annotation))
        for trace_id in annotation.trace_ids:
            if not trace_id.startswith(TRACE_PREFIXES):
                issues.append(
                    _annotation_issue(
                        "trace_ids",
                        f"trace ID {trace_id} must reference Spec 011 requirement or acceptance IDs",
                        trace_ids,
                        annotation,
                    )
                )
    return tuple(issues)


def unresolved_pilot_blockers(
    annotations: Iterable[ReviewerAnnotation],
) -> tuple[ReviewerAnnotation, ...]:
    """Return open high-severity annotations that block pilot readiness."""
    return tuple(
        annotation
        for annotation in annotations
        if annotation.disposition == "open" and annotation.severity in {"high", "blocker"}
    )


def _brief_invariant_issues(
    fixture: GoldenCaseFixture,
    brief: DecisionBrief,
    policy: PrototypePolicy,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    household = fixture.household
    plans = (brief.baseline,) + brief.alternatives
    alternative_strategies = {plan.strategy for plan in brief.alternatives}
    expected_strategies = {strategy.value for strategy in Strategy}

    if brief.baseline.strategy != "waterfall_baseline":
        issues.append(
            _issue(
                fixture,
                "missing_baseline",
                "baseline strategy must be waterfall_baseline",
                ("REQ-CIB-002", "AC-CIB-002"),
            )
        )
    if alternative_strategies != expected_strategies:
        issues.append(
            _issue(
                fixture,
                "missing_alternatives",
                "brief must produce all seven required alternatives",
                ("REQ-CIB-002", "AC-CIB-002"),
            )
        )

    for plan in plans:
        issues.extend(_plan_invariant_issues(fixture, plan, policy))

    if not any("Synthetic inputs only" in assumption for assumption in brief.assumptions):
        issues.append(
            _issue(
                fixture,
                "missing_synthetic_label",
                "validation evidence must retain synthetic-only assumption labeling",
                ("REQ-CIB-007", "REQ-CIB-016", "AC-CIB-009"),
            )
        )

    if household.cash_inflow > _total_modeled_capacity(household, policy):
        retained = [plan for plan in plans if plan.allocations["retained_cash"] > ZERO]
        if not retained:
            issues.append(
                _issue(
                    fixture,
                    "missing_retained_cash",
                    "oversized inflow cases must retain cash after modeled caps are exhausted",
                    ("REQ-CIB-003", "REQ-CIB-012", "AC-CIB-006"),
                )
            )
    return tuple(issues)


def _plan_invariant_issues(
    fixture: GoldenCaseFixture,
    plan: AllocationPlan,
    policy: PrototypePolicy,
) -> tuple[ValidationIssue, ...]:
    household = fixture.household
    issues: list[ValidationIssue] = []
    debt_by_id = {debt.identifier: debt for debt in household.debts}

    if plan.allocated_total != household.cash_inflow:
        issues.append(
            _issue(
                fixture,
                "cash_conservation",
                f"{plan.strategy} allocates {plan.allocated_total} instead of {household.cash_inflow}",
                ("REQ-CIB-003", "AC-CIB-003"),
                plan.strategy,
            )
        )

    for category, amount in plan.allocations.items():
        if amount < ZERO:
            issues.append(
                _issue(
                    fixture,
                    "negative_allocation",
                    f"{plan.strategy} has a negative {category} allocation",
                    ("REQ-CIB-003", "AC-CIB-003"),
                    plan.strategy,
                )
            )

    category_caps = {
        "employer_match_contribution": household.employer_match_contribution_room,
        "tax_advantaged_savings": household.tax_advantaged_contribution_room,
        "near_term_goal": household.near_term_goal_remaining,
        "debt_paydown": sum((debt.balance for debt in household.debts), ZERO),
        "emergency_reserve": _reserve_capacity(household, policy.resilience_reserve_months),
    }
    for category, cap in category_caps.items():
        if plan.allocations[category] > cap:
            issues.append(
                _issue(
                    fixture,
                    "category_cap",
                    f"{plan.strategy} allocates {plan.allocations[category]} to {category}, above cap {cap}",
                    ("REQ-CIB-004", "REQ-CIB-012", "AC-CIB-003"),
                    plan.strategy,
                )
            )

    for debt_id, payment in plan.debt_payments.items():
        if debt_id not in debt_by_id:
            issues.append(
                _issue(
                    fixture,
                    "unknown_debt",
                    f"{plan.strategy} pays unknown debt {debt_id}",
                    ("REQ-CIB-004", "AC-CIB-003"),
                    plan.strategy,
                )
            )
            continue
        if payment > debt_by_id[debt_id].balance:
            issues.append(
                _issue(
                    fixture,
                    "debt_cap",
                    f"{plan.strategy} pays {payment} to {debt_id}, above balance {debt_by_id[debt_id].balance}",
                    ("REQ-CIB-004", "REQ-CIB-012", "AC-CIB-003"),
                    plan.strategy,
                )
            )
    if sum(plan.debt_payments.values(), ZERO) != plan.allocations["debt_paydown"]:
        issues.append(
            _issue(
                fixture,
                "debt_reconciliation",
                f"{plan.strategy} debt payments do not reconcile to debt_paydown",
                ("REQ-CIB-003", "REQ-CIB-004", "AC-CIB-003"),
                plan.strategy,
            )
        )

    if {scenario.name for scenario in plan.scenarios} != VALID_SCENARIO_NAMES:
        issues.append(
            _issue(
                fixture,
                "scenario_coverage",
                f"{plan.strategy} does not include the required scenario set",
                ("REQ-CIB-006", "REQ-CIB-012", "AC-CIB-004"),
                plan.strategy,
            )
        )
    if not plan.tradeoffs:
        issues.append(
            _issue(
                fixture,
                "missing_tradeoffs",
                f"{plan.strategy} must include at least one trade-off statement",
                ("REQ-CIB-005", "AC-CIB-004"),
                plan.strategy,
            )
        )
    return tuple(issues)


def _metric_expectation_issues(
    fixture: GoldenCaseFixture,
    brief: DecisionBrief,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    plans = brief.alternatives
    for expectation in fixture.metric_expectations:
        values = {plan.strategy: _metric_value(plan, expectation.metric_name) for plan in plans}
        target_value = (
            max(values.values()) if expectation.direction == "max" else min(values.values())
        )
        leaders = {strategy for strategy, value in values.items() if value == target_value}
        missing = set(expectation.expected_strategies) - leaders
        if missing:
            issues.append(
                _issue(
                    fixture,
                    "metric_expectation",
                    (
                        f"{expectation.metric_name} expected leaders {sorted(expectation.expected_strategies)} "
                        f"but observed leaders {sorted(leaders)}"
                    ),
                    expectation.trace_ids,
                )
            )
    return tuple(issues)


def _metric_value(plan: AllocationPlan, metric_name: str) -> Decimal:
    value = getattr(plan.metrics, metric_name, None)
    if value is None:
        raise ValueError(f"unsupported metric expectation: {metric_name}")
    return value


def _strategy_ids(brief: DecisionBrief) -> tuple[str, ...]:
    return tuple(plan.strategy for plan in (brief.baseline,) + brief.alternatives)


def _reserve_capacity(household: HouseholdCase, target_months: Decimal) -> Decimal:
    target = household.monthly_essential_expenses * target_months
    return max(ZERO, target - household.liquid_reserves)


def _total_modeled_capacity(household: HouseholdCase, policy: PrototypePolicy) -> Decimal:
    return sum(
        (
            _reserve_capacity(household, policy.resilience_reserve_months),
            household.employer_match_contribution_room,
            sum((debt.balance for debt in household.debts), ZERO),
            household.tax_advantaged_contribution_room,
            household.near_term_goal_remaining,
        ),
        ZERO,
    )


def _issue(
    fixture: GoldenCaseFixture,
    code: str,
    message: str,
    trace_ids: tuple[str, ...],
    strategy: str | None = None,
) -> ValidationIssue:
    return ValidationIssue(code, message, trace_ids, fixture.household.case_id, strategy)


def _annotation_issue(
    field: str,
    message: str,
    trace_ids: tuple[str, ...],
    annotation: ReviewerAnnotation,
) -> ValidationIssue:
    code = field if field.startswith("annotation_") else f"annotation_{field}"
    return ValidationIssue(
        code=code,
        message=message,
        trace_ids=trace_ids,
        case_id=annotation.case_id,
        strategy=annotation.strategy,
    )
