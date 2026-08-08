"""Manual-entry interface helpers for the Spec 011 cash-inflow brief."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Mapping, Sequence
from urllib.parse import parse_qs

from kinvoryx.cash_inflow import Debt, HouseholdCase, build_decision_brief
from kinvoryx.cash_inflow_rendering import (
    BriefRenderContext,
    SAFETY_DISCLOSURE,
    render_combined_html,
)


FORM_FIELDS = (
    "case_id",
    "cash_inflow",
    "monthly_essential_expenses",
    "liquid_reserves",
    "debts",
    "employer_match_contribution_room",
    "employer_match_rate",
    "tax_advantaged_contribution_room",
    "estimated_marginal_tax_rate",
    "near_term_goal_remaining",
)


@dataclass(frozen=True)
class ManualEntryResult:
    household: HouseholdCase | None
    errors: tuple[str, ...]
    values: dict[str, str]


def default_form_values() -> dict[str, str]:
    """Return a useful synthetic starting point for the manual-entry form."""
    return {
        "case_id": "synthetic-manual-case",
        "cash_inflow": "20000",
        "monthly_essential_expenses": "5000",
        "liquid_reserves": "5000",
        "debts": "credit_card,6000,0.24\nstudent_loan,12000,0.055",
        "employer_match_contribution_room": "6000",
        "employer_match_rate": "0.50",
        "tax_advantaged_contribution_room": "7000",
        "estimated_marginal_tax_rate": "0.24",
        "near_term_goal_remaining": "15000",
    }


def parse_manual_entry(form: Mapping[str, Sequence[str] | str]) -> ManualEntryResult:
    """Parse manual-entry fields into a synthetic household case."""
    values = _normalize_form_values(form)
    errors: list[str] = []
    debts: tuple[Debt, ...] = ()

    try:
        debts = parse_debt_rows(values["debts"])
    except ValueError as exc:
        errors.append(f"debts: {exc}")

    household = None
    if not values["case_id"].strip():
        errors.append("case_id: case identifier is required")

    if not errors:
        try:
            household = HouseholdCase(
                case_id=values["case_id"].strip(),
                cash_inflow=values["cash_inflow"],
                monthly_essential_expenses=values["monthly_essential_expenses"],
                liquid_reserves=values["liquid_reserves"],
                debts=debts,
                employer_match_contribution_room=values["employer_match_contribution_room"],
                employer_match_rate=values["employer_match_rate"],
                tax_advantaged_contribution_room=values["tax_advantaged_contribution_room"],
                estimated_marginal_tax_rate=values["estimated_marginal_tax_rate"],
                near_term_goal_remaining=values["near_term_goal_remaining"],
                synthetic=True,
            )
        except (ArithmeticError, ValueError) as exc:
            errors.append(str(exc))
    return ManualEntryResult(household, tuple(errors), values)


def parse_debt_rows(raw_rows: str) -> tuple[Debt, ...]:
    """Parse supported debts from lines formatted as identifier,balance,annual_rate."""
    debts: list[Debt] = []
    for line_number, raw_line in enumerate(raw_rows.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        parts = tuple(part.strip() for part in line.split(","))
        if len(parts) != 3:
            raise ValueError(
                f"line {line_number} must use identifier,balance,annual_rate"
            )
        try:
            debts.append(Debt(parts[0], parts[1], parts[2]))
        except ValueError as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
    return tuple(debts)


def render_manual_entry_form(
    values: Mapping[str, str] | None = None,
    errors: Sequence[str] = (),
) -> str:
    """Render the standalone manual-entry HTML form."""
    selected = default_form_values()
    if values is not None:
        selected.update({key: values.get(key, "") for key in FORM_FIELDS})

    error_html = ""
    if errors:
        error_html = (
            "<section class=\"errors\"><h2>Submission Errors</h2><ul>"
            + "".join(f"<li>{escape(error)}</li>" for error in errors)
            + "</ul></section>"
        )

    return _interface_document(
        "Cash Inflow Decision Brief",
        f"""
<main>
  <section class="intro">
    <h1>Cash Inflow Decision Brief</h1>
    <p>{escape(SAFETY_DISCLOSURE)}</p>
  </section>
  {error_html}
  <form method="post" action="/brief">
    <fieldset>
      <legend>Household Snapshot</legend>
      {_input("Case ID", "case_id", selected)}
      {_input("Cash inflow", "cash_inflow", selected)}
      {_input("Monthly essential expenses", "monthly_essential_expenses", selected)}
      {_input("Current liquid reserves", "liquid_reserves", selected)}
    </fieldset>
    <fieldset>
      <legend>Supported Debts</legend>
      <label>
        <span>Debt rows</span>
        <textarea name="debts" rows="4">{escape(selected["debts"])}</textarea>
      </label>
      <p class="hint">One debt per line: identifier,balance,annual_rate</p>
    </fieldset>
    <fieldset>
      <legend>Contribution and Goal Capacity</legend>
      {_input("Employer-match contribution room", "employer_match_contribution_room", selected)}
      {_input("Employer-match rate", "employer_match_rate", selected)}
      {_input("Tax-advantaged contribution room", "tax_advantaged_contribution_room", selected)}
      {_input("Estimated marginal tax rate", "estimated_marginal_tax_rate", selected)}
      {_input("Near-term goal remaining", "near_term_goal_remaining", selected)}
    </fieldset>
    <button type="submit">Generate comparison</button>
  </form>
</main>
""",
    )


def render_result_from_manual_entry(form: Mapping[str, Sequence[str] | str]) -> tuple[int, str]:
    """Render a decision brief or the form with field-level errors."""
    result = parse_manual_entry(form)
    if result.household is None:
        return HTTPStatus.BAD_REQUEST, render_manual_entry_form(result.values, result.errors)
    brief = build_decision_brief(result.household)
    context = BriefRenderContext(result.household, brief)
    return HTTPStatus.OK, _with_back_link(render_combined_html(context))


def serve_manual_entry(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    """Start the local manual-entry server."""
    server = ThreadingHTTPServer((host, port), _ManualEntryHandler)
    return server


class _ManualEntryHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in {"/", "/brief"}:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        self._send_html(HTTPStatus.OK, render_manual_entry_form())

    def do_POST(self) -> None:
        if self.path != "/brief":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        status, html = render_result_from_manual_entry(parse_qs(body))
        self._send_html(status, html)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, status: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _normalize_form_values(form: Mapping[str, Sequence[str] | str]) -> dict[str, str]:
    values = default_form_values()
    for field in FORM_FIELDS:
        raw_value = form.get(field, "")
        if isinstance(raw_value, str):
            values[field] = raw_value.strip()
        else:
            values[field] = raw_value[0].strip() if raw_value else ""
    return values


def _input(label: str, name: str, values: Mapping[str, str]) -> str:
    return f"""
      <label>
        <span>{escape(label)}</span>
        <input name="{escape(name)}" value="{escape(values[name])}">
      </label>
"""


def _with_back_link(html: str) -> str:
    return html.replace(
        "<main>",
        '<main><p class="nav"><a href="/">Enter another synthetic case</a></p>',
        1,
    )


def _interface_document(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #52616f;
      --line: #d7dee6;
      --panel: #f8fafc;
      --paper: #ffffff;
      --accent: #0f766e;
      --error: #7c2d12;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.45;
    }}
    main {{ max-width: 920px; margin: 0 auto; padding: 24px; }}
    h1 {{ margin: 0 0 10px; font-size: 28px; letter-spacing: 0; }}
    h2, legend {{ font-size: 18px; font-weight: 700; letter-spacing: 0; }}
    .intro {{ border-bottom: 1px solid var(--line); padding-bottom: 18px; margin-bottom: 18px; }}
    .intro p {{ border-left: 4px solid var(--accent); background: var(--panel); padding: 10px 12px; }}
    fieldset {{ border: 1px solid var(--line); margin: 16px 0; padding: 16px; }}
    label {{ display: grid; gap: 6px; margin: 10px 0; }}
    label span {{ color: var(--muted); font-size: 13px; }}
    input, textarea {{
      width: 100%;
      border: 1px solid var(--line);
      padding: 10px;
      font: inherit;
      color: var(--ink);
      background: #fff;
    }}
    textarea {{ resize: vertical; min-height: 96px; }}
    button {{
      border: 0;
      background: var(--accent);
      color: #fff;
      padding: 11px 14px;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }}
    .hint, .nav {{ color: var(--muted); }}
    .errors {{ border: 1px solid #fed7aa; background: #fff7ed; color: var(--error); padding: 12px; }}
    a {{ color: var(--accent); }}
    @media (max-width: 700px) {{
      main {{ padding: 16px; }}
      h1 {{ font-size: 23px; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""
