"""Export optimizer household and reviewer artifacts for the synthetic Spec 004 demo.

Usage:
    python examples/demo/optimizer_decision_brief.py          # prints to stdout
    python examples/demo/optimizer_decision_brief.py --save   # writes .md / .html files
"""

from __future__ import annotations

import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

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
from kinvoryx.capital_allocation_optimizer import optimize_household_allocation
from kinvoryx.optimizer_rendering import (
    OptimizerRenderContext,
    render_household_markdown,
    render_reviewer_markdown,
    render_household_html,
    render_reviewer_html,
    render_combined_html,
)


def _fv(amount: str) -> FieldValue:
    return FieldValue(
        value=Decimal(amount),
        provenance=DataProvenance.USER_ENTERED,
        information_class=InformationClass.HOUSEHOLD_CONFIG,
        source="demo",
        effective_date=date(2024, 1, 1),
        freshness=Freshness.CURRENT,
        owner="primary",
    )


def _demo_household() -> HouseholdState:
    """
    Synthetic household: dual-income couple, variable RSU comp, student loan,
    credit card, and competing goals — archetypal GATE-M3 research subject.
    """
    return HouseholdState(
        household_id="synthetic-hcao-demo-001",
        synthetic=True,
        members=(
            HouseholdMember(member_id="primary",   role=MemberRole.PRIMARY,   birth_year=1987),
            HouseholdMember(member_id="secondary",  role=MemberRole.PARTNER,    birth_year=1989),
        ),
        income_sources=(
            IncomeSource(
                source_id="salary-primary",
                member_id="primary",
                income_type=IncomeType.SALARY,
                annual_gross=_fv("180000"),
                work_jurisdiction="CA",
            ),
            IncomeSource(
                source_id="rsu-primary",
                member_id="primary",
                income_type=IncomeType.EQUITY_VESTING,
                annual_gross=_fv("60000"),
                work_jurisdiction="CA",
            ),
            IncomeSource(
                source_id="salary-secondary",
                member_id="secondary",
                income_type=IncomeType.SALARY,
                annual_gross=_fv("95000"),
                work_jurisdiction="CA",
            ),
        ),
        expenses=(
            Expense(
                expense_id="housing",
                category=ExpenseCategory.ESSENTIAL,
                label="Rent + utilities",
                monthly_amount=_fv("4200"),
            ),
            Expense(
                expense_id="childcare",
                category=ExpenseCategory.ESSENTIAL,
                label="Childcare",
                monthly_amount=_fv("2500"),
            ),
            Expense(
                expense_id="groceries",
                category=ExpenseCategory.ESSENTIAL,
                label="Groceries & household",
                monthly_amount=_fv("1100"),
            ),
            Expense(
                expense_id="transport",
                category=ExpenseCategory.ESSENTIAL,
                label="Transportation",
                monthly_amount=_fv("600"),
            ),
            Expense(
                expense_id="insurance",
                category=ExpenseCategory.ESSENTIAL,
                label="Health & life insurance",
                monthly_amount=_fv("400"),
            ),
        ),
        accounts=(
            Account(
                account_id="checking",
                account_type=AccountType.CASH,
                owner_member_id="primary",
                balance=_fv("18000"),
            ),
            Account(
                account_id="brokerage",
                account_type=AccountType.TAXABLE_BROKERAGE,
                owner_member_id="primary",
                balance=_fv("45000"),
            ),
            Account(
                account_id="401k-primary",
                account_type=AccountType.TRADITIONAL_401K,
                owner_member_id="primary",
                balance=_fv("120000"),
            ),
            Account(
                account_id="401k-secondary",
                account_type=AccountType.TRADITIONAL_401K,
                owner_member_id="secondary",
                balance=_fv("55000"),
            ),
        ),
        debts=(
            HouseholdDebt(
                debt_id="student-primary",
                category=DebtCategory.STUDENT_LOAN,
                label="Federal student loan (primary)",
                balance=_fv("42000"),
                annual_rate=_fv("0.065"),
                monthly_minimum=_fv("480"),
            ),
            HouseholdDebt(
                debt_id="student-secondary",
                category=DebtCategory.STUDENT_LOAN,
                label="Federal student loan (secondary)",
                balance=_fv("28000"),
                annual_rate=_fv("0.055"),
                monthly_minimum=_fv("310"),
            ),
            HouseholdDebt(
                debt_id="cc",
                category=DebtCategory.CREDIT_CARD,
                label="Credit card",
                balance=_fv("9500"),
                annual_rate=_fv("0.229"),
                monthly_minimum=_fv("250"),
            ),
        ),
        benefits=(
            EmployerBenefit(
                benefit_id="401k-primary",
                member_id="primary",
                plan_type="401k",
                annual_employee_limit=_fv("23000"),
                match_tiers=(EmployerMatchTier(
                    match_rate=Decimal("0.50"),
                    up_to_percent_of_salary=Decimal("0.06"),
                ),),
            ),
            EmployerBenefit(
                benefit_id="401k-secondary",
                member_id="secondary",
                plan_type="401k",
                annual_employee_limit=_fv("23000"),
                match_tiers=(EmployerMatchTier(
                    match_rate=Decimal("0.50"),
                    up_to_percent_of_salary=Decimal("0.04"),
                ),),
            ),
        ),
        goals=(
            Goal(
                goal_id="home-purchase",
                label="Home down payment",
                target_amount=_fv("200000"),
                priority=GoalPriority.HIGH,
                flexibility=GoalFlexibility.DATE_FLEXIBLE,
                owner_member_ids=("primary", "secondary"),
                horizon_years=4,
            ),
            Goal(
                goal_id="college-529",
                label="529 college fund",
                target_amount=_fv("50000"),
                priority=GoalPriority.MEDIUM,
                flexibility=GoalFlexibility.AMOUNT_FLEXIBLE,
                owner_member_ids=("primary", "secondary"),
                horizon_years=15,
            ),
        ),
        constraints=(),
        tax_profile=TaxProfile(
            filing_status=FilingStatus.MARRIED_FILING_JOINTLY,
            domicile_state="CA",
            work_state="CA",
        ),
    )


def main() -> None:
    save = "--save" in sys.argv

    household = _demo_household()
    rules = federal_rules_2024()
    result = optimize_household_allocation(household, rules)
    ctx = OptimizerRenderContext(household=household, result=result)

    hh_md = render_household_markdown(ctx)
    rv_md = render_reviewer_markdown(ctx)
    hh_html = render_household_html(ctx)
    rv_html = render_reviewer_html(ctx)
    combined_html = render_combined_html(ctx)

    if save:
        out = Path(__file__).parent / "out"
        out.mkdir(exist_ok=True)
        (out / "optimizer_household.md").write_text(hh_md, encoding="utf-8")
        (out / "optimizer_reviewer.md").write_text(rv_md, encoding="utf-8")
        (out / "optimizer_household.html").write_text(hh_html, encoding="utf-8")
        (out / "optimizer_reviewer.html").write_text(rv_html, encoding="utf-8")
        (out / "optimizer_combined.html").write_text(combined_html, encoding="utf-8")
        print(f"Saved 5 artifacts to {out}/")
    else:
        print("=== Household Markdown ===")
        print(hh_md)
        print("=== Reviewer Markdown ===")
        print(rv_md)
        print("=== HTML artifact sizes ===")
        print(f"  household HTML: {len(hh_html.encode('utf-8')):,} bytes")
        print(f"  reviewer HTML:  {len(rv_html.encode('utf-8')):,} bytes")
        print(f"  combined HTML:  {len(combined_html.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    main()
