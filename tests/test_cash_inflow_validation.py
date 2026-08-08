"""Slice B validation harness tests for Spec 011."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.cash_inflow import Strategy, build_decision_brief
from kinvoryx.cash_inflow_validation import (
    ReviewerAnnotation,
    golden_case_fixtures,
    property_sweep_cases,
    unresolved_pilot_blockers,
    validate_all_golden_cases,
    validate_reviewer_annotations,
)


class CashInflowValidationHarnessTests(unittest.TestCase):
    def test_ac_cib_006_golden_case_suite_covers_required_household_shapes(self) -> None:
        fixtures = golden_case_fixtures()

        self.assertEqual(len(fixtures), 8)
        self.assertEqual(
            {fixture.fixture_id for fixture in fixtures},
            {
                "bonus-full-tradeoff",
                "no-supported-debt",
                "underfunded-emergency-reserve",
                "already-funded-reserve",
                "employer-match-capped",
                "tax-room-exhausted",
                "goal-larger-than-inflow",
                "oversized-inflow",
            },
        )
        for fixture in fixtures:
            self.assertTrue(fixture.purpose, "REQ-CIB-011 fixture purpose is required")
            self.assertTrue(fixture.household.synthetic, "REQ-CIB-011 fixtures must be synthetic")

    def test_ac_cib_006_golden_case_suite_passes_validation_harness(self) -> None:
        evidence = validate_all_golden_cases()

        failures = {
            result.fixture_id: [issue.message for issue in result.issues]
            for result in evidence
            if not result.passed
        }

        self.assertFalse(failures, f"REQ-CIB-012 validation failures: {failures}")
        self.assertTrue(all(result.pilot_ready for result in evidence))

    def test_ac_cib_005_golden_cases_prove_material_strategy_differentiation(self) -> None:
        full_tradeoff = {
            fixture.fixture_id: fixture for fixture in golden_case_fixtures()
        }["bonus-full-tradeoff"]
        plans = {
            plan.strategy: plan for plan in build_decision_brief(full_tradeoff.household).alternatives
        }

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

    def test_ac_cib_007_property_sweep_preserves_invariants_across_edge_cases(self) -> None:
        for household in property_sweep_cases():
            with self.subTest(case_id=household.case_id):
                brief = build_decision_brief(household)
                plans = (brief.baseline,) + brief.alternatives

                for plan in plans:
                    self.assertEqual(plan.allocated_total, household.cash_inflow)
                    self.assertLessEqual(
                        plan.allocations["employer_match_contribution"],
                        household.employer_match_contribution_room,
                    )
                    self.assertLessEqual(
                        plan.allocations["tax_advantaged_savings"],
                        household.tax_advantaged_contribution_room,
                    )
                    self.assertLessEqual(
                        plan.allocations["near_term_goal"],
                        household.near_term_goal_remaining,
                    )
                    debt_balance = sum((debt.balance for debt in household.debts), start=household.cash_inflow * 0)
                    self.assertLessEqual(plan.allocations["debt_paydown"], debt_balance)
                    self.assertEqual(
                        {scenario.name for scenario in plan.scenarios},
                        {"job_loss", "unexpected_expense", "market_decline", "goal_cost_increase"},
                    )

    def test_ac_cib_008_reviewer_annotations_validate_required_traceable_fields(self) -> None:
        annotation = ReviewerAnnotation(
            annotation_id="rvw-test-001",
            case_id="case-1",
            strategy=Strategy.SAFETY_FIRST.value,
            reviewer_role="risk-reviewer",
            category="risk",
            severity="medium",
            note="Traceable concern about assumption disclosure.",
            trace_ids=("REQ-CIB-014", "AC-CIB-008"),
            disposition="accepted",
        )

        issues = validate_reviewer_annotations(
            (annotation,),
            valid_case_ids=("case-1",),
            valid_strategies=(Strategy.SAFETY_FIRST.value,),
        )

        self.assertEqual(issues, ())

    def test_ac_cib_008_malformed_reviewer_annotations_are_rejected(self) -> None:
        annotation = ReviewerAnnotation(
            annotation_id="",
            case_id="unknown-case",
            strategy="unknown-strategy",
            reviewer_role="",
            category="narrative",
            severity="urgent",
            note="",
            trace_ids=("FEAT-016",),
            disposition="waiting",
        )

        issues = validate_reviewer_annotations(
            (annotation,),
            valid_case_ids=("case-1",),
            valid_strategies=(Strategy.SAFETY_FIRST.value,),
        )

        self.assertGreaterEqual(len(issues), 8)
        self.assertIn("annotation_id", {issue.code for issue in issues})
        self.assertIn("annotation_trace_ids", {issue.code for issue in issues})

    def test_ac_cib_008_open_high_severity_annotations_block_pilot_readiness(self) -> None:
        open_blocker = ReviewerAnnotation(
            annotation_id="rvw-blocker-001",
            case_id="case-1",
            reviewer_role="compliance-reviewer",
            category="compliance",
            severity="blocker",
            note="Pilot language requires review before real-household use.",
            trace_ids=("REQ-CIB-015", "AC-CIB-008"),
            disposition="open",
        )
        resolved_high = ReviewerAnnotation(
            annotation_id="rvw-high-001",
            case_id="case-1",
            reviewer_role="risk-reviewer",
            category="risk",
            severity="high",
            note="Resolved copy concern.",
            trace_ids=("REQ-CIB-015", "AC-CIB-008"),
            disposition="resolved",
        )

        blockers = unresolved_pilot_blockers((open_blocker, resolved_high))

        self.assertEqual(blockers, (open_blocker,))


if __name__ == "__main__":
    unittest.main()
