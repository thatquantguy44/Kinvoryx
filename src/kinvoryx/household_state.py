"""Household State and Data Model — Spec 002.

Synthetic-only. Real household data is rejected at construction.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Generic, Optional, TypeVar


CENT = Decimal("0.01")
ZERO = Decimal("0")
T = TypeVar("T")


def _money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def _rate(value: Decimal | int | float | str) -> Decimal:
    v = Decimal(str(value))
    if v < ZERO:
        raise ValueError(f"rate must be non-negative, got {v}")
    return v


# --------------------------------------------------------------------------- #
# Provenance and information class                                             #
# --------------------------------------------------------------------------- #


class DataProvenance(str, Enum):
    USER_ENTERED = "user_entered"
    IMPORTED = "imported"
    INFERRED = "inferred"
    DEFAULTED = "defaulted"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class InformationClass(str, Enum):
    AUTHORITATIVE_PUBLIC = "authoritative_public"   # Tax limits, agency guidance
    INSTITUTIONAL_POLICY = "institutional_policy"   # Capital-market assumptions
    HOUSEHOLD_CONFIG = "household_config"            # Goals, preferences, restrictions
    OBSERVED_STATE = "observed_state"               # Balances, transactions, payroll
    AI_NARRATIVE = "ai_narrative"                   # Summaries — never authoritative


class Freshness(str, Enum):
    CURRENT = "current"   # Within freshness window
    STALE = "stale"       # Outside freshness window but usable with disclosure
    MISSING = "missing"   # Required but absent


@dataclass(frozen=True)
class FieldValue(Generic[T]):
    """A typed field value with full provenance metadata (REQ-DATA-001)."""

    value: Optional[T]
    provenance: DataProvenance
    information_class: InformationClass
    source: str              # Human-readable source description
    effective_date: Optional[date]
    freshness: Freshness
    owner: str               # Who provided or is responsible for this value
    confidence: Optional[str] = None  # "high" | "medium" | "low" | None
    permitted_uses: tuple[str, ...] = ()

    def is_usable(self) -> bool:
        return (
            self.provenance != DataProvenance.UNAVAILABLE
            and self.freshness != Freshness.MISSING
            and self.value is not None
        )

    def requires_disclosure(self) -> bool:
        """True when the value is usable but carries a quality caveat."""
        return (
            self.freshness == Freshness.STALE
            or self.provenance == DataProvenance.DEFAULTED
        )


# --------------------------------------------------------------------------- #
# People                                                                       #
# --------------------------------------------------------------------------- #


class MemberRole(str, Enum):
    PRIMARY = "primary"
    PARTNER = "partner"
    DEPENDENT = "dependent"


@dataclass(frozen=True)
class HouseholdMember:
    member_id: str
    role: MemberRole
    birth_year: Optional[int]
    # Categories of decisions that require this member's explicit approval
    approval_required_for: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.member_id:
            raise ValueError("member_id is required")


# --------------------------------------------------------------------------- #
# Income                                                                       #
# --------------------------------------------------------------------------- #


class IncomeType(str, Enum):
    SALARY = "salary"
    BONUS = "bonus"
    EQUITY_VESTING = "equity_vesting"
    SELF_EMPLOYMENT = "self_employment"
    RENTAL = "rental"
    OTHER = "other"


@dataclass(frozen=True)
class IncomeSource:
    source_id: str
    member_id: str
    income_type: IncomeType
    annual_gross: FieldValue[Decimal]
    work_jurisdiction: Optional[str]    # State/locality code for tax routing
    effective_from: Optional[date] = None
    effective_through: Optional[date] = None

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id is required")
        if not self.member_id:
            raise ValueError("member_id is required")


# --------------------------------------------------------------------------- #
# Expenses                                                                     #
# --------------------------------------------------------------------------- #


class ExpenseCategory(str, Enum):
    ESSENTIAL = "essential"         # Housing, utilities, food, insurance
    DISCRETIONARY = "discretionary"
    OBLIGATION = "obligation"       # Contractual: loan minimums, subscriptions


@dataclass(frozen=True)
class Expense:
    expense_id: str
    category: ExpenseCategory
    label: str
    monthly_amount: FieldValue[Decimal]

    def __post_init__(self) -> None:
        if not self.expense_id:
            raise ValueError("expense_id is required")
        if not self.label:
            raise ValueError("expense label is required")


# --------------------------------------------------------------------------- #
# Assets / accounts                                                            #
# --------------------------------------------------------------------------- #


class AccountType(str, Enum):
    CASH = "cash"
    TAXABLE_BROKERAGE = "taxable_brokerage"
    TRADITIONAL_401K = "traditional_401k"
    ROTH_401K = "roth_401k"
    TRADITIONAL_IRA = "traditional_ira"
    ROTH_IRA = "roth_ira"
    HSA = "hsa"
    PLAN_529 = "plan_529"
    OTHER = "other"


@dataclass(frozen=True)
class Account:
    account_id: str
    account_type: AccountType
    owner_member_id: str
    balance: FieldValue[Decimal]
    institution: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.account_id:
            raise ValueError("account_id is required")
        if not self.owner_member_id:
            raise ValueError("owner_member_id is required")


# --------------------------------------------------------------------------- #
# Liabilities                                                                  #
# --------------------------------------------------------------------------- #


class DebtCategory(str, Enum):
    MORTGAGE = "mortgage"
    STUDENT_LOAN = "student_loan"
    AUTO = "auto"
    CREDIT_CARD = "credit_card"
    PERSONAL_LOAN = "personal_loan"
    OTHER = "other"


@dataclass(frozen=True)
class HouseholdDebt:
    debt_id: str
    category: DebtCategory
    label: str
    balance: FieldValue[Decimal]
    annual_rate: FieldValue[Decimal]        # APR as decimal (e.g. 0.065 = 6.5%)
    monthly_minimum: FieldValue[Decimal]
    prepayment_penalty: bool = False
    owner_member_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.debt_id:
            raise ValueError("debt_id is required")
        if not self.label:
            raise ValueError("debt label is required")


# --------------------------------------------------------------------------- #
# Benefits                                                                     #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class EmployerMatchTier:
    """A single tier of an employer match formula."""
    match_rate: Decimal                    # e.g. Decimal("0.50") for 50%
    up_to_percent_of_salary: Decimal       # e.g. Decimal("0.06") for first 6%

    def __post_init__(self) -> None:
        if self.match_rate < ZERO:
            raise ValueError("match_rate must be non-negative")
        if self.up_to_percent_of_salary <= ZERO:
            raise ValueError("up_to_percent_of_salary must be positive")


@dataclass(frozen=True)
class EmployerBenefit:
    benefit_id: str
    member_id: str
    plan_type: str                         # e.g. "401k", "SIMPLE IRA"
    annual_employee_limit: FieldValue[Decimal]
    match_tiers: tuple[EmployerMatchTier, ...]
    insurance_deductible: Optional[FieldValue[Decimal]] = None

    def __post_init__(self) -> None:
        if not self.benefit_id:
            raise ValueError("benefit_id is required")
        if not self.member_id:
            raise ValueError("member_id is required")
        if not self.plan_type:
            raise ValueError("plan_type is required")


# --------------------------------------------------------------------------- #
# Goals                                                                        #
# --------------------------------------------------------------------------- #


class GoalPriority(str, Enum):
    CRITICAL = "critical"    # Must achieve — failure is unacceptable
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class GoalFlexibility(str, Enum):
    FIXED = "fixed"                    # Date and amount are non-negotiable
    DATE_FLEXIBLE = "date_flexible"
    AMOUNT_FLEXIBLE = "amount_flexible"
    FULLY_FLEXIBLE = "fully_flexible"


@dataclass(frozen=True)
class Goal:
    goal_id: str
    label: str
    target_amount: FieldValue[Decimal]
    priority: GoalPriority
    flexibility: GoalFlexibility
    owner_member_ids: tuple[str, ...]
    minimum_acceptable_amount: Optional[Decimal] = None
    target_date: Optional[date] = None
    horizon_years: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.goal_id:
            raise ValueError("goal_id is required")
        if not self.label:
            raise ValueError("goal label is required")
        if self.target_date is None and self.horizon_years is None:
            raise ValueError(
                f"Goal {self.goal_id}: must set target_date or horizon_years"
            )
        if (
            self.minimum_acceptable_amount is not None
            and self.target_amount.value is not None
            and self.minimum_acceptable_amount > self.target_amount.value
        ):
            raise ValueError(
                f"Goal {self.goal_id}: minimum_acceptable_amount exceeds target_amount"
            )
        if not self.owner_member_ids:
            raise ValueError(
                f"Goal {self.goal_id}: at least one owner_member_id is required"
            )


# --------------------------------------------------------------------------- #
# Constraints                                                                  #
# --------------------------------------------------------------------------- #


class ConstraintType(str, Enum):
    HARD = "hard"              # Cannot be violated; optimization fails if breached
    SOFT = "soft"              # Preference — violated only with explicit disclosure
    ASPIRATION = "aspiration"  # Nice-to-have; noted but carries no optimization weight


@dataclass(frozen=True)
class HouseholdConstraint:
    constraint_id: str
    constraint_type: ConstraintType
    dimension: str              # e.g. "monthly_cash_outflow", "equity_allocation"
    label: str
    limit_value: Optional[Decimal] = None
    owner_member_id: Optional[str] = None  # None = household-level constraint

    def __post_init__(self) -> None:
        if not self.constraint_id:
            raise ValueError("constraint_id is required")
        if not self.dimension:
            raise ValueError("dimension is required")
        if not self.label:
            raise ValueError("constraint label is required")


# --------------------------------------------------------------------------- #
# Tax profile                                                                  #
# --------------------------------------------------------------------------- #


class FilingStatus(str, Enum):
    SINGLE = "single"
    MARRIED_FILING_JOINTLY = "married_filing_jointly"
    MARRIED_FILING_SEPARATELY = "married_filing_separately"
    HEAD_OF_HOUSEHOLD = "head_of_household"


@dataclass(frozen=True)
class TaxProfile:
    filing_status: FilingStatus
    domicile_state: Optional[str]             # State of legal residence
    work_state: Optional[str]                 # Primary work location
    additional_income_jurisdictions: tuple[str, ...] = ()
    # Explicit disclosure of what tax rules this profile covers
    supported_rule_scope: str = "federal_income_2024"


# --------------------------------------------------------------------------- #
# Decision history                                                             #
# --------------------------------------------------------------------------- #


class DecisionOutcome(str, Enum):
    APPROVED = "approved"
    OVERRIDDEN = "overridden"
    REJECTED = "rejected"
    PENDING = "pending"


@dataclass(frozen=True)
class DecisionRecord:
    record_id: str
    decision_type: str        # e.g. "cash_inflow_allocation"
    brief_fingerprint: str    # SHA-256 of the decision brief for audit linking
    outcome: DecisionOutcome
    recorded_at: date
    approver_member_id: Optional[str] = None
    override_reason: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.record_id:
            raise ValueError("record_id is required")
        if not self.brief_fingerprint:
            raise ValueError("brief_fingerprint is required")


# --------------------------------------------------------------------------- #
# Completeness / freshness gate                                                #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class CompletenessReport:
    """Readiness assessment before optimization (REQ-003, AC)."""

    missing_required: tuple[str, ...]   # Field paths that are UNAVAILABLE/MISSING
    stale_fields: tuple[str, ...]       # Fields whose freshness is STALE
    defaulted_fields: tuple[str, ...]   # Fields using DEFAULTED provenance
    can_proceed: bool                   # False when any required field is missing
    disclosure_required: bool           # True when stale or defaulted fields are present


# --------------------------------------------------------------------------- #
# Root aggregate                                                               #
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class HouseholdState:
    """
    The complete time-indexed state of a household.

    All fields are synthetic only. Real household data is rejected at
    construction to prevent premature pilot use before governance is ready.
    """

    household_id: str
    synthetic: bool
    members: tuple[HouseholdMember, ...]
    income_sources: tuple[IncomeSource, ...]
    expenses: tuple[Expense, ...]
    accounts: tuple[Account, ...]
    debts: tuple[HouseholdDebt, ...]
    benefits: tuple[EmployerBenefit, ...]
    goals: tuple[Goal, ...]
    constraints: tuple[HouseholdConstraint, ...]
    tax_profile: TaxProfile
    decision_history: tuple[DecisionRecord, ...] = ()

    def __post_init__(self) -> None:
        if not self.household_id:
            raise ValueError("household_id is required")
        if not self.synthetic:
            raise ValueError(
                "HouseholdState: real household data is not permitted in the "
                "prototype. Set synthetic=True for demonstration and testing only."
            )
        if not self.members:
            raise ValueError("at least one HouseholdMember is required")

        member_ids = {m.member_id for m in self.members}
        primary_count = sum(1 for m in self.members if m.role == MemberRole.PRIMARY)
        if primary_count != 1:
            raise ValueError(
                f"exactly one PRIMARY member is required, found {primary_count}"
            )

        for inc in self.income_sources:
            if inc.member_id not in member_ids:
                raise ValueError(
                    f"IncomeSource {inc.source_id!r}: "
                    f"member_id {inc.member_id!r} not in household"
                )
        for acct in self.accounts:
            if acct.owner_member_id not in member_ids:
                raise ValueError(
                    f"Account {acct.account_id!r}: "
                    f"owner_member_id {acct.owner_member_id!r} not in household"
                )
        for debt in self.debts:
            if debt.owner_member_id is not None and debt.owner_member_id not in member_ids:
                raise ValueError(
                    f"HouseholdDebt {debt.debt_id!r}: "
                    f"owner_member_id {debt.owner_member_id!r} not in household"
                )
        for ben in self.benefits:
            if ben.member_id not in member_ids:
                raise ValueError(
                    f"EmployerBenefit {ben.benefit_id!r}: "
                    f"member_id {ben.member_id!r} not in household"
                )
        for goal in self.goals:
            for mid in goal.owner_member_ids:
                if mid not in member_ids:
                    raise ValueError(
                        f"Goal {goal.goal_id!r}: "
                        f"owner_member_id {mid!r} not in household"
                    )
        for con in self.constraints:
            if con.owner_member_id is not None and con.owner_member_id not in member_ids:
                raise ValueError(
                    f"HouseholdConstraint {con.constraint_id!r}: "
                    f"owner_member_id {con.owner_member_id!r} not in household"
                )

    # --- Accessors --------------------------------------------------------- #

    def member_by_id(self, member_id: str) -> Optional[HouseholdMember]:
        return next((m for m in self.members if m.member_id == member_id), None)

    def primary_member(self) -> HouseholdMember:
        return next(m for m in self.members if m.role == MemberRole.PRIMARY)

    def goals_by_priority(self) -> tuple[Goal, ...]:
        order = {
            GoalPriority.CRITICAL: 0,
            GoalPriority.HIGH: 1,
            GoalPriority.MEDIUM: 2,
            GoalPriority.LOW: 3,
        }
        return tuple(sorted(self.goals, key=lambda g: order[g.priority]))

    # --- Fingerprint ------------------------------------------------------- #

    def fingerprint(self) -> str:
        """Deterministic SHA-256 for audit linking to decision briefs."""
        payload = json.dumps(
            {
                "household_id": self.household_id,
                "member_ids": sorted(m.member_id for m in self.members),
                "goal_ids": sorted(g.goal_id for g in self.goals),
                "debt_ids": sorted(d.debt_id for d in self.debts),
                "account_ids": sorted(a.account_id for a in self.accounts),
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    # --- Completeness / freshness gate ------------------------------------- #

    def completeness_report(self) -> CompletenessReport:
        """
        Assess readiness before optimization (REQ-003).

        A recommendation cannot proceed when missing_required is non-empty
        unless a bounded sensitivity result or review route is used (AC).
        """
        missing: list[str] = []
        stale: list[str] = []
        defaulted: list[str] = []

        def _check(fv: FieldValue, path: str) -> None:
            if (
                fv.provenance == DataProvenance.UNAVAILABLE
                or fv.freshness == Freshness.MISSING
                or fv.value is None
            ):
                missing.append(path)
            elif fv.freshness == Freshness.STALE:
                stale.append(path)
            elif fv.provenance == DataProvenance.DEFAULTED:
                defaulted.append(path)

        for inc in self.income_sources:
            _check(inc.annual_gross, f"income_sources[{inc.source_id}].annual_gross")
        for exp in self.expenses:
            _check(exp.monthly_amount, f"expenses[{exp.expense_id}].monthly_amount")
        for acct in self.accounts:
            _check(acct.balance, f"accounts[{acct.account_id}].balance")
        for debt in self.debts:
            _check(debt.balance, f"debts[{debt.debt_id}].balance")
            _check(debt.annual_rate, f"debts[{debt.debt_id}].annual_rate")
            _check(debt.monthly_minimum, f"debts[{debt.debt_id}].monthly_minimum")
        for goal in self.goals:
            _check(goal.target_amount, f"goals[{goal.goal_id}].target_amount")
        for ben in self.benefits:
            _check(
                ben.annual_employee_limit,
                f"benefits[{ben.benefit_id}].annual_employee_limit",
            )

        return CompletenessReport(
            missing_required=tuple(missing),
            stale_fields=tuple(stale),
            defaulted_fields=tuple(defaulted),
            can_proceed=len(missing) == 0,
            disclosure_required=len(stale) > 0 or len(defaulted) > 0,
        )

    # --- Conflict detection ------------------------------------------------ #

    def contradictory_goals(self) -> tuple[tuple[Goal, Goal], ...]:
        """
        Flag pairs of CRITICAL/HIGH FIXED goals (REQ-013).

        Two fixed goals at critical or high priority have no scheduling slack
        and require explicit prioritization rather than silent resolution.
        Full conflict resolution belongs to the optimizer (Spec 004).
        """
        high_fixed = [
            g for g in self.goals
            if g.priority in (GoalPriority.CRITICAL, GoalPriority.HIGH)
            and g.flexibility == GoalFlexibility.FIXED
        ]
        conflicts: list[tuple[Goal, Goal]] = []
        seen: set[tuple[str, str]] = set()
        for i, g1 in enumerate(high_fixed):
            for g2 in high_fixed[i + 1:]:
                pair = tuple(sorted([g1.goal_id, g2.goal_id]))
                if pair not in seen:
                    seen.add(pair)  # type: ignore[arg-type]
                    conflicts.append((g1, g2))
        return tuple(conflicts)
