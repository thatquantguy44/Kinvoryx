"""Acceptance tests for the Spec 002 Household State and Data Model."""

from datetime import date
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.household_state import (
    Account,
    AccountType,
    CompletenessReport,
    ConstraintType,
    DataProvenance,
    DecisionOutcome,
    DecisionRecord,
    EmployerBenefit,
    EmployerMatchTier,
    Expense,
    ExpenseCategory,
    FieldValue,
    FilingStatus,
    Freshness,
    Goal,
    GoalFlexibility,
    GoalPriority,
    HouseholdConstraint,
    HouseholdDebt,
    HouseholdMember,
    HouseholdState,
    IncomeSource,
    IncomeType,
    InformationClass,
    MemberRole,
    TaxProfile,
)


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #


def _current_money(amount: str, source: str = "user_entered") -> FieldValue[Decimal]:
    return FieldValue(
        value=Decimal(amount),
        provenance=DataProvenance.USER_ENTERED,
        information_class=InformationClass.HOUSEHOLD_CONFIG,
        source=source,
        effective_date=date(2026, 1, 1),
        freshness=Freshness.CURRENT,
        owner="primary",
    )


def _primary() -> HouseholdMember:
    return HouseholdMember(
        member_id="primary",
        role=MemberRole.PRIMARY,
        birth_year=1988,
    )


def _partner() -> HouseholdMember:
    return HouseholdMember(
        member_id="partner",
        role=MemberRole.PARTNER,
        birth_year=1990,
    )


def _tax_profile() -> TaxProfile:
    return TaxProfile(
        filing_status=FilingStatus.MARRIED_FILING_JOINTLY,
        domicile_state="CA",
        work_state="CA",
    )


def _minimal_household(**overrides) -> HouseholdState:
    """Minimal valid synthetic household with one income, expense, account, debt, benefit, and goal."""
    defaults = dict(
        household_id="synthetic-001",
        synthetic=True,
        members=(_primary(),),
        income_sources=(
            IncomeSource(
                source_id="salary-primary",
                member_id="primary",
                income_type=IncomeType.SALARY,
                annual_gross=_current_money("180000"),
                work_jurisdiction="CA",
            ),
        ),
        expenses=(
            Expense(
                expense_id="housing",
                category=ExpenseCategory.ESSENTIAL,
                label="Rent",
                monthly_amount=_current_money("3500"),
            ),
        ),
        accounts=(
            Account(
                account_id="checking",
                account_type=AccountType.CASH,
                owner_member_id="primary",
                balance=_current_money("25000"),
                institution="Chase",
            ),
        ),
        debts=(
            HouseholdDebt(
                debt_id="student-loan",
                category=__import__("kinvoryx.household_state", fromlist=["DebtCategory"]).DebtCategory.STUDENT_LOAN,
                label="Student Loan",
                balance=_current_money("28000"),
                annual_rate=FieldValue(
                    value=Decimal("0.065"),
                    provenance=DataProvenance.USER_ENTERED,
                    information_class=InformationClass.OBSERVED_STATE,
                    source="servicer",
                    effective_date=date(2026, 1, 1),
                    freshness=Freshness.CURRENT,
                    owner="primary",
                ),
                monthly_minimum=_current_money("320"),
            ),
        ),
        benefits=(
            EmployerBenefit(
                benefit_id="401k-primary",
                member_id="primary",
                plan_type="401k",
                annual_employee_limit=_current_money("23000"),
                match_tiers=(
                    EmployerMatchTier(
                        match_rate=Decimal("0.50"),
                        up_to_percent_of_salary=Decimal("0.06"),
                    ),
                ),
            ),
        ),
        goals=(
            Goal(
                goal_id="emergency-fund",
                label="Emergency fund",
                target_amount=_current_money("30000"),
                priority=GoalPriority.CRITICAL,
                flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
                owner_member_ids=("primary",),
                horizon_years=1,
            ),
        ),
        constraints=(),
        tax_profile=_tax_profile(),
    )
    defaults.update(overrides)
    return HouseholdState(**defaults)


# --------------------------------------------------------------------------- #
# FieldValue tests                                                             #
# --------------------------------------------------------------------------- #


class FieldValueTests(unittest.TestCase):
    def test_usable_current_user_entered(self) -> None:
        fv = _current_money("1000")
        self.assertTrue(fv.is_usable())
        self.assertFalse(fv.requires_disclosure())

    def test_unavailable_is_not_usable(self) -> None:
        fv = FieldValue(
            value=None,
            provenance=DataProvenance.UNAVAILABLE,
            information_class=InformationClass.OBSERVED_STATE,
            source="unknown",
            effective_date=None,
            freshness=Freshness.MISSING,
            owner="primary",
        )
        self.assertFalse(fv.is_usable())

    def test_stale_is_usable_but_requires_disclosure(self) -> None:
        fv = FieldValue(
            value=Decimal("5000"),
            provenance=DataProvenance.IMPORTED,
            information_class=InformationClass.OBSERVED_STATE,
            source="bank",
            effective_date=date(2025, 1, 1),
            freshness=Freshness.STALE,
            owner="primary",
        )
        self.assertTrue(fv.is_usable())
        self.assertTrue(fv.requires_disclosure())

    def test_defaulted_requires_disclosure(self) -> None:
        fv = FieldValue(
            value=Decimal("0.07"),
            provenance=DataProvenance.DEFAULTED,
            information_class=InformationClass.INSTITUTIONAL_POLICY,
            source="system_default",
            effective_date=None,
            freshness=Freshness.CURRENT,
            owner="system",
        )
        self.assertTrue(fv.is_usable())
        self.assertTrue(fv.requires_disclosure())


# --------------------------------------------------------------------------- #
# HouseholdMember tests                                                        #
# --------------------------------------------------------------------------- #


class HouseholdMemberTests(unittest.TestCase):
    def test_valid_primary_member(self) -> None:
        m = _primary()
        self.assertEqual(m.member_id, "primary")
        self.assertEqual(m.role, MemberRole.PRIMARY)

    def test_empty_member_id_rejected(self) -> None:
        with self.assertRaises(ValueError):
            HouseholdMember(member_id="", role=MemberRole.PRIMARY, birth_year=1985)

    def test_approval_rights_stored(self) -> None:
        m = HouseholdMember(
            member_id="partner",
            role=MemberRole.PARTNER,
            birth_year=1990,
            approval_required_for=("investment_allocation", "debt_paydown"),
        )
        self.assertIn("investment_allocation", m.approval_required_for)


# --------------------------------------------------------------------------- #
# HouseholdState construction tests                                            #
# --------------------------------------------------------------------------- #


class HouseholdStateConstructionTests(unittest.TestCase):
    def test_minimal_household_constructs(self) -> None:
        h = _minimal_household()
        self.assertEqual(h.household_id, "synthetic-001")
        self.assertTrue(h.synthetic)

    def test_real_data_rejected(self) -> None:
        with self.assertRaises(ValueError, msg="should reject synthetic=False"):
            _minimal_household(synthetic=False)

    def test_empty_members_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _minimal_household(members=())

    def test_missing_primary_member_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _minimal_household(
                members=(
                    HouseholdMember(member_id="p1", role=MemberRole.PARTNER, birth_year=1990),
                )
            )

    def test_two_primary_members_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _minimal_household(
                members=(
                    HouseholdMember(member_id="p1", role=MemberRole.PRIMARY, birth_year=1985),
                    HouseholdMember(member_id="p2", role=MemberRole.PRIMARY, birth_year=1987),
                )
            )

    def test_income_source_unknown_member_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _minimal_household(
                income_sources=(
                    IncomeSource(
                        source_id="salary-ghost",
                        member_id="nobody",
                        income_type=IncomeType.SALARY,
                        annual_gross=_current_money("100000"),
                        work_jurisdiction="CA",
                    ),
                )
            )

    def test_account_unknown_member_rejected(self) -> None:
        from kinvoryx.household_state import Account, AccountType
        with self.assertRaises(ValueError):
            _minimal_household(
                accounts=(
                    Account(
                        account_id="acct-x",
                        account_type=AccountType.CASH,
                        owner_member_id="ghost",
                        balance=_current_money("1000"),
                    ),
                )
            )

    def test_goal_unknown_member_rejected(self) -> None:
        with self.assertRaises(ValueError):
            _minimal_household(
                goals=(
                    Goal(
                        goal_id="g1",
                        label="Vacation",
                        target_amount=_current_money("10000"),
                        priority=GoalPriority.LOW,
                        flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                        owner_member_ids=("ghost",),
                        horizon_years=2,
                    ),
                )
            )

    def test_two_member_household_constructs(self) -> None:
        h = _minimal_household(
            members=(_primary(), _partner()),
            goals=(
                Goal(
                    goal_id="goal-joint",
                    label="Down payment",
                    target_amount=_current_money("80000"),
                    priority=GoalPriority.HIGH,
                    flexibility=GoalFlexibility.DATE_FLEXIBLE,
                    owner_member_ids=("primary", "partner"),
                    horizon_years=3,
                ),
            ),
        )
        self.assertEqual(len(h.members), 2)


# --------------------------------------------------------------------------- #
# Completeness / freshness gate tests                                          #
# --------------------------------------------------------------------------- #


class CompletenessReportTests(unittest.TestCase):
    def test_fully_complete_household_can_proceed(self) -> None:
        h = _minimal_household()
        report = h.completeness_report()
        self.assertTrue(report.can_proceed)
        self.assertEqual(report.missing_required, ())
        self.assertFalse(report.disclosure_required)

    def test_missing_income_blocks_proceed(self) -> None:
        missing_fv: FieldValue[Decimal] = FieldValue(
            value=None,
            provenance=DataProvenance.UNAVAILABLE,
            information_class=InformationClass.OBSERVED_STATE,
            source="unknown",
            effective_date=None,
            freshness=Freshness.MISSING,
            owner="primary",
        )
        h = _minimal_household(
            income_sources=(
                IncomeSource(
                    source_id="salary-primary",
                    member_id="primary",
                    income_type=IncomeType.SALARY,
                    annual_gross=missing_fv,
                    work_jurisdiction="CA",
                ),
            )
        )
        report = h.completeness_report()
        self.assertFalse(report.can_proceed)
        self.assertIn("income_sources[salary-primary].annual_gross", report.missing_required)

    def test_stale_balance_triggers_disclosure(self) -> None:
        stale_balance: FieldValue[Decimal] = FieldValue(
            value=Decimal("25000"),
            provenance=DataProvenance.IMPORTED,
            information_class=InformationClass.OBSERVED_STATE,
            source="bank_import",
            effective_date=date(2025, 6, 1),
            freshness=Freshness.STALE,
            owner="primary",
        )
        h = _minimal_household(
            accounts=(
                Account(
                    account_id="checking",
                    account_type=AccountType.CASH,
                    owner_member_id="primary",
                    balance=stale_balance,
                ),
            )
        )
        report = h.completeness_report()
        self.assertTrue(report.can_proceed)
        self.assertTrue(report.disclosure_required)
        self.assertIn("accounts[checking].balance", report.stale_fields)

    def test_defaulted_field_triggers_disclosure(self) -> None:
        defaulted_rate: FieldValue[Decimal] = FieldValue(
            value=Decimal("0.065"),
            provenance=DataProvenance.DEFAULTED,
            information_class=InformationClass.INSTITUTIONAL_POLICY,
            source="system_default",
            effective_date=None,
            freshness=Freshness.CURRENT,
            owner="system",
        )
        from kinvoryx.household_state import DebtCategory
        h = _minimal_household(
            debts=(
                HouseholdDebt(
                    debt_id="student-loan",
                    category=DebtCategory.STUDENT_LOAN,
                    label="Student Loan",
                    balance=_current_money("28000"),
                    annual_rate=defaulted_rate,
                    monthly_minimum=_current_money("320"),
                ),
            )
        )
        report = h.completeness_report()
        self.assertTrue(report.can_proceed)
        self.assertTrue(report.disclosure_required)
        self.assertIn("debts[student-loan].annual_rate", report.defaulted_fields)


# --------------------------------------------------------------------------- #
# Goal tests                                                                   #
# --------------------------------------------------------------------------- #


class GoalTests(unittest.TestCase):
    def test_goal_without_date_or_horizon_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Goal(
                goal_id="g1",
                label="Mystery goal",
                target_amount=_current_money("5000"),
                priority=GoalPriority.LOW,
                flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                owner_member_ids=("primary",),
            )

    def test_minimum_exceeds_target_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Goal(
                goal_id="g1",
                label="Bad goal",
                target_amount=_current_money("5000"),
                minimum_acceptable_amount=Decimal("6000"),
                priority=GoalPriority.MEDIUM,
                flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
                owner_member_ids=("primary",),
                horizon_years=2,
            )

    def test_goal_without_owners_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Goal(
                goal_id="g1",
                label="No owner",
                target_amount=_current_money("10000"),
                priority=GoalPriority.MEDIUM,
                flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                owner_member_ids=(),
                horizon_years=2,
            )

    def test_target_date_accepted_instead_of_horizon(self) -> None:
        g = Goal(
            goal_id="g1",
            label="Home purchase",
            target_amount=_current_money("80000"),
            priority=GoalPriority.HIGH,
            flexibility=GoalFlexibility.DATE_FLEXIBLE,
            owner_member_ids=("primary",),
            target_date=date(2029, 6, 1),
        )
        self.assertEqual(g.target_date, date(2029, 6, 1))


# --------------------------------------------------------------------------- #
# Goal priority ordering                                                       #
# --------------------------------------------------------------------------- #


class GoalPriorityOrderingTests(unittest.TestCase):
    def test_goals_sorted_by_priority(self) -> None:
        h = _minimal_household(
            goals=(
                Goal(
                    goal_id="low-goal",
                    label="Vacation",
                    target_amount=_current_money("5000"),
                    priority=GoalPriority.LOW,
                    flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                    owner_member_ids=("primary",),
                    horizon_years=1,
                ),
                Goal(
                    goal_id="critical-goal",
                    label="Emergency fund",
                    target_amount=_current_money("30000"),
                    priority=GoalPriority.CRITICAL,
                    flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
                    owner_member_ids=("primary",),
                    horizon_years=1,
                ),
                Goal(
                    goal_id="medium-goal",
                    label="Car fund",
                    target_amount=_current_money("15000"),
                    priority=GoalPriority.MEDIUM,
                    flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                    owner_member_ids=("primary",),
                    horizon_years=2,
                ),
            )
        )
        ordered = h.goals_by_priority()
        self.assertEqual(ordered[0].goal_id, "critical-goal")
        self.assertEqual(ordered[1].goal_id, "medium-goal")
        self.assertEqual(ordered[2].goal_id, "low-goal")


# --------------------------------------------------------------------------- #
# Contradictory goals tests                                                    #
# --------------------------------------------------------------------------- #


class ContradictoryGoalsTests(unittest.TestCase):
    def test_two_fixed_critical_goals_flagged(self) -> None:
        h = _minimal_household(
            goals=(
                Goal(
                    goal_id="g1",
                    label="Down payment",
                    target_amount=_current_money("80000"),
                    priority=GoalPriority.CRITICAL,
                    flexibility=GoalFlexibility.FIXED,
                    owner_member_ids=("primary",),
                    target_date=date(2028, 6, 1),
                ),
                Goal(
                    goal_id="g2",
                    label="Emergency fund",
                    target_amount=_current_money("30000"),
                    priority=GoalPriority.CRITICAL,
                    flexibility=GoalFlexibility.FIXED,
                    owner_member_ids=("primary",),
                    target_date=date(2027, 12, 1),
                ),
            )
        )
        conflicts = h.contradictory_goals()
        self.assertEqual(len(conflicts), 1)
        conflict_ids = {g.goal_id for g in conflicts[0]}
        self.assertEqual(conflict_ids, {"g1", "g2"})

    def test_flexible_goals_not_flagged(self) -> None:
        h = _minimal_household(
            goals=(
                Goal(
                    goal_id="g1",
                    label="Down payment",
                    target_amount=_current_money("80000"),
                    priority=GoalPriority.CRITICAL,
                    flexibility=GoalFlexibility.DATE_FLEXIBLE,
                    owner_member_ids=("primary",),
                    horizon_years=3,
                ),
                Goal(
                    goal_id="g2",
                    label="Emergency fund",
                    target_amount=_current_money("30000"),
                    priority=GoalPriority.HIGH,
                    flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
                    owner_member_ids=("primary",),
                    horizon_years=1,
                ),
            )
        )
        self.assertEqual(h.contradictory_goals(), ())

    def test_single_goal_no_conflict(self) -> None:
        h = _minimal_household()
        self.assertEqual(h.contradictory_goals(), ())


# --------------------------------------------------------------------------- #
# Fingerprint tests                                                            #
# --------------------------------------------------------------------------- #


class FingerprintTests(unittest.TestCase):
    def test_fingerprint_is_deterministic(self) -> None:
        h1 = _minimal_household()
        h2 = _minimal_household()
        self.assertEqual(h1.fingerprint(), h2.fingerprint())

    def test_different_household_ids_differ(self) -> None:
        h1 = _minimal_household(household_id="synthetic-001")
        h2 = _minimal_household(household_id="synthetic-002")
        self.assertNotEqual(h1.fingerprint(), h2.fingerprint())

    def test_fingerprint_is_64_hex_chars(self) -> None:
        h = _minimal_household()
        fp = h.fingerprint()
        self.assertEqual(len(fp), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in fp))


if __name__ == "__main__":
    unittest.main()
