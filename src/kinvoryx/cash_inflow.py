"""Synthetic-only cash-inflow alternative generation for Spec 011."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Iterable


CENT = Decimal("0.01")
ZERO = Decimal("0")


def _money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def _rate(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value))


def _non_negative(name: str, value: Decimal) -> None:
    if value < ZERO:
        raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True)
class Debt:
    """A supported debt balance used only for transparent scenario comparison."""

    identifier: str
    balance: Decimal | int | float | str
    annual_interest_rate: Decimal | int | float | str

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("debt identifier is required")
        object.__setattr__(self, "balance", _money(self.balance))
        object.__setattr__(self, "annual_interest_rate", _rate(self.annual_interest_rate))
        _non_negative("debt balance", self.balance)
        _non_negative("annual interest rate", self.annual_interest_rate)


@dataclass(frozen=True)
class HouseholdCase:
    """The minimum synthetic-case contract for a cash-inflow decision brief."""

    case_id: str
    cash_inflow: Decimal | int | float | str
    monthly_essential_expenses: Decimal | int | float | str
    liquid_reserves: Decimal | int | float | str
    debts: tuple[Debt, ...]
    employer_match_contribution_room: Decimal | int | float | str
    employer_match_rate: Decimal | int | float | str
    tax_advantaged_contribution_room: Decimal | int | float | str
    estimated_marginal_tax_rate: Decimal | int | float | str
    near_term_goal_remaining: Decimal | int | float | str
    synthetic: bool = True

    def __post_init__(self) -> None:
        if not self.case_id:
            raise ValueError("case_id is required")
        for field_name in (
            "cash_inflow",
            "monthly_essential_expenses",
            "liquid_reserves",
            "employer_match_contribution_room",
            "tax_advantaged_contribution_room",
            "near_term_goal_remaining",
        ):
            value = _money(getattr(self, field_name))
            object.__setattr__(self, field_name, value)
            _non_negative(field_name, value)
        for field_name in ("employer_match_rate", "estimated_marginal_tax_rate"):
            value = _rate(getattr(self, field_name))
            object.__setattr__(self, field_name, value)
            _non_negative(field_name, value)
        if self.monthly_essential_expenses <= ZERO:
            raise ValueError("monthly_essential_expenses must be greater than zero")


class Strategy(str, Enum):
    SAFETY_FIRST = "safety_first"
    MATCH_AND_DEBT_FIRST = "match_and_debt_first"
    TAX_ADVANTAGED_FIRST = "tax_advantaged_first"
    NEAR_TERM_GOAL_FIRST = "near_term_goal_first"
    BALANCED = "balanced"
    RESILIENCE = "resilience"
    DEBT_ACCELERATION = "debt_acceleration"


@dataclass(frozen=True)
class ScenarioImpact:
    name: str
    summary: str


@dataclass(frozen=True)
class PlanMetrics:
    liquidity_months: Decimal
    estimated_first_year_interest_avoided: Decimal
    estimated_employer_match_captured: Decimal
    estimated_tax_value: Decimal
    near_term_goal_funded: Decimal
    supported_debt_remaining: Decimal


@dataclass(frozen=True)
class AllocationPlan:
    strategy: str
    label: str
    allocations: dict[str, Decimal]
    debt_payments: dict[str, Decimal]
    metrics: PlanMetrics
    tradeoffs: tuple[str, ...]
    scenarios: tuple[ScenarioImpact, ...]

    @property
    def allocated_total(self) -> Decimal:
        return sum(self.allocations.values(), ZERO).quantize(CENT)


@dataclass(frozen=True)
class DecisionBrief:
    case_id: str
    baseline: AllocationPlan
    alternatives: tuple[AllocationPlan, ...]
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class PrototypePolicy:
    safety_reserve_months: Decimal = Decimal("3")
    resilience_reserve_months: Decimal = Decimal("6")
    goal_first_minimum_reserve_months: Decimal = Decimal("1")
    high_cost_debt_rate: Decimal = Decimal("0.07")
    job_loss_months: Decimal = Decimal("3")
    market_decline_rate: Decimal = Decimal("0.20")
    goal_cost_increase_rate: Decimal = Decimal("0.10")


_CATEGORY_NAMES = (
    "emergency_reserve",
    "employer_match_contribution",
    "debt_paydown",
    "tax_advantaged_savings",
    "near_term_goal",
    "retained_cash",
)


def build_decision_brief(
    household: HouseholdCase,
    policy: PrototypePolicy = PrototypePolicy(),
) -> DecisionBrief:
    """Build comparable deterministic alternatives from a synthetic household case."""
    if not household.synthetic:
        raise ValueError("Spec 011 prototype accepts synthetic cases only")

    baseline = _build_ordered_plan(
        household,
        strategy="waterfall_baseline",
        label="Transparent waterfall baseline",
        order=("reserve", "match", "high_cost_debt", "tax", "goal"),
        reserve_target_months=policy.safety_reserve_months,
        policy=policy,
    )
    alternatives = (
        _build_ordered_plan(
            household,
            Strategy.SAFETY_FIRST,
            "Safety first",
            ("reserve", "match", "high_cost_debt", "tax", "goal"),
            policy.safety_reserve_months,
            policy,
        ),
        _build_ordered_plan(
            household,
            Strategy.MATCH_AND_DEBT_FIRST,
            "Match and debt first",
            ("match", "high_cost_debt", "reserve", "tax", "goal"),
            policy.safety_reserve_months,
            policy,
        ),
        _build_ordered_plan(
            household,
            Strategy.TAX_ADVANTAGED_FIRST,
            "Tax-advantaged first",
            ("match", "tax", "reserve", "high_cost_debt", "goal"),
            policy.safety_reserve_months,
            policy,
        ),
        _build_ordered_plan(
            household,
            Strategy.NEAR_TERM_GOAL_FIRST,
            "Near-term goal first",
            ("goal", "reserve", "match", "high_cost_debt", "tax"),
            policy.goal_first_minimum_reserve_months,
            policy,
        ),
        _build_balanced_plan(household, policy),
        _build_ordered_plan(
            household,
            Strategy.RESILIENCE,
            "Resilience",
            ("reserve", "match", "high_cost_debt", "tax", "goal"),
            policy.resilience_reserve_months,
            policy,
        ),
        _build_ordered_plan(
            household,
            Strategy.DEBT_ACCELERATION,
            "Debt acceleration",
            ("all_debt", "match", "reserve", "tax", "goal"),
            policy.goal_first_minimum_reserve_months,
            policy,
        ),
    )
    return DecisionBrief(
        case_id=household.case_id,
        baseline=baseline,
        alternatives=alternatives,
        assumptions=_policy_assumptions(policy),
    )


def _build_ordered_plan(
    household: HouseholdCase,
    strategy: Strategy | str,
    label: str,
    order: Iterable[str],
    reserve_target_months: Decimal,
    policy: PrototypePolicy,
) -> AllocationPlan:
    allocations = _empty_allocations()
    debt_payments: dict[str, Decimal] = {}
    remaining = household.cash_inflow
    for action in order:
        remaining = _allocate_action(
            action,
            remaining,
            household,
            allocations,
            debt_payments,
            reserve_target_months,
            policy,
        )
    allocations["retained_cash"] = remaining
    return _finalize_plan(household, strategy, label, allocations, debt_payments, policy)


def _build_balanced_plan(household: HouseholdCase, policy: PrototypePolicy) -> AllocationPlan:
    allocations = _empty_allocations()
    debt_payments: dict[str, Decimal] = {}
    remaining = household.cash_inflow
    actions = ("reserve", "match", "high_cost_debt", "tax", "goal")
    capacities = {
        "reserve": _reserve_capacity(household, policy.safety_reserve_months),
        "match": household.employer_match_contribution_room,
        "high_cost_debt": _debt_capacity(household, policy, high_cost_only=True),
        "tax": household.tax_advantaged_contribution_room,
        "goal": household.near_term_goal_remaining,
    }

    while remaining > ZERO:
        active = [action for action in actions if capacities[action] > ZERO]
        if not active:
            break
        share = (remaining / len(active)).quantize(CENT, rounding=ROUND_HALF_UP)
        if share <= ZERO:
            share = remaining
        progress = ZERO
        for action in active:
            amount = min(share, capacities[action], remaining)
            if amount <= ZERO:
                continue
            before = remaining
            remaining = _allocate_action(
                action,
                remaining,
                household,
                allocations,
                debt_payments,
                policy.safety_reserve_months,
                policy,
                limit=amount,
            )
            applied = before - remaining
            capacities[action] -= applied
            progress += applied
        if progress <= ZERO:
            break
    allocations["retained_cash"] = remaining
    return _finalize_plan(
        household,
        Strategy.BALANCED,
        "Balanced allocation",
        allocations,
        debt_payments,
        policy,
    )


def _allocate_action(
    action: str,
    remaining: Decimal,
    household: HouseholdCase,
    allocations: dict[str, Decimal],
    debt_payments: dict[str, Decimal],
    reserve_target_months: Decimal,
    policy: PrototypePolicy,
    limit: Decimal | None = None,
) -> Decimal:
    available = min(remaining, limit) if limit is not None else remaining
    if available <= ZERO:
        return remaining

    if action == "reserve":
        amount = min(available, _reserve_capacity(household, reserve_target_months))
        allocations["emergency_reserve"] += amount
    elif action == "match":
        amount = min(available, household.employer_match_contribution_room)
        allocations["employer_match_contribution"] += amount
    elif action == "tax":
        amount = min(available, household.tax_advantaged_contribution_room)
        allocations["tax_advantaged_savings"] += amount
    elif action == "goal":
        amount = min(available, household.near_term_goal_remaining)
        allocations["near_term_goal"] += amount
    elif action in {"high_cost_debt", "all_debt"}:
        amount, payments = _pay_debts(
            household,
            available,
            policy,
            high_cost_only=action == "high_cost_debt",
        )
        allocations["debt_paydown"] += amount
        for identifier, payment in payments.items():
            debt_payments[identifier] = debt_payments.get(identifier, ZERO) + payment
    else:
        raise ValueError(f"unsupported allocation action: {action}")
    return (remaining - amount).quantize(CENT)


def _pay_debts(
    household: HouseholdCase,
    available: Decimal,
    policy: PrototypePolicy,
    high_cost_only: bool,
) -> tuple[Decimal, dict[str, Decimal]]:
    remaining = available
    payments: dict[str, Decimal] = {}
    debts = sorted(household.debts, key=lambda debt: debt.annual_interest_rate, reverse=True)
    for debt in debts:
        if high_cost_only and debt.annual_interest_rate < policy.high_cost_debt_rate:
            continue
        payment = min(remaining, debt.balance)
        if payment > ZERO:
            payments[debt.identifier] = payment
            remaining -= payment
        if remaining <= ZERO:
            break
    return (available - remaining).quantize(CENT), payments


def _finalize_plan(
    household: HouseholdCase,
    strategy: Strategy | str,
    label: str,
    allocations: dict[str, Decimal],
    debt_payments: dict[str, Decimal],
    policy: PrototypePolicy,
) -> AllocationPlan:
    for category in allocations:
        allocations[category] = allocations[category].quantize(CENT)
    metrics = _metrics(household, allocations, debt_payments)
    return AllocationPlan(
        strategy=strategy.value if isinstance(strategy, Strategy) else strategy,
        label=label,
        allocations=dict(allocations),
        debt_payments=dict(debt_payments),
        metrics=metrics,
        tradeoffs=_tradeoffs(strategy, household, allocations, metrics, policy),
        scenarios=_scenarios(household, allocations, metrics, policy),
    )


def _metrics(
    household: HouseholdCase,
    allocations: dict[str, Decimal],
    debt_payments: dict[str, Decimal],
) -> PlanMetrics:
    cash_after = household.liquid_reserves + allocations["emergency_reserve"] + allocations["retained_cash"]
    liquidity_months = (cash_after / household.monthly_essential_expenses).quantize(CENT)
    debt_by_id = {debt.identifier: debt for debt in household.debts}
    interest_avoided = sum(
        (
            payment * debt_by_id[identifier].annual_interest_rate
            for identifier, payment in debt_payments.items()
        ),
        ZERO,
    ).quantize(CENT)
    debt_remaining = sum(
        (debt.balance - debt_payments.get(debt.identifier, ZERO) for debt in household.debts),
        ZERO,
    ).quantize(CENT)
    return PlanMetrics(
        liquidity_months=liquidity_months,
        estimated_first_year_interest_avoided=interest_avoided,
        estimated_employer_match_captured=(
            allocations["employer_match_contribution"] * household.employer_match_rate
        ).quantize(CENT),
        estimated_tax_value=(
            allocations["tax_advantaged_savings"] * household.estimated_marginal_tax_rate
        ).quantize(CENT),
        near_term_goal_funded=allocations["near_term_goal"],
        supported_debt_remaining=debt_remaining,
    )


def _tradeoffs(
    strategy: Strategy | str,
    household: HouseholdCase,
    allocations: dict[str, Decimal],
    metrics: PlanMetrics,
    policy: PrototypePolicy,
) -> tuple[str, ...]:
    reserve_gap = max(
        ZERO,
        policy.safety_reserve_months - metrics.liquidity_months,
    ).quantize(CENT)
    common = (
        f"Liquidity after allocation: {metrics.liquidity_months} months of essential expenses.",
        f"Near-term goal funding deferred: ${household.near_term_goal_remaining - allocations['near_term_goal']:.2f}.",
    )
    strategy_key = strategy.value if isinstance(strategy, Strategy) else strategy
    specific = {
        Strategy.SAFETY_FIRST.value: "Prioritizes accessible cash before debt, tax, and goal acceleration.",
        Strategy.MATCH_AND_DEBT_FIRST.value: "Prioritizes employer match and high-cost debt before full liquidity.",
        Strategy.TAX_ADVANTAGED_FIRST.value: "Prioritizes contribution room and estimated tax value, reducing flexibility.",
        Strategy.NEAR_TERM_GOAL_FIRST.value: "Prioritizes the stated goal date while leaving other financial capacity deferred.",
        Strategy.BALANCED.value: "Makes partial progress across categories without maximizing any single outcome.",
        Strategy.RESILIENCE.value: "Targets a larger cash buffer and accepts slower debt, tax, and goal progress.",
        Strategy.DEBT_ACCELERATION.value: "Reduces supported debt quickly and may leave less cash for a surprise expense.",
        "waterfall_baseline": "Uses a transparent reference order rather than a personalized optimization objective.",
    }[strategy_key]
    gap_note = (
        f"Reserve remains {reserve_gap} months below the {policy.safety_reserve_months}-month safety target."
        if reserve_gap > ZERO
        else "Meets the configured three-month safety reserve target."
    )
    return common + (specific, gap_note)


def _scenarios(
    household: HouseholdCase,
    allocations: dict[str, Decimal],
    metrics: PlanMetrics,
    policy: PrototypePolicy,
) -> tuple[ScenarioImpact, ...]:
    reserve_after = household.liquid_reserves + allocations["emergency_reserve"] + allocations["retained_cash"]
    job_loss_shortfall = max(ZERO, policy.job_loss_months - metrics.liquidity_months).quantize(CENT)
    surprise_cash_after = max(ZERO, reserve_after - household.monthly_essential_expenses)
    surprise_months = (surprise_cash_after / household.monthly_essential_expenses).quantize(CENT)
    market_decline = (allocations["tax_advantaged_savings"] * policy.market_decline_rate).quantize(CENT)
    goal_remaining_after_stress = max(
        ZERO,
        household.near_term_goal_remaining * (ONE + policy.goal_cost_increase_rate) - allocations["near_term_goal"],
    ).quantize(CENT)
    return (
        ScenarioImpact(
            "job_loss",
            f"A {policy.job_loss_months}-month income interruption leaves a {job_loss_shortfall}-month reserve gap.",
        ),
        ScenarioImpact(
            "unexpected_expense",
            f"After one month of essential expenses, liquid reserve coverage is {surprise_months} months.",
        ),
        ScenarioImpact(
            "market_decline",
            f"A {policy.market_decline_rate:.0%} decline applied to long-term contribution exposure is ${market_decline:.2f}.",
        ),
        ScenarioImpact(
            "goal_cost_increase",
            f"A {policy.goal_cost_increase_rate:.0%} goal-cost increase leaves ${goal_remaining_after_stress:.2f} still to fund.",
        ),
    )


def _reserve_capacity(household: HouseholdCase, target_months: Decimal) -> Decimal:
    target = household.monthly_essential_expenses * target_months
    return max(ZERO, target - household.liquid_reserves).quantize(CENT)


def _debt_capacity(household: HouseholdCase, policy: PrototypePolicy, high_cost_only: bool) -> Decimal:
    return sum(
        (
            debt.balance
            for debt in household.debts
            if not high_cost_only or debt.annual_interest_rate >= policy.high_cost_debt_rate
        ),
        ZERO,
    ).quantize(CENT)


def _empty_allocations() -> dict[str, Decimal]:
    return {category: ZERO for category in _CATEGORY_NAMES}


def _policy_assumptions(policy: PrototypePolicy) -> tuple[str, ...]:
    return (
        "Synthetic inputs only; output is deterministic decision support, not personalized advice.",
        f"Safety reserve target: {policy.safety_reserve_months} months of essential expenses.",
        f"Resilience reserve target: {policy.resilience_reserve_months} months of essential expenses.",
        f"High-cost debt threshold: {policy.high_cost_debt_rate:.0%} annual interest.",
        f"Market-decline stress: {policy.market_decline_rate:.0%} of long-term contribution exposure.",
        f"Goal-cost stress: {policy.goal_cost_increase_rate:.0%} increase in goal cost.",
    )


ONE = Decimal("1")
