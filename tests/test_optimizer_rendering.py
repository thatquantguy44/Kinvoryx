"""Acceptance tests for the Spec 004 optimizer rendering layer."""

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
from kinvoryx.optimizer_rendering import (
    OptimizerRenderContext,
    render_household_markdown,
    render_reviewer_markdown,
    render_household_html,
    render_reviewer_html,
    render_combined_html,
    SAFETY_DISCLOSURE,
)

RULES = federal_rules_2024()
ZERO = Decimal("0")


# --------------------------------------------------------------------------- #
# Fixture helpers (mirrored from test_capital_allocation_optimizer.py)        #
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


def _build_household(
    annual_income: str = "200000",
    monthly_essential: str = "5000",
    liquid_reserves: str = "10000",
    debts: tuple = (),
    benefits: tuple = (),
    goals: tuple = (),
    filing_status: FilingStatus = FilingStatus.MARRIED_FILING_JOINTLY,
) -> HouseholdState:
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
        household_id="synthetic-render-001",
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


def _make_ctx(
    annual_income: str = "200000",
    monthly_essential: str = "5000",
    liquid_reserves: str = "10000",
    debts: tuple = (),
) -> OptimizerRenderContext:
    h = _build_household(
        annual_income=annual_income,
        monthly_essential=monthly_essential,
        liquid_reserves=liquid_reserves,
        debts=debts,
    )
    result = optimize_household_allocation(h, RULES)
    return OptimizerRenderContext(household=h, result=result)


# --------------------------------------------------------------------------- #
# OptimizerRenderContext construction                                          #
# --------------------------------------------------------------------------- #


class RenderContextTests(unittest.TestCase):
    def test_context_stores_household_and_result(self) -> None:
        h = _build_household()
        result = optimize_household_allocation(h, RULES)
        ctx = OptimizerRenderContext(household=h, result=result)
        self.assertIs(ctx.household, h)
        self.assertIs(ctx.result, result)

    def test_context_is_frozen(self) -> None:
        ctx = _make_ctx()
        with self.assertRaises((AttributeError, TypeError)):
            ctx.household = None  # type: ignore[misc]


# --------------------------------------------------------------------------- #
# Markdown — household view                                                    #
# --------------------------------------------------------------------------- #


class HouseholdMarkdownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx()
        self.md = render_household_markdown(self.ctx)

    def test_returns_string(self) -> None:
        self.assertIsInstance(self.md, str)

    def test_ends_with_newline(self) -> None:
        self.assertTrue(self.md.endswith("\n"))

    def test_contains_safety_disclosure(self) -> None:
        self.assertIn(SAFETY_DISCLOSURE, self.md)

    def test_contains_household_id(self) -> None:
        self.assertIn(self.ctx.result.household_id, self.md)

    def test_contains_jurisdiction_scope(self) -> None:
        self.assertIn(self.ctx.result.jurisdiction_scope, self.md)

    def test_contains_period_label(self) -> None:
        self.assertIn(self.ctx.result.period_label, self.md)

    def test_contains_comparison_table(self) -> None:
        self.assertIn("Comparable Alternatives", self.md)
        self.assertIn("Alternative", self.md)

    def test_contains_recommended_detail(self) -> None:
        self.assertIn("Allocation Detail", self.md)

    def test_contains_scenario_section(self) -> None:
        self.assertIn("Scenario Results", self.md)
        self.assertIn("Survives", self.md)

    def test_contains_common_assumptions(self) -> None:
        self.assertIn("Common Assumptions", self.md)
        for a in self.ctx.result.common_assumptions:
            self.assertIn(a, self.md)

    def test_snapshot_shows_annual_surplus(self) -> None:
        surplus = f"${self.ctx.result.annual_surplus:,.2f}"
        self.assertIn(surplus, self.md)

    def test_all_four_use_labels_appear(self) -> None:
        for label in ("Emergency reserve", "Tax-advantaged savings", "Discretionary buffer"):
            self.assertIn(label, self.md)

    def test_no_reviewer_fingerprint_in_household_view(self) -> None:
        self.assertNotIn("fingerprint", self.md.lower())

    def test_no_income_source_detail_in_household_view(self) -> None:
        self.assertNotIn("Income Sources", self.md)


class HouseholdMarkdownWithDebtTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx(debts=(_credit_card_debt(), _student_loan()))
        self.md = render_household_markdown(self.ctx)

    def test_cash_amounts_formatted_as_dollars(self) -> None:
        self.assertIn("$", self.md)

    def test_document_is_non_empty(self) -> None:
        self.assertGreater(len(self.md.strip()), 200)


# --------------------------------------------------------------------------- #
# Markdown — infeasibility branch                                              #
# --------------------------------------------------------------------------- #


class HouseholdMarkdownInfeasibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        # Income far below fixed obligations — triggers infeasibility
        self.ctx = _make_ctx(annual_income="10000", monthly_essential="5000")
        self.md = render_household_markdown(self.ctx)

    def test_infeasibility_section_present(self) -> None:
        self.assertIn("Infeasibility", self.md)

    def test_diagnosis_present(self) -> None:
        self.assertIn(self.ctx.result.infeasibility.diagnosis, self.md)

    def test_comparison_table_absent(self) -> None:
        self.assertNotIn("Comparable Alternatives", self.md)

    def test_shortfall_figures_present(self) -> None:
        shortfall = f"${self.ctx.result.infeasibility.shortfall:,.2f}"
        self.assertIn(shortfall, self.md)


# --------------------------------------------------------------------------- #
# Markdown — reviewer view                                                     #
# --------------------------------------------------------------------------- #


class ReviewerMarkdownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx(debts=(_credit_card_debt(),))
        self.md = render_reviewer_markdown(self.ctx)

    def test_returns_string(self) -> None:
        self.assertIsInstance(self.md, str)

    def test_ends_with_newline(self) -> None:
        self.assertTrue(self.md.endswith("\n"))

    def test_contains_household_fingerprint(self) -> None:
        self.assertIn(self.ctx.result.household_fingerprint, self.md)

    def test_contains_income_sources_section(self) -> None:
        self.assertIn("Income Sources", self.md)
        self.assertIn("salary", self.md)

    def test_contains_debts_section(self) -> None:
        self.assertIn("Debts", self.md)
        self.assertIn("Credit card", self.md)

    def test_all_alternatives_present(self) -> None:
        for alt in self.ctx.result.alternatives:
            self.assertIn(alt.label, self.md)

    def test_baseline_present(self) -> None:
        self.assertIn(self.ctx.result.baseline.label, self.md)

    def test_all_alternatives_have_scenario_table(self) -> None:
        self.assertGreaterEqual(self.md.count("Scenarios"), 3)

    def test_trade_off_summaries_present(self) -> None:
        for alt in (self.ctx.result.baseline,) + self.ctx.result.alternatives:
            self.assertIn(alt.trade_off_summary, self.md)

    def test_safety_disclosure_present(self) -> None:
        self.assertIn(SAFETY_DISCLOSURE, self.md)


class ReviewerMarkdownNoDebtTests(unittest.TestCase):
    def test_no_debt_message(self) -> None:
        ctx = _make_ctx()
        md = render_reviewer_markdown(ctx)
        self.assertIn("No debts declared", md)


class ReviewerMarkdownInfeasibilityTests(unittest.TestCase):
    def test_infeasibility_shown_in_reviewer_view(self) -> None:
        ctx = _make_ctx(annual_income="10000", monthly_essential="5000")
        md = render_reviewer_markdown(ctx)
        self.assertIn("Infeasibility", md)
        self.assertIn(ctx.result.infeasibility.diagnosis, md)


# --------------------------------------------------------------------------- #
# HTML — household view                                                        #
# --------------------------------------------------------------------------- #


class HouseholdHTMLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx()
        self.html = render_household_html(self.ctx)

    def test_returns_string(self) -> None:
        self.assertIsInstance(self.html, str)

    def test_valid_html_structure(self) -> None:
        self.assertIn("<!doctype html>", self.html.lower())
        self.assertIn("<html", self.html)
        self.assertIn("</html>", self.html)
        self.assertIn("<body", self.html)
        self.assertIn("</body>", self.html)

    def test_contains_title_tag(self) -> None:
        self.assertIn("<title>", self.html)
        self.assertIn(self.ctx.result.household_id, self.html)

    def test_contains_comparison_table(self) -> None:
        self.assertIn("<table>", self.html)
        self.assertIn("Comparable Alternatives", self.html)

    def test_contains_scenario_table(self) -> None:
        self.assertIn("Scenario Results", self.html)
        self.assertIn("Survives", self.html)

    def test_safety_disclosure_present(self) -> None:
        self.assertIn(SAFETY_DISCLOSURE, self.html)

    def test_inline_css_present(self) -> None:
        self.assertIn("<style>", self.html)
        self.assertIn("--ink:", self.html)

    def test_no_fingerprint_in_household_html(self) -> None:
        self.assertNotIn("Fingerprint", self.html)

    def test_num_class_on_monetary_cells(self) -> None:
        self.assertIn('class="num"', self.html)


class HouseholdHTMLInfeasibilityTests(unittest.TestCase):
    def test_warn_box_shown_when_infeasible(self) -> None:
        ctx = _make_ctx(annual_income="10000", monthly_essential="5000")
        html = render_household_html(ctx)
        self.assertIn("warn-box", html)
        self.assertIn(ctx.result.infeasibility.diagnosis, html)

    def test_comparison_table_absent_when_infeasible(self) -> None:
        ctx = _make_ctx(annual_income="10000", monthly_essential="5000")
        html = render_household_html(ctx)
        self.assertNotIn("Comparable Alternatives", html)


# --------------------------------------------------------------------------- #
# HTML — reviewer view                                                         #
# --------------------------------------------------------------------------- #


class ReviewerHTMLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx(debts=(_credit_card_debt(),))
        self.html = render_reviewer_html(self.ctx)

    def test_returns_string(self) -> None:
        self.assertIsInstance(self.html, str)

    def test_valid_html_structure(self) -> None:
        self.assertIn("<!doctype html>", self.html.lower())
        self.assertIn("</html>", self.html)

    def test_fingerprint_present(self) -> None:
        self.assertIn(self.ctx.result.household_fingerprint, self.html)

    def test_income_table_present(self) -> None:
        self.assertIn("Income Sources", self.html)
        self.assertIn("salary", self.html)

    def test_debt_table_present(self) -> None:
        self.assertIn("Debts", self.html)
        self.assertIn("Credit card", self.html)

    def test_all_alternatives_present(self) -> None:
        for alt in self.ctx.result.alternatives:
            self.assertIn(alt.label, self.html)

    def test_reviewer_css_class_present(self) -> None:
        self.assertIn("reviewer", self.html)


class ReviewerHTMLNoDebtTests(unittest.TestCase):
    def test_no_debt_message_in_html(self) -> None:
        ctx = _make_ctx()
        html = render_reviewer_html(ctx)
        self.assertIn("No debts declared.", html)


# --------------------------------------------------------------------------- #
# HTML — combined view                                                         #
# --------------------------------------------------------------------------- #


class CombinedHTMLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx(debts=(_credit_card_debt(), _student_loan()))
        self.html = render_combined_html(self.ctx)

    def test_returns_string(self) -> None:
        self.assertIsInstance(self.html, str)

    def test_single_doctype(self) -> None:
        self.assertEqual(self.html.lower().count("<!doctype html>"), 1)

    def test_single_style_block(self) -> None:
        self.assertEqual(self.html.count("<style>"), 1)

    def test_household_content_present(self) -> None:
        self.assertIn("Capital Allocation Decision Brief", self.html)

    def test_reviewer_content_present(self) -> None:
        self.assertIn("Reviewer Record", self.html)

    def test_fingerprint_present(self) -> None:
        self.assertIn(self.ctx.result.household_fingerprint, self.html)

    def test_income_table_present(self) -> None:
        self.assertIn("Income Sources", self.html)

    def test_all_alternative_labels_present(self) -> None:
        for alt in self.ctx.result.alternatives:
            self.assertIn(alt.label, self.html)

    def test_comparison_table_present(self) -> None:
        self.assertIn("Comparable Alternatives", self.html)


# --------------------------------------------------------------------------- #
# Content correctness — money formatting                                       #
# --------------------------------------------------------------------------- #


class MoneyFormattingTests(unittest.TestCase):
    def test_annual_surplus_formatted_correctly(self) -> None:
        ctx = _make_ctx(annual_income="200000", monthly_essential="5000")
        md = render_household_markdown(ctx)
        surplus = ctx.result.annual_surplus
        formatted = f"${surplus:,.2f}"
        self.assertIn(formatted, md)

    def test_total_allocated_equals_surplus_in_md_table(self) -> None:
        ctx = _make_ctx()
        md = render_household_markdown(ctx)
        surplus_str = f"${ctx.result.annual_surplus:,.2f}"
        self.assertIn(surplus_str, md)

    def test_zero_debt_shows_zero_amounts(self) -> None:
        ctx = _make_ctx()
        md = render_household_markdown(ctx)
        # Should not reference debt labels
        self.assertNotIn("Credit card", md)

    def test_debt_amounts_appear_in_reviewer_md(self) -> None:
        ctx = _make_ctx(debts=(_credit_card_debt(),))
        md = render_reviewer_markdown(ctx)
        # Credit card balance $8,000 should appear
        self.assertIn("8,000.00", md)


# --------------------------------------------------------------------------- #
# Content correctness — all scenarios rendered                                 #
# --------------------------------------------------------------------------- #


class ScenarioRenderingTests(unittest.TestCase):
    def test_household_md_has_four_scenario_rows(self) -> None:
        ctx = _make_ctx()
        md = render_household_markdown(ctx)
        # Count "yes" or "NO" occurrences as proxy for scenario rows
        rec = ctx.result.baseline
        for alt in ctx.result.alternatives:
            if alt.name == "recommended":
                rec = alt
                break
        self.assertEqual(len(rec.scenario_results), 4)

    def test_reviewer_md_all_alts_have_scenario_tables(self) -> None:
        ctx = _make_ctx()
        md = render_reviewer_markdown(ctx)
        all_alts = (ctx.result.baseline,) + ctx.result.alternatives
        for alt in all_alts:
            for scenario in alt.scenario_results:
                self.assertIn(scenario.scenario, md)

    def test_survives_label_present(self) -> None:
        ctx = _make_ctx()
        md = render_household_markdown(ctx)
        self.assertIn("Survives", md)


# --------------------------------------------------------------------------- #
# Idempotency — calling render twice returns the same output                  #
# --------------------------------------------------------------------------- #


class IdempotencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = _make_ctx(debts=(_credit_card_debt(),))

    def test_household_markdown_idempotent(self) -> None:
        self.assertEqual(
            render_household_markdown(self.ctx),
            render_household_markdown(self.ctx),
        )

    def test_reviewer_markdown_idempotent(self) -> None:
        self.assertEqual(
            render_reviewer_markdown(self.ctx),
            render_reviewer_markdown(self.ctx),
        )

    def test_household_html_idempotent(self) -> None:
        self.assertEqual(
            render_household_html(self.ctx),
            render_household_html(self.ctx),
        )

    def test_combined_html_idempotent(self) -> None:
        self.assertEqual(
            render_combined_html(self.ctx),
            render_combined_html(self.ctx),
        )


if __name__ == "__main__":
    unittest.main()
