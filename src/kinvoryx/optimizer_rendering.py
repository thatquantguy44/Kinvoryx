"""Household and reviewer renderers for Spec 004 optimizer output."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from html import escape

from kinvoryx.capital_allocation_optimizer import (
    AllocationAlternative,
    AllocationUse,
    InfeasibilityReport,
    OptimizerResult,
    ScenarioResult,
)
from kinvoryx.household_state import HouseholdState


SAFETY_DISCLOSURE = (
    "Synthetic decision-support prototype only. Values are deterministic estimates "
    "from manually entered inputs; this artifact does not provide personalized "
    "financial, tax, legal, trading, benefits, or execution advice."
)

_USE_ORDER = (
    AllocationUse.EMERGENCY_RESERVE,
    AllocationUse.EMPLOYER_MATCH,
    AllocationUse.HIGH_COST_DEBT,
    AllocationUse.TAX_ADVANTAGED_SAVINGS,
    AllocationUse.GOAL_FUNDING,
    AllocationUse.LOWER_COST_DEBT,
    AllocationUse.DISCRETIONARY_BUFFER,
)

_USE_LABELS = {
    AllocationUse.EMERGENCY_RESERVE: "Emergency reserve",
    AllocationUse.EMPLOYER_MATCH: "Employer match",
    AllocationUse.HIGH_COST_DEBT: "High-cost debt",
    AllocationUse.TAX_ADVANTAGED_SAVINGS: "Tax-advantaged savings",
    AllocationUse.GOAL_FUNDING: "Goal funding",
    AllocationUse.LOWER_COST_DEBT: "Lower-cost debt",
    AllocationUse.DISCRETIONARY_BUFFER: "Discretionary buffer",
}

ZERO = Decimal("0")


@dataclass(frozen=True)
class OptimizerRenderContext:
    """All source material needed to render optimizer artifacts."""

    household: HouseholdState
    result: OptimizerResult


# --------------------------------------------------------------------------- #
# Markdown renderers                                                           #
# --------------------------------------------------------------------------- #


def render_household_markdown(ctx: OptimizerRenderContext) -> str:
    """Household-readable Markdown: comparison table, scenarios, assumptions."""
    r = ctx.result
    all_alts = (r.baseline,) + r.alternatives
    rec = _alternative_by_name(r, "recommended") or r.baseline

    lines = [
        f"# Capital Allocation Decision Brief — {r.household_id}",
        "",
        f"**Boundary:** {SAFETY_DISCLOSURE}",
        "",
        f"**Period:** {r.period_label}  |  **Jurisdiction:** {r.jurisdiction_scope}",
        "",
        "## Household Snapshot",
        "",
        *_snapshot_md_lines(r),
        "",
    ]

    if r.infeasibility:
        lines += _infeasibility_md_section(r.infeasibility)
    else:
        lines += [
            "## Comparable Alternatives",
            "",
            _markdown_comparison_table(all_alts),
            "",
            "## Allocation Detail — Recommended",
            "",
            _markdown_detail_table(rec),
            "",
            "## Scenario Results — Recommended",
            "",
            _markdown_scenario_table(rec.scenario_results),
            "",
        ]
        if rec.binding_constraints:
            lines += [
                "## Binding Constraints",
                "",
                *[f"- **{c.dimension}**: limit {_money(c.limit)}, applied {_money(c.applied)}"
                  + (f", marginal value {_percent(c.marginal_value)}" if c.marginal_value else "")
                  for c in rec.binding_constraints],
                "",
            ]
        if rec.opportunity_costs:
            lines += [
                "## Opportunity Costs",
                "",
                *[f"- **{o.foregone_use}** (${_money(o.foregone_amount)}): {o.description}"
                  for o in rec.opportunity_costs],
                "",
            ]

    lines += [
        "## Common Assumptions",
        "",
        *[f"- {a}" for a in r.common_assumptions],
        "",
        "## Calculation Posture",
        "",
        "This artifact compares alternatives under shared assumptions. "
        "It does not rank, select, or execute a plan.",
        "",
    ]
    return "\n".join(lines).strip() + "\n"


def render_reviewer_markdown(ctx: OptimizerRenderContext) -> str:
    """Reviewer-readable Markdown: full structured dump across all alternatives."""
    r = ctx.result
    all_alts = (r.baseline,) + r.alternatives

    lines = [
        f"# Reviewer Record — {r.household_id}",
        "",
        f"**Boundary:** {SAFETY_DISCLOSURE}",
        f"**Household fingerprint:** `{r.household_fingerprint}`",
        f"**Period:** {r.period_label}  |  **Jurisdiction:** {r.jurisdiction_scope}",
        "",
        "## Household Snapshot",
        "",
        *_snapshot_md_lines(r),
        "",
        "## Income Sources",
        "",
        *[f"- {inc.source_id} ({inc.income_type.value}): "
          f"{_money(inc.annual_gross.value or ZERO)}/yr  "
          f"[{inc.annual_gross.provenance.value}, {inc.annual_gross.freshness.value}]"
          for inc in ctx.household.income_sources],
        "",
        "## Debts",
        "",
    ]
    if ctx.household.debts:
        lines += [
            "| Debt | Balance | APR | Monthly minimum | Prepay penalty |",
            "|---|---:|---:|---:|:---:|",
            *[f"| {d.label} | {_money(d.balance.value or ZERO)} "
              f"| {_percent(d.annual_rate.value or ZERO)} "
              f"| {_money(d.monthly_minimum.value or ZERO)} "
              f"| {'yes' if d.prepayment_penalty else 'no'} |"
              for d in ctx.household.debts],
        ]
    else:
        lines.append("No debts declared.")
    lines.append("")

    if r.infeasibility:
        lines += _infeasibility_md_section(r.infeasibility)
    else:
        lines += [
            "## Comparable Alternatives",
            "",
            _markdown_comparison_table(all_alts),
            "",
        ]
        for alt in all_alts:
            lines += [
                f"## {alt.label}",
                "",
                f"**Trade-off:** {alt.trade_off_summary}",
                "",
                "### Allocation Lines",
                "",
                _markdown_detail_table(alt),
                "",
                "### Scenarios",
                "",
                _markdown_scenario_table(alt.scenario_results),
                "",
            ]
            if alt.binding_constraints:
                lines += [
                    "### Binding Constraints",
                    "",
                    *[f"- {c.dimension}: limit {_money(c.limit)}, applied {_money(c.applied)}"
                      + (f", marginal_value {_percent(c.marginal_value)}" if c.marginal_value else "")
                      for c in alt.binding_constraints],
                    "",
                ]
            if alt.opportunity_costs:
                lines += [
                    "### Opportunity Costs",
                    "",
                    *[f"- {o.foregone_use} (${_money(o.foregone_amount)}): {o.description}"
                      for o in alt.opportunity_costs],
                    "",
                ]
            lines += [
                "### Assumptions",
                "",
                *[f"- {a}" for a in alt.assumptions],
                "",
            ]

    lines += [
        "## Common Assumptions",
        "",
        *[f"- {a}" for a in r.common_assumptions],
        "",
    ]
    return "\n".join(lines).strip() + "\n"


# --------------------------------------------------------------------------- #
# HTML renderers                                                               #
# --------------------------------------------------------------------------- #


def render_household_html(ctx: OptimizerRenderContext) -> str:
    """Household-facing HTML artifact."""
    body = _household_html_body(ctx)
    return _html_document(f"Allocation Brief — {ctx.result.household_id}", body)


def render_reviewer_html(ctx: OptimizerRenderContext) -> str:
    """Reviewer-facing HTML record."""
    body = _reviewer_html_body(ctx)
    return _html_document(f"Reviewer Record — {ctx.result.household_id}", body)


def render_combined_html(ctx: OptimizerRenderContext) -> str:
    """Household and reviewer views in one local interface page."""
    body = (
        "<main>"
        + _household_html_body(ctx, include_main=False)
        + _reviewer_html_body(ctx, include_main=False)
        + "</main>"
    )
    return _html_document(f"Decision Brief — {ctx.result.household_id}", body)


# --------------------------------------------------------------------------- #
# HTML body builders                                                           #
# --------------------------------------------------------------------------- #


def _household_html_body(ctx: OptimizerRenderContext, include_main: bool = True) -> str:
    r = ctx.result
    all_alts = (r.baseline,) + r.alternatives
    rec = _alternative_by_name(r, "recommended") or r.baseline

    content = [
        "<section class=\"band\">",
        "<h1>Capital Allocation Decision Brief</h1>",
        f"<p class=\"meta\">Household: {escape(r.household_id)} &nbsp;·&nbsp; "
        f"{escape(r.period_label)} &nbsp;·&nbsp; {escape(r.jurisdiction_scope)}</p>",
        f"<p class=\"notice\">{escape(SAFETY_DISCLOSURE)}</p>",
        "</section>",
        "<section class=\"band\">",
        "<h2>Household Snapshot</h2>",
        _html_def_grid(_snapshot_pairs(r)),
        "</section>",
    ]

    if r.infeasibility:
        content += [
            "<section class=\"band\">",
            "<h2>Infeasibility</h2>",
            f"<p class=\"warn-box\">{escape(r.infeasibility.diagnosis)}</p>",
            _html_def_grid((
                ("Minimum required annual", _money(r.infeasibility.minimum_required_annual)),
                ("Actual gross income", _money(r.infeasibility.actual_annual_gross)),
                ("Annual shortfall", _money(r.infeasibility.shortfall)),
            )),
            "</section>",
        ]
    else:
        content += [
            "<section class=\"band\">",
            "<h2>Comparable Alternatives</h2>",
            _html_comparison_table(all_alts),
            "</section>",
            "<section class=\"band\">",
            "<h2>Allocation Detail — Recommended</h2>",
            _html_detail_table(rec),
            "</section>",
            "<section class=\"band\">",
            "<h2>Scenario Results — Recommended</h2>",
            _html_scenario_table(rec.scenario_results),
            "</section>",
        ]
        if rec.binding_constraints or rec.opportunity_costs:
            content.append("<section class=\"band\">")
            if rec.binding_constraints:
                content.append("<h2>Binding Constraints</h2>")
                rows = tuple(
                    (c.dimension, _money(c.limit), _money(c.applied),
                     _percent(c.marginal_value) if c.marginal_value else "—")
                    for c in rec.binding_constraints
                )
                content.append(_html_table(("Dimension", "Limit", "Applied", "Marginal value"), rows, numeric_from=1))
            if rec.opportunity_costs:
                content.append("<h2>Opportunity Costs</h2>")
                rows = tuple(
                    (o.foregone_use, _money(o.foregone_amount), o.description)
                    for o in rec.opportunity_costs
                )
                content.append(_html_table(("Foregone use", "Amount", "Description"), rows, numeric_from=1))
            content.append("</section>")

    content += [
        "<section class=\"band\">",
        "<h2>Common Assumptions</h2>",
        _html_list(r.common_assumptions),
        "<p class=\"meta\">This artifact compares alternatives under shared assumptions. "
        "It does not rank, select, or execute a plan.</p>",
        "</section>",
    ]
    joined = "\n".join(content)
    return f"<main>{joined}</main>" if include_main else joined


def _reviewer_html_body(ctx: OptimizerRenderContext, include_main: bool = True) -> str:
    r = ctx.result
    all_alts = (r.baseline,) + r.alternatives

    content = [
        "<section class=\"band reviewer\">",
        "<h1>Reviewer Record</h1>",
        f"<p class=\"meta\">Household: {escape(r.household_id)} &nbsp;·&nbsp; "
        f"{escape(r.period_label)} &nbsp;·&nbsp; {escape(r.jurisdiction_scope)}</p>",
        f"<p class=\"meta\">Fingerprint: <code>{escape(r.household_fingerprint)}</code></p>",
        f"<p class=\"notice\">{escape(SAFETY_DISCLOSURE)}</p>",
        "</section>",
        "<section class=\"band reviewer\">",
        "<h2>Income Sources</h2>",
        _html_income_table(ctx.household),
        "<h2>Debts</h2>",
        _html_debt_table(ctx.household),
        "</section>",
    ]

    if r.infeasibility:
        content += [
            "<section class=\"band reviewer\">",
            "<h2>Infeasibility Diagnosis</h2>",
            f"<p class=\"warn-box\">{escape(r.infeasibility.diagnosis)}</p>",
            _html_def_grid((
                ("Minimum required annual", _money(r.infeasibility.minimum_required_annual)),
                ("Actual gross income", _money(r.infeasibility.actual_annual_gross)),
                ("Annual shortfall", _money(r.infeasibility.shortfall)),
            )),
            "</section>",
        ]
    else:
        content += [
            "<section class=\"band reviewer\">",
            "<h2>Comparable Alternatives</h2>",
            _html_comparison_table(all_alts),
            "</section>",
        ]
        for alt in all_alts:
            content += [
                "<section class=\"band reviewer\">",
                f"<h2>{escape(alt.label)}</h2>",
                f"<p class=\"meta\">{escape(alt.trade_off_summary)}</p>",
                "<h3>Allocation Lines</h3>",
                _html_detail_table(alt),
                "<h3>Scenarios</h3>",
                _html_scenario_table(alt.scenario_results),
            ]
            if alt.binding_constraints:
                rows = tuple(
                    (c.dimension, _money(c.limit), _money(c.applied),
                     _percent(c.marginal_value) if c.marginal_value else "—")
                    for c in alt.binding_constraints
                )
                content += [
                    "<h3>Binding Constraints</h3>",
                    _html_table(("Dimension", "Limit", "Applied", "Marginal value"), rows, numeric_from=1),
                ]
            if alt.opportunity_costs:
                rows = tuple(
                    (o.foregone_use, _money(o.foregone_amount), o.description)
                    for o in alt.opportunity_costs
                )
                content += [
                    "<h3>Opportunity Costs</h3>",
                    _html_table(("Foregone use", "Amount", "Description"), rows, numeric_from=1),
                ]
            if alt.assumptions:
                content += ["<h3>Assumptions</h3>", _html_list(alt.assumptions)]
            content.append("</section>")

    content += [
        "<section class=\"band reviewer\">",
        "<h2>Common Assumptions</h2>",
        _html_list(r.common_assumptions),
        "</section>",
    ]
    joined = "\n".join(content)
    return f"<main>{joined}</main>" if include_main else joined


# --------------------------------------------------------------------------- #
# Table helpers                                                                #
# --------------------------------------------------------------------------- #


def _use_totals(alt: AllocationAlternative) -> dict[AllocationUse, Decimal]:
    totals: dict[AllocationUse, Decimal] = {u: ZERO for u in _USE_ORDER}
    for line in alt.lines:
        totals[line.use] = totals.get(line.use, ZERO) + line.amount
    return totals


def _markdown_comparison_table(alts: tuple[AllocationAlternative, ...]) -> str:
    use_headers = [_USE_LABELS[u] for u in _USE_ORDER]
    header = "| Alternative | " + " | ".join(use_headers) + " | Total |"
    sep = "|---|" + "---:|" * len(_USE_ORDER) + "---:|"
    rows = [header, sep]
    for alt in alts:
        totals = _use_totals(alt)
        cells = " | ".join(_money(totals[u]) for u in _USE_ORDER)
        rows.append(f"| {alt.label} | {cells} | {_money(alt.total_allocated)} |")
    return "\n".join(rows)


def _markdown_detail_table(alt: AllocationAlternative) -> str:
    rows = [
        "| Use | Destination | Amount | Rationale |",
        "|---|---|---:|---|",
    ]
    for line in alt.lines:
        dest = line.destination_label
        rows.append(f"| {_USE_LABELS[line.use]} | {dest} | {_money(line.amount)} | {line.rationale} |")
    rows.append(f"| **Total** | | **{_money(alt.total_allocated)}** | |")
    return "\n".join(rows)


def _markdown_scenario_table(scenarios: tuple[ScenarioResult, ...]) -> str:
    rows = [
        "| Scenario | Income reduction | Expense increase | Reserve months | Survives |",
        "|---|---:|---:|---:|:---:|",
    ]
    for s in scenarios:
        months = _decimal(s.reserve_months_remaining) if s.reserve_months_remaining else "—"
        rows.append(
            f"| {s.scenario} | {_money(s.income_reduction)} "
            f"| {_money(s.expense_increase)} | {months} "
            f"| {'yes' if s.plan_survives else 'NO'} |"
        )
    return "\n".join(rows)


def _html_comparison_table(alts: tuple[AllocationAlternative, ...]) -> str:
    headers = ("Alternative",) + tuple(_USE_LABELS[u] for u in _USE_ORDER) + ("Total",)
    rows = []
    for alt in alts:
        totals = _use_totals(alt)
        rows.append(
            (alt.label,)
            + tuple(_money(totals[u]) for u in _USE_ORDER)
            + (_money(alt.total_allocated),)
        )
    return _html_table(headers, tuple(rows), numeric_from=1)


def _html_detail_table(alt: AllocationAlternative) -> str:
    headers = ("Use", "Destination", "Amount", "Rationale")
    rows = tuple(
        (_USE_LABELS[line.use], line.destination_label, _money(line.amount), line.rationale)
        for line in alt.lines
    )
    return _html_table(headers, rows, numeric_from=2)


def _html_scenario_table(scenarios: tuple[ScenarioResult, ...]) -> str:
    headers = ("Scenario", "Income reduction", "Expense increase", "Reserve months", "Survives", "Notes")
    rows = tuple(
        (
            s.scenario,
            _money(s.income_reduction),
            _money(s.expense_increase),
            _decimal(s.reserve_months_remaining) if s.reserve_months_remaining is not None else "—",
            "yes" if s.plan_survives else "NO",
            s.notes,
        )
        for s in scenarios
    )
    return _html_table(headers, rows, numeric_from=1)


def _html_income_table(household: HouseholdState) -> str:
    if not household.income_sources:
        return "<p>No income sources declared.</p>"
    rows = tuple(
        (
            inc.source_id,
            inc.income_type.value,
            _money(inc.annual_gross.value or ZERO),
            inc.annual_gross.provenance.value,
            inc.annual_gross.freshness.value,
        )
        for inc in household.income_sources
    )
    return _html_table(("Source", "Type", "Annual gross", "Provenance", "Freshness"), rows, numeric_from=2)


def _html_debt_table(household: HouseholdState) -> str:
    if not household.debts:
        return "<p>No debts declared.</p>"
    rows = tuple(
        (
            d.label,
            _money(d.balance.value or ZERO),
            _percent(d.annual_rate.value or ZERO),
            _money(d.monthly_minimum.value or ZERO),
            "yes" if d.prepayment_penalty else "no",
        )
        for d in household.debts
    )
    return _html_table(("Debt", "Balance", "APR", "Monthly minimum", "Prepay penalty"), rows, numeric_from=1)


# --------------------------------------------------------------------------- #
# Snapshot helpers                                                             #
# --------------------------------------------------------------------------- #


def _snapshot_pairs(r: OptimizerResult) -> tuple[tuple[str, str], ...]:
    return (
        ("Annual gross income", _money(r.annual_gross_income)),
        ("Annual fixed obligations", _money(r.annual_fixed_obligations)),
        ("Annual surplus", _money(r.annual_surplus)),
        ("Household ID", r.household_id),
        ("Synthetic input", "yes"),
    )


def _snapshot_md_lines(r: OptimizerResult) -> tuple[str, ...]:
    return tuple(f"- {k}: {v}" for k, v in _snapshot_pairs(r))


def _infeasibility_md_section(inf: InfeasibilityReport) -> list[str]:
    return [
        "## Infeasibility",
        "",
        f"> {inf.diagnosis}",
        "",
        f"- Minimum required annual: {_money(inf.minimum_required_annual)}",
        f"- Actual gross income: {_money(inf.actual_annual_gross)}",
        f"- Annual shortfall: {_money(inf.shortfall)}",
        "",
    ]


# --------------------------------------------------------------------------- #
# Generic HTML primitives (mirrors cash_inflow_rendering.py)                  #
# --------------------------------------------------------------------------- #


def _html_def_grid(pairs: tuple[tuple[str, str], ...]) -> str:
    parts = ["<dl class=\"def-grid\">"]
    for key, value in pairs:
        parts.append(f"<div><dt>{escape(key)}</dt><dd>{escape(value)}</dd></div>")
    parts.append("</dl>")
    return "\n".join(parts)


def _html_table(
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
    numeric_from: int | None = None,
) -> str:
    head = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            cls = " class=\"num\"" if numeric_from is not None and i >= numeric_from else ""
            cells.append(f"<td{cls}>{escape(str(val))}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        f"<div class=\"table-wrap\"><table>"
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        f"</table></div>"
    )


def _html_list(items: tuple[str, ...]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def _alternative_by_name(r: OptimizerResult, name: str) -> AllocationAlternative | None:
    return next((a for a in r.alternatives if a.name == name), None)


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
    h1, h2, h3 {{ margin: 0 0 12px; }}
    h1 {{ font-size: 28px; }}
    h2 {{ font-size: 20px; }}
    h3 {{ font-size: 16px; color: var(--muted); }}
    .meta {{ color: var(--muted); margin: 6px 0; font-size: 14px; }}
    code {{ font-size: 12px; color: var(--muted); }}
    .notice {{ border-left: 4px solid var(--accent); background: var(--panel); padding: 10px 12px; margin: 12px 0; font-size: 14px; }}
    .warn-box {{ border-left: 4px solid var(--warn); background: #fff7f5; padding: 10px 12px; margin: 12px 0; }}
    .reviewer .notice {{ border-left-color: var(--warn); }}
    .def-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 12px 0 0; }}
    .def-grid div {{ border: 1px solid var(--line); padding: 10px; background: var(--panel); }}
    dt {{ color: var(--muted); font-size: 12px; }}
    dd {{ margin: 4px 0 0; font-weight: 650; overflow-wrap: anywhere; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); margin: 12px 0; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 700px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; font-size: 14px; }}
    th {{ background: var(--panel); font-size: 12px; color: var(--muted); white-space: nowrap; }}
    td.num {{ text-align: right; white-space: nowrap; }}
    ul {{ padding-left: 20px; margin: 8px 0; }}
    li {{ margin: 4px 0; font-size: 14px; }}
    @media (max-width: 700px) {{
      main {{ padding: 16px; }}
      h1 {{ font-size: 22px; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Formatting helpers                                                           #
# --------------------------------------------------------------------------- #


def _money(value: Decimal) -> str:
    return f"${value:,.2f}"


def _percent(value: Decimal) -> str:
    return f"{value:.2%}"


def _decimal(value: Decimal) -> str:
    return f"{value:.2f}"
