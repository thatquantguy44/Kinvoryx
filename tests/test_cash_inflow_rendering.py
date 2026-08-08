"""Slice C rendering and manual-entry tests for Spec 011."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.cash_inflow import Debt, HouseholdCase, build_decision_brief
from kinvoryx.cash_inflow_interface import parse_debt_rows, parse_manual_entry, render_result_from_manual_entry
from kinvoryx.cash_inflow_rendering import (
    BriefRenderContext,
    render_household_html,
    render_household_markdown,
    render_reviewer_html,
    render_reviewer_markdown,
)
from kinvoryx.cash_inflow_validation import golden_case_fixtures, validate_golden_case


class CashInflowRenderingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = golden_case_fixtures()[0]
        self.evidence = validate_golden_case(self.fixture)
        self.context = BriefRenderContext(
            household=self.fixture.household,
            brief=self.evidence.brief,
            validation_evidence=self.evidence,
            reviewer_annotations=self.fixture.reviewer_annotations,
        )

    def test_ac_cib_010_household_artifact_includes_comparison_and_boundary(self) -> None:
        markdown = render_household_markdown(self.context)

        self.assertIn("Synthetic decision-support prototype only", markdown)
        self.assertIn("Transparent waterfall baseline", markdown)
        self.assertIn("Safety first", markdown)
        self.assertIn("Debt acceleration", markdown)
        self.assertIn("Interest avoided", markdown)
        self.assertIn("Scenario Summaries", markdown)
        self.assertNotIn("Recommended plan", markdown)
        self.assertNotIn("Selected plan", markdown)

    def test_ac_cib_011_reviewer_record_includes_evidence_annotations_and_trace_ids(self) -> None:
        markdown = render_reviewer_markdown(self.context)

        self.assertIn("Validation passed: yes", markdown)
        self.assertIn("Pilot ready: yes", markdown)
        self.assertIn("rvw-bonus-001", markdown)
        self.assertIn("REQ-CIB-018", markdown)
        self.assertIn("REQ-CIB-014", markdown)
        self.assertIn("Supported Debts", markdown)

    def test_ac_cib_012_manual_entry_accepts_valid_synthetic_inputs_and_debts(self) -> None:
        result = parse_manual_entry(
            {
                "case_id": ["manual-valid"],
                "cash_inflow": ["20000"],
                "monthly_essential_expenses": ["5000"],
                "liquid_reserves": ["5000"],
                "debts": ["credit_card,6000,0.24\nstudent_loan,12000,0.055"],
                "employer_match_contribution_room": ["6000"],
                "employer_match_rate": ["0.50"],
                "tax_advantaged_contribution_room": ["7000"],
                "estimated_marginal_tax_rate": ["0.24"],
                "near_term_goal_remaining": ["15000"],
            }
        )

        self.assertEqual(result.errors, ())
        self.assertIsNotNone(result.household)
        self.assertEqual(len(result.household.debts), 2)
        self.assertEqual(len(build_decision_brief(result.household).alternatives), 7)

    def test_ac_cib_012_manual_entry_rejects_invalid_supported_debt_rows(self) -> None:
        result = parse_manual_entry({"case_id": ["manual-invalid"], "debts": ["credit_card,6000"]})

        self.assertIsNone(result.household)
        self.assertTrue(result.errors)
        self.assertIn("debts:", result.errors[0])

    def test_ac_cib_012_result_renderer_returns_error_without_brief_for_bad_form(self) -> None:
        status, html = render_result_from_manual_entry({"case_id": [""], "debts": ["bad,row"]})

        self.assertEqual(status, 400)
        self.assertIn("Submission Errors", html)
        self.assertNotIn("Comparable Alternatives</h2><div", html)

    def test_ac_cib_013_markdown_and_html_exports_preserve_calculation_values(self) -> None:
        markdown = render_household_markdown(self.context)
        html = render_household_html(self.context)

        self.assertIn("$20,000.00", markdown)
        self.assertIn("$20,000.00", html)
        self.assertIn("$6,000.00", markdown)
        self.assertIn("$6,000.00", html)

    def test_ac_cib_013_reviewer_html_escapes_user_supplied_case_identifiers(self) -> None:
        household = HouseholdCase(
            case_id="<script>alert(1)</script>",
            cash_inflow="1000",
            monthly_essential_expenses="1000",
            liquid_reserves="1000",
            debts=(Debt("card", "100", "0.2"),),
            employer_match_contribution_room="0",
            employer_match_rate="0",
            tax_advantaged_contribution_room="0",
            estimated_marginal_tax_rate="0",
            near_term_goal_remaining="0",
        )
        context = BriefRenderContext(household, build_decision_brief(household))

        html = render_reviewer_html(context)

        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_ac_cib_012_debt_parser_accepts_blank_lines(self) -> None:
        debts = parse_debt_rows("\ncredit_card,6000,0.24\n\n")

        self.assertEqual(len(debts), 1)
        self.assertEqual(debts[0].identifier, "credit_card")


if __name__ == "__main__":
    unittest.main()
