"""Capital Allocation Optimizer — Spec 004.

Synthetic-only. Given a validated HouseholdState and JurisdictionRules,
produces:
  - A rules-based waterfall baseline (REQ-020)
  - Three feasible alternatives: recommended, liquidity-preserving,
    goal-acceleration (REQ-023)
  - Four deterministic scenario stresses on each alternative (REQ-030, REQ-031)
  - Binding constraints and opportunity costs (REQ-041, REQ-042)
  - Infeasibility diagnosis when obligations exceed income (REQ-024)

Multi-period optimization (REQ-022) is deferred to a later phase.
All outputs reconcile sources and uses of funds (REQ-025).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Optional

from kinvoryx.household_state import (
    AccountType,
    ExpenseCategory,
    GoalPriority,
    HouseholdState,
)
from kinvoryx.jurisdiction_rules import JurisdictionRules


CENT = Decimal("0.01")
ZERO = Decimal("0")

HIGH_COST_THRESHOLD = Decimal("0.07")    # 7% APR
ASSUMED_EQUITY_RETURN = Decimal("0.06")  # 6% nominal long-run planning assumption
INCOME_LOSS_FRACTION = Decimal("0.50")
INCOME_LOSS_MONTHS = Decimal("3")
UNEXPECTED_EXPENSE = Decimal("15000")
MARKET_DECLINE_RATE = Decimal("0.30")
GOAL_COST_INCREASE = Decimal("0.20")


def _money(v: Decimal | int | str) -> Decimal:
    return Decimal(str(v)).quantize(CENT, rounding=ROUND_HALF_UP)


# --------------------------------------------------------------------------- #
# Public output types                                                          #
# --------------------------------------------------------------------------- #


class AllocationUse(str, Enum):
    EMERGENCY_RESERVE = "emergency_reserve"
    EMPLOYER_MATCH = "employer_match"
    HIGH_COST_DEBT = "high_cost_debt"
    TAX_ADVANTAGED_SAVINGS = "tax_advantaged_savings"
    GOAL_FUNDING = "goal_funding"
    LOWER_COST_DEBT = "lower_cost_debt"
    DISCRETIONARY_BUFFER = "discretionary_buffer"


@dataclass(frozen=True)
class AllocationLine:
    """One use of surplus funds (REQ-040)."""

    use: AllocationUse
    amount: Decimal
    destination_id: Optional[str]    # debt_id, goal_id, or None
    destination_label: str
    rationale: str


@dataclass(frozen=True)
class BindingConstraint:
    """A capacity limit that was fully consumed (REQ-041)."""

    dimension: str
    limit: Decimal
    applied: Decimal
    marginal_value: Optional[Decimal]    # estimated benefit per $1 if relaxed


@dataclass(frozen=True)
class OpportunityCost:
    """Benefit foregone by this allocation path (REQ-042)."""

    foregone_use: str
    foregone_amount: Decimal
    description: str


@dataclass(frozen=True)
class ScenarioResult:
    """Outcome under one deterministic stress (REQ-030, REQ-031)."""

    scenario: str
    income_reduction: Decimal
    expense_increase: Decimal
    reserve_months_remaining: Optional[Decimal]
    plan_survives: bool
    notes: str


@dataclass(frozen=True)
class AllocationAlternative:
    """One feasible allocation path (REQ-023, REQ-025, REQ-040)."""

    name: str
    label: str
    lines: tuple[AllocationLine, ...]
    total_allocated: Decimal           # Invariant: == annual_surplus
    binding_constraints: tuple[BindingConstraint, ...]
    opportunity_costs: tuple[OpportunityCost, ...]
    assumptions: tuple[str, ...]
    scenario_results: tuple[ScenarioResult, ...]
    trade_off_summary: str


@dataclass(frozen=True)
class InfeasibilityReport:
    """Minimum conflicting constraint set when obligations exceed income (REQ-024)."""

    conflicting_constraints: tuple[str, ...]
    diagnosis: str
    minimum_required_annual: Decimal
    actual_annual_gross: Decimal
    shortfall: Decimal


@dataclass(frozen=True)
class OptimizerResult:
    """Full optimizer output for one household, one 12-month horizon (REQ-044)."""

    household_id: str
    household_fingerprint: str
    annual_gross_income: Decimal
    annual_fixed_obligations: Decimal    # expenses + debt minimums
    annual_surplus: Decimal              # gross - fixed_obligations
    baseline: AllocationAlternative
    alternatives: tuple[AllocationAlternative, ...]
    infeasibility: Optional[InfeasibilityReport]
    jurisdiction_scope: str
    period_label: str
    common_assumptions: tuple[str, ...]


# --------------------------------------------------------------------------- #
# Internal capacity derivation                                                 #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class _DebtRow:
    debt_id: str
    label: str
    balance: Decimal
    annual_rate: Decimal
    prepayment_penalty: bool


@dataclass(frozen=True)
class _GoalRow:
    goal_id: str
    label: str
    target: Decimal
    priority: GoalPriority


@dataclass(frozen=True)
class _Capacity:
    annual_gross: Decimal
    annual_fixed: Decimal
    annual_surplus: Decimal
    monthly_essential: Decimal
    current_liquid: Decimal
    reserve_gap_2mo: Decimal
    reserve_gap_3mo: Decimal
    reserve_gap_6mo: Decimal
    employer_match_room: Decimal
    tax_advantaged_room: Decimal
    high_cost_debts: tuple[_DebtRow, ...]    # rate >= threshold, no prepay penalty, sorted desc
    lower_cost_debts: tuple[_DebtRow, ...]   # rate < threshold or has penalty, sorted desc
    goals: tuple[_GoalRow, ...]              # sorted by priority
    marginal_tax_rate: Decimal
    infeasible: bool
    infeasibility_report: Optional[InfeasibilityReport]


def _reserve_gap(monthly_essential: Decimal, months: int, current_liquid: Decimal) -> Decimal:
    return max(ZERO, _money(monthly_essential * months) - current_liquid)


def _compute_capacity(household: HouseholdState, rules: JurisdictionRules) -> _Capacity:
    # Annual gross income
    annual_gross = sum(
        (inc.annual_gross.value for inc in household.income_sources
         if inc.annual_gross.is_usable() and inc.annual_gross.value is not None),
        ZERO,
    )

    # Annual expenses (all categories × 12) and essential subset
    monthly_essential = ZERO
    annual_expenses = ZERO
    for exp in household.expenses:
        if exp.monthly_amount.is_usable() and exp.monthly_amount.value is not None:
            annual_expenses += exp.monthly_amount.value * 12
            if exp.category == ExpenseCategory.ESSENTIAL:
                monthly_essential += exp.monthly_amount.value

    # Annual debt minimums
    annual_minimums = sum(
        (debt.monthly_minimum.value * 12 for debt in household.debts
         if debt.monthly_minimum.is_usable() and debt.monthly_minimum.value is not None),
        ZERO,
    )

    annual_fixed = _money(annual_expenses + annual_minimums)
    raw_surplus = annual_gross - annual_fixed

    infeasibility: Optional[InfeasibilityReport] = None
    infeasible = raw_surplus < ZERO
    if infeasible:
        shortfall = _money(-raw_surplus)
        infeasibility = InfeasibilityReport(
            conflicting_constraints=(
                "minimum_annual_expenses",
                "minimum_annual_debt_service",
                "annual_gross_income",
            ),
            diagnosis=(
                f"Minimum annual obligations (${_money(annual_fixed):,.0f}) exceed "
                f"gross income (${_money(annual_gross):,.0f}). "
                f"Reduce fixed obligations or increase income by "
                f"${shortfall:,.0f}/year before any surplus allocation is possible."
            ),
            minimum_required_annual=_money(annual_fixed),
            actual_annual_gross=_money(annual_gross),
            shortfall=shortfall,
        )

    # Liquid reserves (CASH accounts only)
    current_liquid = sum(
        (acct.balance.value for acct in household.accounts
         if acct.account_type == AccountType.CASH
         and acct.balance.is_usable()
         and acct.balance.value is not None),
        ZERO,
    )
    current_liquid = _money(current_liquid)
    monthly_essential = _money(monthly_essential)

    # Employer match room: sum match tiers across all benefits
    employer_match_room = ZERO
    for ben in household.benefits:
        member_income = sum(
            (inc.annual_gross.value for inc in household.income_sources
             if inc.member_id == ben.member_id
             and inc.annual_gross.is_usable()
             and inc.annual_gross.value is not None),
            ZERO,
        )
        for tier in ben.match_tiers:
            employer_match_room += _money(
                member_income * tier.up_to_percent_of_salary * tier.match_rate
            )

    # Tax-advantaged room: 401k employee limit per benefit + IRA per member
    tax_room = sum(
        (min(ben.annual_employee_limit.value, rules.contribution_limits.k401_employee)
         for ben in household.benefits
         if ben.annual_employee_limit.is_usable()
         and ben.annual_employee_limit.value is not None),
        ZERO,
    )
    tax_room += rules.contribution_limits.ira * len(household.members)
    tax_room = _money(tax_room)

    # Debt rows: categorize and sort by rate descending
    all_debts: list[_DebtRow] = []
    for debt in household.debts:
        bal = (debt.balance.value or ZERO) if debt.balance.is_usable() else ZERO
        rate = (debt.annual_rate.value or ZERO) if debt.annual_rate.is_usable() else ZERO
        all_debts.append(_DebtRow(
            debt_id=debt.debt_id,
            label=debt.label,
            balance=_money(bal),
            annual_rate=rate,
            prepayment_penalty=debt.prepayment_penalty,
        ))
    all_debts.sort(key=lambda d: d.annual_rate, reverse=True)
    high_cost = tuple(d for d in all_debts if d.annual_rate >= HIGH_COST_THRESHOLD and not d.prepayment_penalty)
    lower_cost = tuple(d for d in all_debts if d.annual_rate < HIGH_COST_THRESHOLD or d.prepayment_penalty)

    # Goal rows sorted by priority
    priority_order = {
        GoalPriority.CRITICAL: 0,
        GoalPriority.HIGH: 1,
        GoalPriority.MEDIUM: 2,
        GoalPriority.LOW: 3,
    }
    goal_rows: list[_GoalRow] = []
    for goal in household.goals:
        target = (goal.target_amount.value or ZERO) if goal.target_amount.is_usable() else ZERO
        goal_rows.append(_GoalRow(
            goal_id=goal.goal_id,
            label=goal.label,
            target=_money(target),
            priority=goal.priority,
        ))
    goal_rows.sort(key=lambda g: priority_order[g.priority])

    marginal_rate = rules.marginal_rate(
        _money(annual_gross), household.tax_profile.filing_status
    )

    return _Capacity(
        annual_gross=_money(annual_gross),
        annual_fixed=annual_fixed,
        annual_surplus=_money(max(ZERO, raw_surplus)),
        monthly_essential=monthly_essential,
        current_liquid=current_liquid,
        reserve_gap_2mo=_reserve_gap(monthly_essential, 2, current_liquid),
        reserve_gap_3mo=_reserve_gap(monthly_essential, 3, current_liquid),
        reserve_gap_6mo=_reserve_gap(monthly_essential, 6, current_liquid),
        employer_match_room=_money(employer_match_room),
        tax_advantaged_room=tax_room,
        high_cost_debts=high_cost,
        lower_cost_debts=lower_cost,
        goals=tuple(goal_rows),
        marginal_tax_rate=marginal_rate,
        infeasible=infeasible,
        infeasibility_report=infeasibility,
    )


# --------------------------------------------------------------------------- #
# Greedy allocator                                                             #
# --------------------------------------------------------------------------- #

# Each use spec: (AllocationUse, destination_label, rationale, capacity, destination_id)
_UseSpec = tuple[AllocationUse, str, str, Decimal, Optional[str]]


def _greedy(surplus: Decimal, specs: list[_UseSpec]) -> tuple[list[AllocationLine], Decimal]:
    """
    Fill each use in order up to its capacity or remaining surplus.
    Returns (lines, remaining). remaining + sum(line.amount) == surplus.
    """
    lines: list[AllocationLine] = []
    remaining = surplus
    for use, label, rationale, capacity, dest_id in specs:
        if remaining <= ZERO:
            break
        amount = min(remaining, capacity)
        if amount > ZERO:
            lines.append(AllocationLine(
                use=use,
                amount=amount,
                destination_id=dest_id,
                destination_label=label,
                rationale=rationale,
            ))
            remaining -= amount
    return lines, remaining


def _buffer_line(remaining: Decimal, label: str, rationale: str) -> AllocationLine:
    return AllocationLine(
        use=AllocationUse.DISCRETIONARY_BUFFER,
        amount=remaining,
        destination_id=None,
        destination_label=label,
        rationale=rationale,
    )


# --------------------------------------------------------------------------- #
# Scenario stresses (REQ-030, REQ-031)                                        #
# --------------------------------------------------------------------------- #


def _apply_scenarios(cap: _Capacity, reserve_allocated: Decimal) -> tuple[ScenarioResult, ...]:
    reserve_after = cap.current_liquid + reserve_allocated

    def months_left(liquid: Decimal) -> Optional[Decimal]:
        if cap.monthly_essential <= ZERO:
            return None
        return _money(liquid / cap.monthly_essential)

    # 1. Income loss: 3 months at 50% income
    income_loss = _money(cap.annual_gross * INCOME_LOSS_FRACTION * (INCOME_LOSS_MONTHS / 12))
    post_loss = reserve_after - income_loss
    s1 = ScenarioResult(
        scenario="income_loss_3mo_50pct",
        income_reduction=income_loss,
        expense_increase=ZERO,
        reserve_months_remaining=months_left(max(ZERO, post_loss)),
        plan_survives=post_loss >= ZERO,
        notes=(
            f"3 months at 50% income reduces reserves by ${income_loss:,.0f}. "
            + ("Reserves remain positive." if post_loss >= ZERO
               else f"Reserve shortfall of ${-post_loss:,.0f} requires drawing on other assets.")
        ),
    )

    # 2. Unexpected $15,000 expense
    post_expense = reserve_after - UNEXPECTED_EXPENSE
    s2 = ScenarioResult(
        scenario="unexpected_expense_15k",
        income_reduction=ZERO,
        expense_increase=UNEXPECTED_EXPENSE,
        reserve_months_remaining=months_left(max(ZERO, post_expense)),
        plan_survives=post_expense >= ZERO,
        notes=(
            f"${UNEXPECTED_EXPENSE:,.0f} unexpected expense against reserves. "
            + ("Reserves remain positive." if post_expense >= ZERO
               else f"Reserve shortfall of ${-post_expense:,.0f}.")
        ),
    )

    # 3. 30% market decline — affects investment balances, not year-1 cash plan
    s3 = ScenarioResult(
        scenario="market_decline_30pct",
        income_reduction=ZERO,
        expense_increase=ZERO,
        reserve_months_remaining=months_left(reserve_after),
        plan_survives=True,
        notes=(
            "A 30% equity decline reduces investment account balances but does not "
            "affect the year-1 cash allocation plan. Goal attainment timelines "
            "lengthen if existing balances are impacted."
        ),
    )

    # 4. Goal costs increase 20% — requires more annual contribution
    s4 = ScenarioResult(
        scenario="goal_cost_increase_20pct",
        income_reduction=ZERO,
        expense_increase=ZERO,
        reserve_months_remaining=months_left(reserve_after),
        plan_survives=True,
        notes=(
            f"A {int(GOAL_COST_INCREASE * 100)}% increase in goal targets requires "
            "additional annual contributions. Review goal flexibility and extend "
            "timelines if the surplus cannot absorb the increase."
        ),
    )

    return (s1, s2, s3, s4)


# --------------------------------------------------------------------------- #
# Binding constraint helpers                                                   #
# --------------------------------------------------------------------------- #


def _match_binding(lines: list[AllocationLine], cap: _Capacity) -> list[BindingConstraint]:
    match_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMPLOYER_MATCH), ZERO)
    if match_alloc >= cap.employer_match_room > ZERO:
        return [BindingConstraint(
            dimension="employer_match_room",
            limit=cap.employer_match_room,
            applied=match_alloc,
            marginal_value=None,
        )]
    return []


def _tax_binding(lines: list[AllocationLine], cap: _Capacity) -> list[BindingConstraint]:
    tax_alloc = sum((l.amount for l in lines if l.use == AllocationUse.TAX_ADVANTAGED_SAVINGS), ZERO)
    if tax_alloc >= cap.tax_advantaged_room > ZERO:
        return [BindingConstraint(
            dimension="tax_advantaged_room",
            limit=cap.tax_advantaged_room,
            applied=tax_alloc,
            marginal_value=cap.marginal_tax_rate,
        )]
    return []


# --------------------------------------------------------------------------- #
# Allocation alternatives                                                      #
# --------------------------------------------------------------------------- #


def _waterfall_baseline(cap: _Capacity) -> AllocationAlternative:
    """
    Rules-based waterfall: reserve → match → high-cost debt → tax-advantaged
    → goals → lower-cost debt → buffer (REQ-020).
    """
    specs: list[_UseSpec] = []

    if cap.reserve_gap_3mo > ZERO:
        specs.append((
            AllocationUse.EMERGENCY_RESERVE,
            "Emergency reserve (3-month target)",
            "Build liquid safety buffer before any discretionary allocation.",
            cap.reserve_gap_3mo, None,
        ))
    if cap.employer_match_room > ZERO:
        specs.append((
            AllocationUse.EMPLOYER_MATCH,
            "401(k) employer match",
            "Capture full employer match — guaranteed immediate return on contribution.",
            cap.employer_match_room, None,
        ))
    for d in cap.high_cost_debts:
        specs.append((
            AllocationUse.HIGH_COST_DEBT, d.label,
            f"Eliminate {d.annual_rate:.1%} APR debt — guaranteed after-tax return.",
            d.balance, d.debt_id,
        ))
    if cap.tax_advantaged_room > ZERO:
        specs.append((
            AllocationUse.TAX_ADVANTAGED_SAVINGS,
            "Tax-advantaged accounts (401k/IRA)",
            f"Tax deferral at estimated {cap.marginal_tax_rate:.0%} marginal rate.",
            cap.tax_advantaged_room, None,
        ))
    for g in cap.goals:
        specs.append((
            AllocationUse.GOAL_FUNDING, g.label,
            f"{g.priority.value.capitalize()} priority goal.",
            g.target, g.goal_id,
        ))
    for d in cap.lower_cost_debts:
        specs.append((
            AllocationUse.LOWER_COST_DEBT, d.label,
            f"Prepay {d.annual_rate:.1%} APR debt ahead of schedule.",
            d.balance, d.debt_id,
        ))

    lines, remaining = _greedy(cap.annual_surplus, specs)
    if remaining > ZERO:
        lines.append(_buffer_line(remaining, "Discretionary buffer", "Surplus after all priority uses."))

    reserve_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMERGENCY_RESERVE), ZERO)
    binding = _match_binding(lines, cap) + _tax_binding(lines, cap)

    return AllocationAlternative(
        name="waterfall_baseline",
        label="Waterfall Baseline",
        lines=tuple(lines),
        total_allocated=sum((l.amount for l in lines), ZERO),
        binding_constraints=tuple(binding),
        opportunity_costs=(),
        assumptions=(
            "3-month emergency reserve target using liquid CASH balances.",
            f"High-cost debt threshold: {HIGH_COST_THRESHOLD:.0%} APR.",
            f"Estimated federal marginal rate: {cap.marginal_tax_rate:.0%}.",
            "401(k)/IRA limits per federal_rules_2024.",
            "Single 12-month horizon; multi-period sequencing deferred.",
        ),
        scenario_results=_apply_scenarios(cap, _money(reserve_alloc)),
        trade_off_summary=(
            "Rules-based waterfall establishes liquidity, captures guaranteed match, "
            "eliminates high-cost debt, and defers discretionary to last. Predictable "
            "and explainable but does not optimize for marginal value."
        ),
    )


def _recommended(cap: _Capacity) -> AllocationAlternative:
    """
    Marginal-value ordering.

    High-cost debt with rate > marginal_tax_rate is paid before tax-advantaged
    savings (guaranteed return exceeds immediate tax benefit). Debts at or
    below the marginal rate are paid after tax-advantaged space is filled.
    """
    specs: list[_UseSpec] = []

    if cap.reserve_gap_3mo > ZERO:
        specs.append((
            AllocationUse.EMERGENCY_RESERVE,
            "Emergency reserve (3-month target)",
            "Non-negotiable liquidity floor before any investment allocation.",
            cap.reserve_gap_3mo, None,
        ))
    if cap.employer_match_room > ZERO:
        specs.append((
            AllocationUse.EMPLOYER_MATCH,
            "401(k) employer match",
            "Highest guaranteed return available — employer match precedes all other uses.",
            cap.employer_match_room, None,
        ))

    # High-cost debts above marginal rate: pay before tax-advantaged
    above_rate = [d for d in cap.high_cost_debts if d.annual_rate > cap.marginal_tax_rate]
    at_or_below_rate = [d for d in cap.high_cost_debts if d.annual_rate <= cap.marginal_tax_rate]

    for d in above_rate:
        specs.append((
            AllocationUse.HIGH_COST_DEBT, d.label,
            f"{d.annual_rate:.1%} APR exceeds {cap.marginal_tax_rate:.0%} marginal rate — "
            "eliminating this outperforms tax-advantaged contribution on a marginal basis.",
            d.balance, d.debt_id,
        ))

    if cap.tax_advantaged_room > ZERO:
        specs.append((
            AllocationUse.TAX_ADVANTAGED_SAVINGS,
            "Tax-advantaged accounts (401k/IRA)",
            f"{cap.marginal_tax_rate:.0%} marginal rate deferred now; tax-free compounding.",
            cap.tax_advantaged_room, None,
        ))

    for d in at_or_below_rate:
        specs.append((
            AllocationUse.HIGH_COST_DEBT, d.label,
            f"{d.annual_rate:.1%} APR — below marginal rate but still eliminates guaranteed cost.",
            d.balance, d.debt_id,
        ))

    for g in cap.goals:
        specs.append((
            AllocationUse.GOAL_FUNDING, g.label,
            f"{g.priority.value.capitalize()} priority goal.",
            g.target, g.goal_id,
        ))
    for d in cap.lower_cost_debts:
        specs.append((
            AllocationUse.LOWER_COST_DEBT, d.label,
            f"{d.annual_rate:.1%} APR — compare with {ASSUMED_EQUITY_RETURN:.0%} assumed equity return.",
            d.balance, d.debt_id,
        ))

    lines, remaining = _greedy(cap.annual_surplus, specs)
    if remaining > ZERO:
        lines.append(_buffer_line(remaining, "Discretionary buffer", "Remaining surplus after all priority uses."))

    reserve_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMERGENCY_RESERVE), ZERO)
    binding = _match_binding(lines, cap) + _tax_binding(lines, cap)

    # Opportunity cost: uncaptured match (if surplus was insufficient)
    match_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMPLOYER_MATCH), ZERO)
    opp_costs: list[OpportunityCost] = []
    if cap.employer_match_room > ZERO and match_alloc < cap.employer_match_room:
        opp_costs.append(OpportunityCost(
            foregone_use="employer_match",
            foregone_amount=cap.employer_match_room - match_alloc,
            description=(
                "Uncaptured employer match due to insufficient surplus. "
                "Increasing income or reducing fixed obligations would unlock this return."
            ),
        ))

    return AllocationAlternative(
        name="recommended",
        label="Recommended",
        lines=tuple(lines),
        total_allocated=sum((l.amount for l in lines), ZERO),
        binding_constraints=tuple(binding),
        opportunity_costs=tuple(opp_costs),
        assumptions=(
            "Marginal value ordering: employer match > debt above marginal rate > "
            "tax-advantaged savings > debt at/below marginal rate.",
            f"High-cost threshold: {HIGH_COST_THRESHOLD:.0%} APR.",
            f"Estimated federal marginal rate: {cap.marginal_tax_rate:.0%}.",
            f"Assumed long-run equity return: {ASSUMED_EQUITY_RETURN:.0%} nominal.",
            "Single 12-month horizon.",
        ),
        scenario_results=_apply_scenarios(cap, _money(reserve_alloc)),
        trade_off_summary=(
            "Marginal-value ordering minimizes total interest cost while maximizing "
            "tax-deferred wealth accumulation. Pays high-rate debt before filling "
            "tax-advantaged space when the rate exceeds the marginal tax benefit."
        ),
    )


def _liquidity_preserving(cap: _Capacity) -> AllocationAlternative:
    """
    Extended 6-month reserve; defers debt prepayment; partial tax-advantaged
    and goal contributions. Maximizes optionality at the cost of higher
    interest expense.
    """
    specs: list[_UseSpec] = []

    if cap.reserve_gap_6mo > ZERO:
        specs.append((
            AllocationUse.EMERGENCY_RESERVE,
            "Emergency reserve (6-month target)",
            "Extended cushion for variable income, career transition, or near-term liquidity needs.",
            cap.reserve_gap_6mo, None,
        ))
    if cap.employer_match_room > ZERO:
        specs.append((
            AllocationUse.EMPLOYER_MATCH,
            "401(k) employer match",
            "Guaranteed return regardless of liquidity posture.",
            cap.employer_match_room, None,
        ))
    if cap.tax_advantaged_room > ZERO:
        specs.append((
            AllocationUse.TAX_ADVANTAGED_SAVINGS,
            "Tax-advantaged accounts (401k/IRA) — partial",
            "Partial contribution preserves cash flow flexibility.",
            _money(cap.tax_advantaged_room / 2), None,
        ))
    for g in cap.goals:
        if g.priority in (GoalPriority.CRITICAL, GoalPriority.HIGH):
            specs.append((
                AllocationUse.GOAL_FUNDING, g.label,
                f"{g.priority.value.capitalize()} priority goal — partial contribution.",
                _money(g.target / 2), g.goal_id,
            ))
    # No debt prepayment above minimums in this alternative

    lines, remaining = _greedy(cap.annual_surplus, specs)
    if remaining > ZERO:
        lines.append(_buffer_line(
            remaining, "Liquidity buffer",
            "Surplus held liquid — consistent with liquidity-preserving posture.",
        ))

    reserve_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMERGENCY_RESERVE), ZERO)
    high_cost_balance = sum(d.balance for d in cap.high_cost_debts)

    return AllocationAlternative(
        name="liquidity_preserving",
        label="Liquidity-Preserving",
        lines=tuple(lines),
        total_allocated=sum((l.amount for l in lines), ZERO),
        binding_constraints=(),
        opportunity_costs=(
            OpportunityCost(
                foregone_use="high_cost_debt_paydown",
                foregone_amount=high_cost_balance,
                description=(
                    "Defers high-cost debt elimination in exchange for greater liquidity. "
                    "Total interest cost is higher than the Recommended alternative."
                ),
            ),
        ) if high_cost_balance > ZERO else (),
        assumptions=(
            "6-month emergency reserve target (vs. 3-month default).",
            "Tax-advantaged contributions capped at 50% of statutory room.",
            "No discretionary debt prepayment above minimum payments.",
            "Trade-off: higher liquidity, higher long-run interest cost.",
        ),
        scenario_results=_apply_scenarios(cap, _money(reserve_alloc)),
        trade_off_summary=(
            "Maximum liquidity and optionality at the cost of higher long-run interest "
            "expense and slower debt elimination. Best suited for households with "
            "variable income, near-term large purchases, or career transition risk."
        ),
    )


def _goal_acceleration(cap: _Capacity) -> AllocationAlternative:
    """
    Front-loads CRITICAL and HIGH goals; accepts reduced reserve (2 months).
    Appropriate when a critical goal has a fixed near-term deadline.
    """
    specs: list[_UseSpec] = []

    if cap.reserve_gap_2mo > ZERO:
        specs.append((
            AllocationUse.EMERGENCY_RESERVE,
            "Emergency reserve (2-month minimum)",
            "Minimum liquidity buffer; reduced to accelerate critical goal.",
            cap.reserve_gap_2mo, None,
        ))
    if cap.employer_match_room > ZERO:
        specs.append((
            AllocationUse.EMPLOYER_MATCH,
            "401(k) employer match",
            "Guaranteed return — never defer match to accelerate goals.",
            cap.employer_match_room, None,
        ))
    for g in cap.goals:
        if g.priority in (GoalPriority.CRITICAL, GoalPriority.HIGH):
            specs.append((
                AllocationUse.GOAL_FUNDING, g.label,
                f"Front-loaded {g.priority.value} priority goal.",
                g.target, g.goal_id,
            ))
    if cap.tax_advantaged_room > ZERO:
        specs.append((
            AllocationUse.TAX_ADVANTAGED_SAVINGS,
            "Tax-advantaged accounts (401k/IRA)",
            "Maximize tax-advantaged space after critical goals are funded.",
            cap.tax_advantaged_room, None,
        ))
    for d in cap.high_cost_debts:
        specs.append((
            AllocationUse.HIGH_COST_DEBT, d.label,
            f"High-cost debt elimination after goal funding.",
            d.balance, d.debt_id,
        ))

    lines, remaining = _greedy(cap.annual_surplus, specs)
    if remaining > ZERO:
        lines.append(_buffer_line(remaining, "Discretionary buffer", "Remaining surplus after goal acceleration."))

    reserve_alloc = sum((l.amount for l in lines if l.use == AllocationUse.EMERGENCY_RESERVE), ZERO)
    reserve_foregone = max(ZERO, cap.reserve_gap_3mo - _money(reserve_alloc))

    return AllocationAlternative(
        name="goal_acceleration",
        label="Goal Acceleration",
        lines=tuple(lines),
        total_allocated=sum((l.amount for l in lines), ZERO),
        binding_constraints=(),
        opportunity_costs=(
            OpportunityCost(
                foregone_use="emergency_reserve",
                foregone_amount=reserve_foregone,
                description=(
                    "Reduced reserve (2 months vs. 3-month default) accepted in exchange "
                    "for faster goal attainment. Increases vulnerability to income disruption."
                ),
            ),
        ) if reserve_foregone > ZERO else (),
        assumptions=(
            "2-month emergency reserve target (reduced from 3-month default).",
            "Critical and high-priority goals funded before tax-advantaged savings.",
            "Medium and low goals deferred in favour of critical goals.",
            "Trade-off: faster goal attainment, lower liquidity buffer.",
        ),
        scenario_results=_apply_scenarios(cap, _money(reserve_alloc)),
        trade_off_summary=(
            "Maximizes progress toward the highest-priority goal at the cost of a "
            "reduced liquidity buffer. Best suited for CRITICAL goals with fixed "
            "near-term deadlines where timeline flexibility is unavailable."
        ),
    )


# --------------------------------------------------------------------------- #
# Entry point                                                                  #
# --------------------------------------------------------------------------- #


def optimize_household_allocation(
    household: HouseholdState,
    rules: JurisdictionRules,
) -> OptimizerResult:
    """
    Full optimizer entry point (REQ-020 through REQ-044).

    Preconditions:
      - household.synthetic must be True
      - household.completeness_report().can_proceed must be True

    Returns an OptimizerResult with baseline, three alternatives, and scenario
    stresses. When the household is infeasible (obligations exceed income),
    infeasibility is set and all alternatives contain zero-line plans.
    """
    if not household.synthetic:
        raise ValueError(
            "optimize_household_allocation: real household data is not "
            "permitted in the prototype."
        )

    report = household.completeness_report()
    if not report.can_proceed:
        raise ValueError(
            f"Household {household.household_id!r} has missing required fields: "
            + ", ".join(report.missing_required[:5])
            + ("..." if len(report.missing_required) > 5 else "")
        )

    cap = _compute_capacity(household, rules)

    baseline = _waterfall_baseline(cap)
    rec = _recommended(cap)
    liq = _liquidity_preserving(cap)
    goal_acc = _goal_acceleration(cap)

    return OptimizerResult(
        household_id=household.household_id,
        household_fingerprint=household.fingerprint(),
        annual_gross_income=cap.annual_gross,
        annual_fixed_obligations=cap.annual_fixed,
        annual_surplus=cap.annual_surplus,
        baseline=baseline,
        alternatives=(rec, liq, goal_acc),
        infeasibility=cap.infeasibility_report,
        jurisdiction_scope=rules.scope,
        period_label="12-month horizon",
        common_assumptions=(
            f"Jurisdiction scope: {rules.scope}. Not legal or tax advice.",
            "All inputs are synthetic; real household data is not accepted in the prototype.",
            "Single 12-month horizon; multi-period sequencing deferred (REQ-022 partial).",
            "Emergency reserve defined as liquid CASH account balances only.",
            "Employer match room computed from declared match tiers and member salaries.",
            f"Long-run equity return assumption: {ASSUMED_EQUITY_RETURN:.0%} nominal.",
        ),
    )
