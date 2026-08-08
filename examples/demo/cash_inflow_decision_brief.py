"""Run the synthetic Spec 011 decision-brief example."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from kinvoryx.cash_inflow import Debt, HouseholdCase, build_decision_brief


def main() -> None:
    household = HouseholdCase(
        case_id="synthetic-bonus-001",
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
    brief = build_decision_brief(household)
    print(f"Synthetic decision brief: {brief.case_id}")
    for plan in brief.alternatives:
        print(f"\n{plan.label}")
        print(f"  Allocations: {plan.allocations}")
        print(f"  Liquidity: {plan.metrics.liquidity_months} months")
        print(f"  Interest avoided: ${plan.metrics.estimated_first_year_interest_avoided}")
        print(f"  Employer match captured: ${plan.metrics.estimated_employer_match_captured}")
        print(f"  Goal funding: ${plan.metrics.near_term_goal_funded}")
        print(f"  Trade-off: {plan.tradeoffs[2]}")


if __name__ == "__main__":
    main()
