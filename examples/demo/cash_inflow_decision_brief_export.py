"""Export household and reviewer artifacts for the synthetic Spec 011 demo."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from kinvoryx.cash_inflow_rendering import (
    BriefRenderContext,
    render_household_html,
    render_household_markdown,
    render_reviewer_html,
    render_reviewer_markdown,
)
from kinvoryx.cash_inflow_validation import golden_case_fixtures, validate_golden_case


def main() -> None:
    fixture = golden_case_fixtures()[0]
    evidence = validate_golden_case(fixture)
    context = BriefRenderContext(
        household=fixture.household,
        brief=evidence.brief,
        validation_evidence=evidence,
        reviewer_annotations=fixture.reviewer_annotations,
    )
    print("=== Household Markdown ===")
    print(render_household_markdown(context))
    print("=== Reviewer Markdown ===")
    print(render_reviewer_markdown(context))
    print("=== Household HTML bytes ===")
    print(len(render_household_html(context).encode("utf-8")))
    print("=== Reviewer HTML bytes ===")
    print(len(render_reviewer_html(context).encode("utf-8")))


if __name__ == "__main__":
    main()
