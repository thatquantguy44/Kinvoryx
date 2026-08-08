"""Acceptance tests for the synthetic Spec 011 vertical slice."""

from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.cash_inflow import Debt, HouseholdCase, Strategy, build_decision_brief


class CashInflowDecisionBriefTests(unittest.TestCase):
    def setUp(self) -> None:
        self.household = HouseholdCase(
            case_id="synthetic-test-case",
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
        )

    def test_ac_cib_002_generates_all_required_alternatives_and_baseline(self) -> None:
        brief = build_decision_brief(self.household)

        self.assertEqual(brief.baseline.strategy, "waterfall_baseline")
        self.assertEqual(len(brief.alternatives), 7)
        self.assertEqual(
            {plan.strategy for plan in brief.alternatives},
            {strategy.value for strategy in Strategy},
        )

    def test_ac_cib_003_every_plan_conserves_inflow_and_respects_capacity(self) -> None:
        brief = build_decision_brief(self.household)
        plans = (brief.baseline,) + brief.alternatives

        for plan in plans:
            self.assertEqual(plan.allocated_total, self.household.cash_inflow)
            self.assertLessEqual(plan.allocations["employer_match_contribution"], Decimal("6000"))
            self.assertLessEqual(plan.allocations["tax_advantaged_savings"], Decimal("7000"))
            self.assertLessEqual(plan.allocations["near_term_goal"], Decimal("15000"))
            self.assertLessEqual(plan.allocations["debt_paydown"], Decimal("18000"))

    def test_ac_cib_005_alternatives_produce_material_tradeoffs(self) -> None:
        plans = {plan.strategy: plan for plan in build_decision_brief(self.household).alternatives}

        self.assertGreater(
            plans[Strategy.RESILIENCE.value].metrics.liquidity_months,
            plans[Strategy.DEBT_ACCELERATION.value].metrics.liquidity_months,
        )
        self.assertGreater(
            plans[Strategy.DEBT_ACCELERATION.value].metrics.estimated_first_year_interest_avoided,
            plans[Strategy.RESILIENCE.value].metrics.estimated_first_year_interest_avoided,
        )
        self.assertGreater(
            plans[Strategy.TAX_ADVANTAGED_FIRST.value].metrics.estimated_tax_value,
            plans[Strategy.MATCH_AND_DEBT_FIRST.value].metrics.estimated_tax_value,
        )
        self.assertGreater(
            plans[Strategy.NEAR_TERM_GOAL_FIRST.value].metrics.near_term_goal_funded,
            plans[Strategy.SAFETY_FIRST.value].metrics.near_term_goal_funded,
        )

    def test_ac_cib_004_scenarios_and_tradeoffs_are_present_for_every_alternative(self) -> None:
        for plan in build_decision_brief(self.household).alternatives:
            self.assertGreaterEqual(len(plan.tradeoffs), 3)
            self.assertEqual(
                {scenario.name for scenario in plan.scenarios},
                {"job_loss", "unexpected_expense", "market_decline", "goal_cost_increase"},
            )

    def test_ac_cib_001_non_synthetic_cases_are_rejected(self) -> None:
        household = HouseholdCase(
            case_id="not-allowed",
            cash_inflow="1000",
            monthly_essential_expenses="1000",
            liquid_reserves="1000",
            debts=(),
            employer_match_contribution_room="0",
            employer_match_rate="0",
            tax_advantaged_contribution_room="0",
            estimated_marginal_tax_rate="0",
            near_term_goal_remaining="0",
            synthetic=False,
        )

        with self.assertRaisesRegex(ValueError, "synthetic"):
            build_decision_brief(household)

    def test_ac_cib_006_case_without_supported_debt_still_generates_a_brief(self) -> None:
        household = HouseholdCase(
            case_id="no-debt-case",
            cash_inflow="1000",
            monthly_essential_expenses="1000",
            liquid_reserves="1000",
            debts=(),
            employer_match_contribution_room="0",
            employer_match_rate="0",
            tax_advantaged_contribution_room="0",
            estimated_marginal_tax_rate="0",
            near_term_goal_remaining="0",
        )

        brief = build_decision_brief(household)

        self.assertEqual(brief.baseline.metrics.supported_debt_remaining, Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()
