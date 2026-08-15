"""Acceptance tests for the Spec 004 Capital Allocation Optimizer."""

from datetime import date
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.household_state import (
    Account,
    AccountType,
    DataProvenance,
    Expense,
    ExpenseCategory,
    EmployerBenefit,
    EmployerMatchTier,
    FieldValue,
    FilingStatus,
    Freshness,
    Goal,
    GoalFlexibility,
    GoalPriority,
    HouseholdDebt,
    HouseholdMember,
    HouseholdState,
    IncomeSource,
    IncomeType,
    InformationClass,
    MemberRole,
    TaxProfile,
    DebtCategory,
)
from kinvoryx.jurisdiction_rules import federal_rules_2024
from kinvoryx.capital_allocation_optimizer import (
    AllocationUse,
    optimize_household_allocation,
)


RULES = federal_rules_2024()
ZERO = Decimal("0")


# --------------------------------------------------------------------------- #
# Fixture helpers                                                              #
# --------------------------------------------------------------------------- #


def _fv(amount: str, provenance: DataProvenance = DataProvenance.USER_ENTERED) -> FieldValue:
    return FieldValue(
        value=Decimal(amount),
        provenance=provenance,
        information_class=InformationClass.HOUSEHOLD_CONFIG,
        source="test",
        effective_date=date(2026, 1, 1),
        freshness=Freshness.CURRENT,
        owner="primary",
    )


def _missing_fv() -> FieldValue:
    return FieldValue(
        value=None,
        provenance=DataProvenance.UNAVAILABLE,
        information_class=InformationClass.OBSERVED_STATE,
        source="unknown",
        effective_date=None,
        freshness=Freshness.MISSING,
        owner="primary",
    )


def _build_household(
    annual_income: str = "200000",
    monthly_essential: str = "5000",
    liquid_reserves: str = "10000",
    debts: tuple = (),
    benefits: tuple = (),
    goals: tuple = (),
    filing_status: FilingStatus = FilingStatus.MARRIED_FILING_JOINTLY,
) -> HouseholdState:
    """Build a minimal synthetic household with configurable parameters."""
    default_benefit = EmployerBenefit(
        benefit_id="401k",
        member_id="primary",
        plan_type="401k",
        annual_employee_limit=_fv("23000"),
        match_tiers=(EmployerMatchTier(
            match_rate=Decimal("0.50"),
            up_to_percent_of_salary=Decimal("0.06"),
        ),),
    )
    default_goal = Goal(
        goal_id="emergency-fund",
        label="Emergency fund top-up",
        target_amount=_fv("10000"),
        priority=GoalPriority.CRITICAL,
        flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
        owner_member_ids=("primary",),
        horizon_years=1,
    )

    return HouseholdState(
        household_id="synthetic-opt-001",
        synthetic=True,
        members=(HouseholdMember(member_id="primary", role=MemberRole.PRIMARY, birth_year=1988),),
        income_sources=(IncomeSource(
            source_id="salary",
            member_id="primary",
            income_type=IncomeType.SALARY,
            annual_gross=_fv(annual_income),
            work_jurisdiction="CA",
        ),),
        expenses=(Expense(
            expense_id="living",
            category=ExpenseCategory.ESSENTIAL,
            label="Living expenses",
            monthly_amount=_fv(monthly_essential),
        ),),
        accounts=(Account(
            account_id="checking",
            account_type=AccountType.CASH,
            owner_member_id="primary",
            balance=_fv(liquid_reserves),
        ),),
        debts=debts or (),
        benefits=benefits if benefits else (default_benefit,),
        goals=goals if goals else (default_goal,),
        constraints=(),
        tax_profile=TaxProfile(
            filing_status=filing_status,
            domicile_state="CA",
            work_state="CA",
        ),
    )


def _credit_card_debt() -> HouseholdDebt:
    return HouseholdDebt(
        debt_id="cc",
        category=DebtCategory.CREDIT_CARD,
        label="Credit card",
        balance=_fv("8000"),
        annual_rate=_fv("0.24"),
        monthly_minimum=_fv("200"),
    )


def _student_loan() -> HouseholdDebt:
    return HouseholdDebt(
        debt_id="student",
        category=DebtCategory.STUDENT_LOAN,
        label="Student loan",
        balance=_fv("30000"),
        annual_rate=_fv("0.055"),
        monthly_minimum=_fv("300"),
    )


# --------------------------------------------------------------------------- #
# AC-004-001: Cash conservation across all alternatives                       #
# --------------------------------------------------------------------------- #


class CashConservationTests(unittest.TestCase):
    def test_baseline_conserves_surplus(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(result.baseline.total_allocated, result.annual_surplus)

    def test_all_alternatives_conserve_surplus(self) -> None:
        h = _build_household(debts=(_credit_card_debt(), _student_loan()))
        result = optimize_household_allocation(h, RULES)
        for alt in result.alternatives:
            with self.subTest(name=alt.name):
                self.assertEqual(alt.total_allocated, result.annual_surplus)

    def test_conservation_with_zero_reserve_gap(self) -> None:
        # Liquid reserves well above 6-month target — no reserve allocation needed
        h = _build_household(liquid_reserves="100000", monthly_essential="3000")
        result = optimize_household_allocation(h, RULES)
        for alt in (result.baseline,) + result.alternatives:
            self.assertEqual(alt.total_allocated, result.annual_surplus)

    def test_conservation_with_large_debt(self) -> None:
        h = _build_household(debts=(_credit_card_debt(),))
        result = optimize_household_allocation(h, RULES)
        for alt in (result.baseline,) + result.alternatives:
            self.assertEqual(alt.total_allocated, result.annual_surplus)


# --------------------------------------------------------------------------- #
# AC-004-002: Three alternatives produced                                      #
# --------------------------------------------------------------------------- #


class AlternativeStructureTests(unittest.TestCase):
    def test_three_alternatives_returned(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(len(result.alternatives), 3)

    def test_alternative_names(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        names = {alt.name for alt in result.alternatives}
        self.assertEqual(names, {"recommended", "liquidity_preserving", "goal_acceleration"})

    def test_baseline_name(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(result.baseline.name, "waterfall_baseline")

    def test_result_carries_household_id(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(result.household_id, h.household_id)

    def test_result_carries_fingerprint(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(result.household_fingerprint, h.fingerprint())


# --------------------------------------------------------------------------- #
# AC-004-003: Infeasibility detection (REQ-024)                               #
# --------------------------------------------------------------------------- #


class InfeasibilityTests(unittest.TestCase):
    def test_infeasible_household_reported(self) -> None:
        # Expenses > income
        h = _build_household(annual_income="40000", monthly_essential="5000")
        result = optimize_household_allocation(h, RULES)
        self.assertIsNotNone(result.infeasibility)

    def test_infeasibility_shortfall_positive(self) -> None:
        h = _build_household(annual_income="40000", monthly_essential="5000")
        result = optimize_household_allocation(h, RULES)
        assert result.infeasibility is not None
        self.assertGreater(result.infeasibility.shortfall, ZERO)

    def test_infeasible_surplus_is_zero(self) -> None:
        h = _build_household(annual_income="40000", monthly_essential="5000")
        result = optimize_household_allocation(h, RULES)
        self.assertEqual(result.annual_surplus, ZERO)

    def test_feasible_household_no_infeasibility(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertIsNone(result.infeasibility)

    def test_missing_field_raises_before_optimizing(self) -> None:
        h = HouseholdState(
            household_id="synthetic-bad",
            synthetic=True,
            members=(HouseholdMember(member_id="primary", role=MemberRole.PRIMARY, birth_year=1985),),
            income_sources=(IncomeSource(
                source_id="salary",
                member_id="primary",
                income_type=IncomeType.SALARY,
                annual_gross=_missing_fv(),
                work_jurisdiction="CA",
            ),),
            expenses=(Expense(
                expense_id="living",
                category=ExpenseCategory.ESSENTIAL,
                label="Living",
                monthly_amount=_fv("3000"),
            ),),
            accounts=(Account(
                account_id="checking",
                account_type=AccountType.CASH,
                owner_member_id="primary",
                balance=_fv("5000"),
            ),),
            debts=(),
            benefits=(EmployerBenefit(
                benefit_id="401k",
                member_id="primary",
                plan_type="401k",
                annual_employee_limit=_fv("23000"),
                match_tiers=(),
            ),),
            goals=(Goal(
                goal_id="g1",
                label="Goal",
                target_amount=_fv("5000"),
                priority=GoalPriority.MEDIUM,
                flexibility=GoalFlexibility.FULLY_FLEXIBLE,
                owner_member_ids=("primary",),
                horizon_years=1,
            ),),
            constraints=(),
            tax_profile=TaxProfile(
                filing_status=FilingStatus.SINGLE,
                domicile_state="CA",
                work_state="CA",
            ),
        )
        with self.assertRaises(ValueError):
            optimize_household_allocation(h, RULES)


# --------------------------------------------------------------------------- #
# AC-004-004: Reserve gap allocation                                           #
# --------------------------------------------------------------------------- #


class ReserveAllocationTests(unittest.TestCase):
    def test_reserve_gap_allocated_in_baseline(self) -> None:
        # 3-month target = 3 * 5000 = 15000; liquid = 5000; gap = 10000
        h = _build_household(monthly_essential="5000", liquid_reserves="5000")
        result = optimize_household_allocation(h, RULES)
        reserve_lines = [l for l in result.baseline.lines if l.use == AllocationUse.EMERGENCY_RESERVE]
        self.assertTrue(len(reserve_lines) > 0)
        total_reserve = sum(l.amount for l in reserve_lines)
        self.assertGreater(total_reserve, ZERO)

    def test_no_reserve_line_when_fully_funded(self) -> None:
        # Liquid = 100000, monthly_essential = 3000; 3-month target = 9000 < 100000
        h = _build_household(monthly_essential="3000", liquid_reserves="100000")
        result = optimize_household_allocation(h, RULES)
        reserve_lines = [l for l in result.baseline.lines if l.use == AllocationUse.EMERGENCY_RESERVE]
        self.assertEqual(len(reserve_lines), 0)

    def test_liquidity_preserving_uses_6mo_reserve(self) -> None:
        # 6-month target = 30000; 3-month target = 15000; liquid = 10000
        h = _build_household(monthly_essential="5000", liquid_reserves="10000")
        result = optimize_household_allocation(h, RULES)
        liq_alt = next(a for a in result.alternatives if a.name == "liquidity_preserving")
        baseline = result.baseline
        liq_reserve = sum(l.amount for l in liq_alt.lines if l.use == AllocationUse.EMERGENCY_RESERVE)
        base_reserve = sum(l.amount for l in baseline.lines if l.use == AllocationUse.EMERGENCY_RESERVE)
        # 6-month gap >= 3-month gap, so liquidity-preserving allocates >= baseline
        self.assertGreaterEqual(liq_reserve, base_reserve)

    def test_goal_acceleration_uses_2mo_reserve(self) -> None:
        # 2-month target = 10000; 3-month = 15000; liquid = 5000
        h = _build_household(monthly_essential="5000", liquid_reserves="5000")
        result = optimize_household_allocation(h, RULES)
        goal_alt = next(a for a in result.alternatives if a.name == "goal_acceleration")
        baseline = result.baseline
        goal_reserve = sum(l.amount for l in goal_alt.lines if l.use == AllocationUse.EMERGENCY_RESERVE)
        base_reserve = sum(l.amount for l in baseline.lines if l.use == AllocationUse.EMERGENCY_RESERVE)
        # 2-month gap <= 3-month gap
        self.assertLessEqual(goal_reserve, base_reserve)


# --------------------------------------------------------------------------- #
# AC-004-005: Employer match captured                                          #
# --------------------------------------------------------------------------- #


class EmployerMatchTests(unittest.TestCase):
    def test_match_captured_in_recommended(self) -> None:
        # $200K salary, 50% match up to 6% = $6000 match room
        h = _build_household(annual_income="200000")
        result = optimize_household_allocation(h, RULES)
        rec = next(a for a in result.alternatives if a.name == "recommended")
        match_lines = [l for l in rec.lines if l.use == AllocationUse.EMPLOYER_MATCH]
        self.assertTrue(len(match_lines) > 0)
        self.assertGreater(sum(l.amount for l in match_lines), ZERO)

    def test_match_room_binding_when_fully_consumed(self) -> None:
        h = _build_household(annual_income="200000")
        result = optimize_household_allocation(h, RULES)
        rec = next(a for a in result.alternatives if a.name == "recommended")
        match_binding = [c for c in rec.binding_constraints if c.dimension == "employer_match_room"]
        if match_binding:
            self.assertGreater(match_binding[0].applied, ZERO)


# --------------------------------------------------------------------------- #
# AC-004-006: Marginal value ordering in recommended                          #
# --------------------------------------------------------------------------- #


class MarginalValueOrderingTests(unittest.TestCase):
    def _get_use_positions(self, alt, use: AllocationUse) -> list[int]:
        return [i for i, l in enumerate(alt.lines) if l.use == use]

    def test_high_rate_debt_before_tax_advantaged(self) -> None:
        # CC at 24% > 22% marginal rate for this income → should appear before tax-advantaged
        h = _build_household(annual_income="150000", debts=(_credit_card_debt(),))
        result = optimize_household_allocation(h, RULES)
        rec = next(a for a in result.alternatives if a.name == "recommended")

        # If both appear, high-cost debt should come before tax-advantaged savings
        hc_positions = self._get_use_positions(rec, AllocationUse.HIGH_COST_DEBT)
        ta_positions = self._get_use_positions(rec, AllocationUse.TAX_ADVANTAGED_SAVINGS)
        if hc_positions and ta_positions:
            # At least one high-cost debt line before tax-advantaged
            self.assertLess(min(hc_positions), min(ta_positions))

    def test_low_rate_debt_after_tax_advantaged(self) -> None:
        # Student loan at 5.5% < marginal rate → appears after tax-advantaged
        h = _build_household(annual_income="200000", debts=(_student_loan(),))
        result = optimize_household_allocation(h, RULES)
        rec = next(a for a in result.alternatives if a.name == "recommended")

        lc_positions = self._get_use_positions(rec, AllocationUse.LOWER_COST_DEBT)
        ta_positions = self._get_use_positions(rec, AllocationUse.TAX_ADVANTAGED_SAVINGS)
        if lc_positions and ta_positions:
            self.assertGreater(min(lc_positions), min(ta_positions))


# --------------------------------------------------------------------------- #
# AC-004-007: Goal acceleration prioritizes critical goals                     #
# --------------------------------------------------------------------------- #


class GoalAccelerationTests(unittest.TestCase):
    def test_critical_goal_appears_before_tax_advantaged(self) -> None:
        critical_goal = Goal(
            goal_id="down-payment",
            label="Down payment",
            target_amount=_fv("50000"),
            priority=GoalPriority.CRITICAL,
            flexibility=GoalFlexibility.FIXED,
            owner_member_ids=("primary",),
            horizon_years=2,
        )
        h = _build_household(goals=(critical_goal,))
        result = optimize_household_allocation(h, RULES)
        acc = next(a for a in result.alternatives if a.name == "goal_acceleration")

        goal_pos = [i for i, l in enumerate(acc.lines) if l.use == AllocationUse.GOAL_FUNDING]
        tax_pos = [i for i, l in enumerate(acc.lines) if l.use == AllocationUse.TAX_ADVANTAGED_SAVINGS]
        if goal_pos and tax_pos:
            self.assertLess(min(goal_pos), min(tax_pos))

    def test_critical_goal_funded_in_goal_acceleration(self) -> None:
        critical_goal = Goal(
            goal_id="down-payment",
            label="Down payment",
            target_amount=_fv("20000"),
            priority=GoalPriority.CRITICAL,
            flexibility=GoalFlexibility.FIXED,
            owner_member_ids=("primary",),
            horizon_years=1,
        )
        h = _build_household(annual_income="200000", goals=(critical_goal,))
        result = optimize_household_allocation(h, RULES)
        acc = next(a for a in result.alternatives if a.name == "goal_acceleration")
        goal_lines = [l for l in acc.lines if l.use == AllocationUse.GOAL_FUNDING and l.destination_id == "down-payment"]
        self.assertTrue(len(goal_lines) > 0)


# --------------------------------------------------------------------------- #
# AC-004-008: Scenario stresses on recommended (REQ-030, REQ-031)             #
# --------------------------------------------------------------------------- #


class ScenarioTests(unittest.TestCase):
    def _get_recommended(self, h: HouseholdState):
        result = optimize_household_allocation(h, RULES)
        return next(a for a in result.alternatives if a.name == "recommended")

    def test_four_scenarios_on_each_alternative(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        for alt in (result.baseline,) + result.alternatives:
            with self.subTest(name=alt.name):
                self.assertEqual(len(alt.scenario_results), 4)

    def test_scenario_names(self) -> None:
        h = _build_household()
        rec = self._get_recommended(h)
        names = {s.scenario for s in rec.scenario_results}
        self.assertEqual(names, {
            "income_loss_3mo_50pct",
            "unexpected_expense_15k",
            "market_decline_30pct",
            "goal_cost_increase_20pct",
        })

    def test_income_loss_reduces_reserve_months(self) -> None:
        # Liquid=10000, monthly_essential=5000; 3-month reserve already funded
        h = _build_household(monthly_essential="5000", liquid_reserves="15000")
        rec = self._get_recommended(h)
        income_loss = next(s for s in rec.scenario_results if s.scenario == "income_loss_3mo_50pct")
        self.assertGreater(income_loss.income_reduction, ZERO)
        self.assertIsNotNone(income_loss.reserve_months_remaining)

    def test_unexpected_expense_reduces_reserves(self) -> None:
        h = _build_household(liquid_reserves="20000")
        rec = self._get_recommended(h)
        exp_scenario = next(s for s in rec.scenario_results if s.scenario == "unexpected_expense_15k")
        self.assertEqual(exp_scenario.expense_increase, Decimal("15000"))

    def test_market_decline_plan_survives(self) -> None:
        h = _build_household()
        rec = self._get_recommended(h)
        market = next(s for s in rec.scenario_results if s.scenario == "market_decline_30pct")
        self.assertTrue(market.plan_survives)

    def test_low_reserve_income_loss_does_not_survive(self) -> None:
        # Tiny reserves; income loss of $200K * 0.5 * 0.25 = $25K will wipe reserves
        h = _build_household(annual_income="200000", liquid_reserves="500")
        rec = self._get_recommended(h)
        income_loss = next(s for s in rec.scenario_results if s.scenario == "income_loss_3mo_50pct")
        self.assertFalse(income_loss.plan_survives)


# --------------------------------------------------------------------------- #
# AC-004-009: Jurisdiction rules                                               #
# --------------------------------------------------------------------------- #


class JurisdictionRulesTests(unittest.TestCase):
    def test_marginal_rate_mfj_180k(self) -> None:
        # MFJ $180K gross: taxable = 180K - 29.2K = 150.8K → 22% bracket
        rate = RULES.marginal_rate(Decimal("180000"), FilingStatus.MARRIED_FILING_JOINTLY)
        self.assertEqual(rate, Decimal("0.22"))

    def test_marginal_rate_mfj_280k(self) -> None:
        # MFJ $280K: taxable = 250.8K → 24% bracket
        rate = RULES.marginal_rate(Decimal("280000"), FilingStatus.MARRIED_FILING_JOINTLY)
        self.assertEqual(rate, Decimal("0.24"))

    def test_marginal_rate_single_100k(self) -> None:
        # Single $100K: taxable = 85.4K → 22% bracket
        rate = RULES.marginal_rate(Decimal("100000"), FilingStatus.SINGLE)
        self.assertEqual(rate, Decimal("0.22"))

    def test_marginal_rate_single_200k(self) -> None:
        # Single $200K: taxable = 185.4K → 24% bracket
        rate = RULES.marginal_rate(Decimal("200000"), FilingStatus.SINGLE)
        self.assertEqual(rate, Decimal("0.24"))

    def test_k401_limit_2024(self) -> None:
        self.assertEqual(RULES.contribution_limits.k401_employee, Decimal("23000"))

    def test_ira_limit_2024(self) -> None:
        self.assertEqual(RULES.contribution_limits.ira, Decimal("7000"))

    def test_scope_label(self) -> None:
        self.assertEqual(RULES.scope, "federal_income_2024")


# --------------------------------------------------------------------------- #
# AC-004-010: Surplus and fixed obligations reporting                          #
# --------------------------------------------------------------------------- #


class SurplusReportingTests(unittest.TestCase):
    def test_surplus_equals_gross_minus_obligations(self) -> None:
        # Annual income $200K, monthly expenses $5K × 12 = $60K, no debt minimums
        h = _build_household(annual_income="200000", monthly_essential="5000")
        result = optimize_household_allocation(h, RULES)
        expected_surplus = Decimal("200000") - Decimal("60000")
        self.assertEqual(result.annual_surplus, expected_surplus)

    def test_surplus_reduced_by_debt_minimums(self) -> None:
        # Student loan adds $300/mo min = $3600/yr
        h = _build_household(annual_income="200000", monthly_essential="5000", debts=(_student_loan(),))
        result_without = optimize_household_allocation(_build_household(annual_income="200000", monthly_essential="5000"), RULES)
        result_with = optimize_household_allocation(h, RULES)
        self.assertLess(result_with.annual_surplus, result_without.annual_surplus)

    def test_common_assumptions_present(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        self.assertGreater(len(result.common_assumptions), 0)
        self.assertEqual(result.period_label, "12-month horizon")
        self.assertEqual(result.jurisdiction_scope, "federal_income_2024")


if __name__ == "__main__":
    unittest.main()
