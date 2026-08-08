"""Household and reviewer renderers for Spec 011 decision briefs."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from html import escape

from kinvoryx.cash_inflow import AllocationPlan, DecisionBrief, HouseholdCase
from kinvoryx.cash_inflow_validation import ReviewerAnnotation, ValidationEvidence


SAFETY_DISCLOSURE = (
    "Synthetic decision-support prototype only. Values are deterministic estimates "
    "from manually entered inputs; this artifact does not provide personalized "
    "financial, tax, legal, trading, benefits, or execution advice."
)
RENDER_TRACE_IDS = ("REQ-CIB-017", "REQ-CIB-018", "REQ-CIB-019", "REQ-CIB-022", "REQ-CIB-023")


@dataclass(frozen=True)
class BriefRenderContext:
    """All source material needed to render Slice C artifacts."""

    household: HouseholdCase
    brief: DecisionBrief
    validation_evidence: ValidationEvidence | None = None
    reviewer_annotations: tuple[ReviewerAnnotation, ...] = ()


def render_household_markdown(context: BriefRenderContext) -> str:
    """Render the household-readable Markdown artifact."""
    household = context.household
    lines = [
        f"# Cash Inflow Allocation Decision Brief - {household.case_id}",
        "",
        f"**Boundary:** {SAFETY_DISCLOSURE}",
        "",
        "## Input Snapshot",
        "",
        f"- Cash inflow: {_money(household.cash_inflow)}",
        f"- Monthly essential expenses: {_money(household.monthly_essential_expenses)}",
        f"- Current liquid reserves: {_money(household.liquid_reserves)}",
        f"- Employer-match contribution room: {_money(household.employer_match_contribution_room)}",
        f"- Employer-match rate: {_percent(household.employer_match_rate)}",
        f"- Tax-advantaged contribution room: {_money(household.tax_advantaged_contribution_room)}",
        f"- Estimated marginal tax rate: {_percent(household.estimated_marginal_tax_rate)}",
        f"- Near-term goal remaining: {_money(household.near_term_goal_remaining)}",
        "",
        "## Comparable Alternatives",
        "",
        _markdown_plan_table(_plans(context.brief)),
        "",
        "## Scenario Summaries",
        "",
    ]
    for plan in _plans(context.brief):
        lines.extend([f"### {plan.label}", ""])
        lines.extend(f"- {scenario.summary}" for scenario in plan.scenarios)
        lines.append("")

    lines.extend(["## Trade-Off Notes", ""])
    for plan in _plans(context.brief):
        lines.extend([f"### {plan.label}", ""])
        lines.extend(f"- {tradeoff}" for tradeoff in plan.tradeoffs)
        lines.append("")

    lines.extend(["## Assumptions", ""])
    lines.extend(f"- {assumption}" for assumption in context.brief.assumptions)
    lines.extend(["", "## Calculation Posture", ""])
    lines.append(
        "This artifact compares alternatives under shared assumptions. It does not rank, select, or execute a plan."
    )
    return "\n".join(lines).strip() + "\n"


def render_reviewer_markdown(context: BriefRenderContext) -> str:
    """Render the reviewer-readable Markdown record."""
    household = context.household
    evidence = context.validation_evidence
    annotations = _context_annotations(context)
    lines = [
        f"# Reviewer Record - {household.case_id}",
        "",
        f"**Boundary:** {SAFETY_DISCLOSURE}",
        "",
        f"**Trace IDs:** {', '.join(RENDER_TRACE_IDS)}",
        "",
        "## Validation Status",
        "",
    ]
    if evidence is None:
        lines.extend(
            [
                "- Validation evidence: not supplied for this render.",
                "- Pilot readiness: not assessed in this render.",
            ]
        )
    else:
        lines.extend(
            [
                f"- Validation passed: {_yes_no(evidence.passed)}",
                f"- Pilot ready: {_yes_no(evidence.pilot_ready)}",
                f"- Validation issue count: {len(evidence.issues)}",
                f"- Open blocker count: {len(evidence.blocker_annotations)}",
            ]
        )
    lines.extend(["", "## Full Input Snapshot", ""])
    lines.extend(_household_snapshot_lines(household))
    lines.extend(["", "## Supported Debts", ""])
    if household.debts:
        lines.append("| Debt | Balance | Annual rate |")
        lines.append("|---|---:|---:|")
        for debt in household.debts:
            lines.append(
                f"| {debt.identifier} | {_money(debt.balance)} | {_percent(debt.annual_interest_rate)} |"
            )
    else:
        lines.append("No supported debts supplied.")

    lines.extend(["", "## Comparable Alternatives", "", _markdown_plan_table(_plans(context.brief))])
    lines.extend(["", "## Reviewer Annotations", ""])
    if annotations:
        lines.append("| ID | Role | Target | Category | Severity | Disposition | Trace IDs | Note |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for annotation in annotations:
            target = annotation.strategy or "case"
            lines.append(
                "| "
                + " | ".join(
                    (
                        annotation.annotation_id,
                        annotation.reviewer_role,
                        target,
                        annotation.category,
                        annotation.severity,
                        annotation.disposition,
                        ", ".join(annotation.trace_ids),
                        annotation.note,
                    )
                )
                + " |"
            )
    else:
        lines.append("No reviewer annotations supplied.")

    if evidence is not None and evidence.issues:
        lines.extend(["", "## Validation Issues", ""])
        for issue in evidence.issues:
            target = f" ({issue.strategy})" if issue.strategy else ""
            lines.append(f"- {issue.code}{target}: {issue.message} [{', '.join(issue.trace_ids)}]")

    lines.extend(["", "## Household Artifact", "", render_household_markdown(context).strip()])
    return "\n".join(lines).strip() + "\n"


def render_household_html(context: BriefRenderContext) -> str:
    """Render a complete household-facing HTML artifact."""
    body = _household_html_body(context)
    return _html_document(f"Cash Inflow Brief - {context.household.case_id}", body)


def render_reviewer_html(context: BriefRenderContext) -> str:
    """Render a complete reviewer-facing HTML record."""
    body = _reviewer_html_body(context)
    return _html_document(f"Reviewer Record - {context.household.case_id}", body)


def render_combined_html(context: BriefRenderContext) -> str:
    """Render household and reviewer views in one local interface page."""
    body = (
        "<main>"
        + _household_html_body(context, include_main=False)
        + _reviewer_html_body(context, include_main=False)
        + "</main>"
    )
    return _html_document(f"Decision Brief - {context.household.case_id}", body)


def _household_html_body(context: BriefRenderContext, include_main: bool = True) -> str:
    household = context.household
    content = [
        "<section class=\"band\">",
        f"<h1>Cash Inflow Allocation Decision Brief</h1>",
        f"<p class=\"meta\">Case {escape(household.case_id)}</p>",
        f"<p class=\"notice\">{escape(SAFETY_DISCLOSURE)}</p>",
        "</section>",
        "<section class=\"band\">",
        "<h2>Input Snapshot</h2>",
        _html_definition_grid(_household_snapshot_pairs(household)),
        "</section>",
        "<section class=\"band\">",
        "<h2>Comparable Alternatives</h2>",
        _html_plan_table(_plans(context.brief)),
        "</section>",
        "<section class=\"band\">",
        "<h2>Scenario Summaries</h2>",
        _html_plan_details(context.brief, "scenarios"),
        "</section>",
        "<section class=\"band\">",
        "<h2>Trade-Off Notes</h2>",
        _html_plan_details(context.brief, "tradeoffs"),
        "</section>",
        "<section class=\"band\">",
        "<h2>Assumptions</h2>",
        _html_list(context.brief.assumptions),
        "<p class=\"meta\">This artifact compares alternatives under shared assumptions. It does not rank, select, or execute a plan.</p>",
        "</section>",
    ]
    joined = "\n".join(content)
    return f"<main>{joined}</main>" if include_main else joined


def _reviewer_html_body(context: BriefRenderContext, include_main: bool = True) -> str:
    household = context.household
    evidence = context.validation_evidence
    annotations = _context_annotations(context)
    content = [
        "<section class=\"band reviewer\">",
        "<h1>Reviewer Record</h1>",
        f"<p class=\"meta\">Case {escape(household.case_id)}</p>",
        f"<p class=\"notice\">{escape(SAFETY_DISCLOSURE)}</p>",
        f"<p class=\"meta\">Trace IDs: {escape(', '.join(RENDER_TRACE_IDS))}</p>",
        "</section>",
        "<section class=\"band reviewer\">",
        "<h2>Validation Status</h2>",
        _validation_status_html(evidence),
        "</section>",
        "<section class=\"band reviewer\">",
        "<h2>Full Input Snapshot</h2>",
        _html_definition_grid(_household_snapshot_pairs(household)),
        "<h3>Supported Debts</h3>",
        _html_debt_table(household),
        "</section>",
        "<section class=\"band reviewer\">",
        "<h2>Reviewer Annotations</h2>",
        _annotations_table_html(annotations),
        "</section>",
        "<section class=\"band reviewer\">",
        "<h2>Reviewer Alternative Table</h2>",
        _html_plan_table(_plans(context.brief)),
        "</section>",
    ]
    joined = "\n".join(content)
    return f"<main>{joined}</main>" if include_main else joined


def _markdown_plan_table(plans: tuple[AllocationPlan, ...]) -> str:
    rows = [
        "| Plan | Reserve | Match contribution | Debt paydown | Tax savings | Goal | Retained cash | Liquidity months | Interest avoided | Match captured | Tax value | Debt remaining |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for plan in plans:
        rows.append(
            "| "
            + " | ".join(
                (
                    plan.label,
                    _money(plan.allocations["emergency_reserve"]),
                    _money(plan.allocations["employer_match_contribution"]),
                    _money(plan.allocations["debt_paydown"]),
                    _money(plan.allocations["tax_advantaged_savings"]),
                    _money(plan.allocations["near_term_goal"]),
                    _money(plan.allocations["retained_cash"]),
                    str(plan.metrics.liquidity_months),
                    _money(plan.metrics.estimated_first_year_interest_avoided),
                    _money(plan.metrics.estimated_employer_match_captured),
                    _money(plan.metrics.estimated_tax_value),
                    _money(plan.metrics.supported_debt_remaining),
                )
            )
            + " |"
        )
    return "\n".join(rows)


def _html_plan_table(plans: tuple[AllocationPlan, ...]) -> str:
    headers = (
        "Plan",
        "Reserve",
        "Match contribution",
        "Debt paydown",
        "Tax savings",
        "Goal",
        "Retained cash",
        "Liquidity months",
        "Interest avoided",
        "Match captured",
        "Tax value",
        "Debt remaining",
    )
    rows = []
    for plan in plans:
        rows.append(
            (
                plan.label,
                _money(plan.allocations["emergency_reserve"]),
                _money(plan.allocations["employer_match_contribution"]),
                _money(plan.allocations["debt_paydown"]),
                _money(plan.allocations["tax_advantaged_savings"]),
                _money(plan.allocations["near_term_goal"]),
                _money(plan.allocations["retained_cash"]),
                str(plan.metrics.liquidity_months),
                _money(plan.metrics.estimated_first_year_interest_avoided),
                _money(plan.metrics.estimated_employer_match_captured),
                _money(plan.metrics.estimated_tax_value),
                _money(plan.metrics.supported_debt_remaining),
            )
        )
    return _html_table(headers, rows, numeric_from=1)


def _html_plan_details(brief: DecisionBrief, detail_type: str) -> str:
    sections = []
    for plan in _plans(brief):
        if detail_type == "scenarios":
            items = tuple(scenario.summary for scenario in plan.scenarios)
        else:
            items = plan.tradeoffs
        sections.append(f"<article class=\"detail\"><h3>{escape(plan.label)}</h3>{_html_list(items)}</article>")
    return "\n".join(sections)


def _validation_status_html(evidence: ValidationEvidence | None) -> str:
    if evidence is None:
        return _html_list(("Validation evidence not supplied for this render.", "Pilot readiness not assessed."))
    items = (
        f"Validation passed: {_yes_no(evidence.passed)}",
        f"Pilot ready: {_yes_no(evidence.pilot_ready)}",
        f"Validation issue count: {len(evidence.issues)}",
        f"Open blocker count: {len(evidence.blocker_annotations)}",
    )
    output = [_html_list(items)]
    if evidence.issues:
        rows = tuple((issue.code, issue.strategy or "case", issue.message, ", ".join(issue.trace_ids)) for issue in evidence.issues)
        output.append(_html_table(("Code", "Target", "Message", "Trace IDs"), rows))
    return "\n".join(output)


def _annotations_table_html(annotations: tuple[ReviewerAnnotation, ...]) -> str:
    if not annotations:
        return "<p>No reviewer annotations supplied.</p>"
    rows = tuple(
        (
            annotation.annotation_id,
            annotation.reviewer_role,
            annotation.strategy or "case",
            annotation.category,
            annotation.severity,
            annotation.disposition,
            ", ".join(annotation.trace_ids),
            annotation.note,
        )
        for annotation in annotations
    )
    return _html_table(("ID", "Role", "Target", "Category", "Severity", "Disposition", "Trace IDs", "Note"), rows)


def _html_debt_table(household: HouseholdCase) -> str:
    if not household.debts:
        return "<p>No supported debts supplied.</p>"
    rows = tuple((debt.identifier, _money(debt.balance), _percent(debt.annual_interest_rate)) for debt in household.debts)
    return _html_table(("Debt", "Balance", "Annual rate"), rows, numeric_from=1)


def _html_definition_grid(pairs: tuple[tuple[str, str], ...]) -> str:
    parts = ["<dl class=\"def-grid\">"]
    for key, value in pairs:
        parts.append(f"<div><dt>{escape(key)}</dt><dd>{escape(value)}</dd></div>")
    parts.append("</dl>")
    return "\n".join(parts)


def _html_table(headers: tuple[str, ...], rows: tuple[tuple[str, ...], ...], numeric_from: int | None = None) -> str:
    head = "".join(f"<th>{escape(header)}</th>" for header in headers)
    body_rows = []
    for row in rows:
        cells = []
        for index, value in enumerate(row):
            class_attr = " class=\"num\"" if numeric_from is not None and index >= numeric_from else ""
            cells.append(f"<td{class_attr}>{escape(str(value))}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<div class=\"table-wrap\"><table><thead><tr>{head}</tr></thead><tbody>{''.join(body_rows)}</tbody></table></div>"


def _html_list(items: tuple[str, ...]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def _html_document(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #52616f;
      --line: #d7dee6;
      --panel: #f8fafc;
      --paper: #ffffff;
      --accent: #0f766e;
      --warn: #7c2d12;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.45;
    }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px; }}
    .band {{ border-bottom: 1px solid var(--line); padding: 22px 0; }}
    h1, h2, h3 {{ margin: 0 0 12px; letter-spacing: 0; }}
    h1 {{ font-size: 28px; }}
    h2 {{ font-size: 20px; }}
    h3 {{ font-size: 16px; }}
    .meta {{ color: var(--muted); margin: 6px 0; }}
    .notice {{ border-left: 4px solid var(--accent); background: var(--panel); padding: 10px 12px; margin: 12px 0; }}
    .reviewer .notice {{ border-left-color: var(--warn); }}
    .def-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; margin: 0; }}
    .def-grid div {{ border: 1px solid var(--line); padding: 10px; background: var(--panel); }}
    dt {{ color: var(--muted); font-size: 12px; }}
    dd {{ margin: 4px 0 0; font-weight: 650; overflow-wrap: anywhere; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 920px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: var(--panel); font-size: 12px; color: var(--muted); }}
    td.num {{ text-align: right; white-space: nowrap; }}
    ul {{ padding-left: 20px; }}
    .detail {{ margin: 14px 0; }}
    @media (max-width: 700px) {{
      main {{ padding: 16px; }}
      h1 {{ font-size: 23px; }}
      table {{ min-width: 760px; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def _context_annotations(context: BriefRenderContext) -> tuple[ReviewerAnnotation, ...]:
    if context.reviewer_annotations:
        return context.reviewer_annotations
    if context.validation_evidence is not None:
        return context.validation_evidence.blocker_annotations
    return ()


def _plans(brief: DecisionBrief) -> tuple[AllocationPlan, ...]:
    return (brief.baseline,) + brief.alternatives


def _household_snapshot_lines(household: HouseholdCase) -> tuple[str, ...]:
    return tuple(f"- {key}: {value}" for key, value in _household_snapshot_pairs(household))


def _household_snapshot_pairs(household: HouseholdCase) -> tuple[tuple[str, str], ...]:
    return (
        ("Cash inflow", _money(household.cash_inflow)),
        ("Monthly essential expenses", _money(household.monthly_essential_expenses)),
        ("Current liquid reserves", _money(household.liquid_reserves)),
        ("Employer-match contribution room", _money(household.employer_match_contribution_room)),
        ("Employer-match rate", _percent(household.employer_match_rate)),
        ("Tax-advantaged contribution room", _money(household.tax_advantaged_contribution_room)),
        ("Estimated marginal tax rate", _percent(household.estimated_marginal_tax_rate)),
        ("Near-term goal remaining", _money(household.near_term_goal_remaining)),
        ("Synthetic input", _yes_no(household.synthetic)),
    )


def _money(value: Decimal) -> str:
    return f"${value:,.2f}"


def _percent(value: Decimal) -> str:
    return f"{value:.2%}"


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
