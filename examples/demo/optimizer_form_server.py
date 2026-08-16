"""
Interactive form server for the Kinvoryx Capital Allocation Optimizer.

Usage:
    python examples/demo/optimizer_form_server.py
    python examples/demo/optimizer_form_server.py --port 9000

Opens in browser:  http://localhost:8080/
Opens on iPhone:   http://<printed-ip>:8080/   (same Wi-Fi)
"""

from __future__ import annotations

import http.server
import socket
import socketserver
import sys
import urllib.parse
from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from kinvoryx.household_state import (
    Account, AccountType, DataProvenance, DebtCategory, Expense,
    ExpenseCategory, EmployerBenefit, EmployerMatchTier, FieldValue,
    FilingStatus, Freshness, Goal, GoalFlexibility, GoalPriority,
    HouseholdDebt, HouseholdMember, HouseholdState, IncomeSource,
    IncomeType, InformationClass, MemberRole, TaxProfile,
)
from kinvoryx.jurisdiction_rules import federal_rules_2024
from kinvoryx.capital_allocation_optimizer import optimize_household_allocation
from kinvoryx.optimizer_rendering import (
    OptimizerRenderContext, render_combined_html,
)

RULES = federal_rules_2024()
TODAY = date.today()
MAX_INCOME = 3
MAX_DEBT = 4
MAX_GOAL = 3


# --------------------------------------------------------------------------- #
# Parsing helpers                                                              #
# --------------------------------------------------------------------------- #

def _get(fields: dict, key: str, default: str = "") -> str:
    vals = fields.get(key, [])
    return vals[0].strip() if vals else default


def _dec(s: str, default: str = "0") -> Decimal:
    try:
        v = Decimal(s.replace(",", "").replace("$", "").strip())
        return v if v >= 0 else Decimal(default)
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _int(s: str, default: int = 0) -> int:
    try:
        return int(s.strip())
    except (ValueError, AttributeError):
        return default


def _fv(amount: Decimal) -> FieldValue:
    return FieldValue(
        value=amount,
        provenance=DataProvenance.USER_ENTERED,
        information_class=InformationClass.HOUSEHOLD_CONFIG,
        source="form",
        effective_date=TODAY,
        freshness=Freshness.CURRENT,
        owner="primary",
    )


_INCOME_TYPE_MAP = {
    "salary":           IncomeType.SALARY,
    "bonus":            IncomeType.BONUS,
    "equity_vesting":   IncomeType.EQUITY_VESTING,
    "self_employment":  IncomeType.SELF_EMPLOYMENT,
    "rental":           IncomeType.RENTAL,
    "other":            IncomeType.OTHER,
}

_DEBT_CAT_MAP = {
    "credit_card":    DebtCategory.CREDIT_CARD,
    "student_loan":   DebtCategory.STUDENT_LOAN,
    "mortgage":       DebtCategory.MORTGAGE,
    "auto":           DebtCategory.AUTO,
    "personal_loan":  DebtCategory.PERSONAL_LOAN,
    "other":          DebtCategory.OTHER,
}

_GOAL_PRI_MAP = {
    "critical": GoalPriority.CRITICAL,
    "high":     GoalPriority.HIGH,
    "medium":   GoalPriority.MEDIUM,
    "low":      GoalPriority.LOW,
}

_FLEX_MAP = {
    "critical": GoalFlexibility.FIXED,
    "high":     GoalFlexibility.DATE_FLEXIBLE,
    "medium":   GoalFlexibility.AMOUNT_FLEXIBLE,
    "low":      GoalFlexibility.FULLY_FLEXIBLE,
}

_FILING_MAP = {
    "mfj":   FilingStatus.MARRIED_FILING_JOINTLY,
    "single": FilingStatus.SINGLE,
    "hoh":   FilingStatus.HEAD_OF_HOUSEHOLD,
    "mfs":   FilingStatus.MARRIED_FILING_SEPARATELY,
}


def parse_and_run(fields: dict) -> str:
    """Build a HouseholdState from form fields, run the optimizer, return HTML."""

    # ── Members ────────────────────────────────────────────────────────────
    primary_year = _int(_get(fields, "primary_birth_year"), 1985)
    partner_year_str = _get(fields, "partner_birth_year")
    has_partner = bool(partner_year_str)

    members: list[HouseholdMember] = [
        HouseholdMember(member_id="primary", role=MemberRole.PRIMARY,
                        birth_year=primary_year),
    ]
    if has_partner:
        members.append(HouseholdMember(member_id="partner", role=MemberRole.PARTNER,
                                       birth_year=_int(partner_year_str, 1985)))

    filing_key = _get(fields, "filing_status", "mfj")
    filing_status = _FILING_MAP.get(filing_key, FilingStatus.MARRIED_FILING_JOINTLY)

    # ── Income sources ──────────────────────────────────────────────────────
    income_sources: list[IncomeSource] = []
    for i in range(MAX_INCOME):
        label = _get(fields, f"income_label_{i}")
        gross_str = _get(fields, f"income_gross_{i}")
        if not label or not gross_str:
            continue
        itype = _INCOME_TYPE_MAP.get(_get(fields, f"income_type_{i}", "salary"), IncomeType.SALARY)
        member = _get(fields, f"income_member_{i}", "primary")
        if member == "partner" and not has_partner:
            member = "primary"
        income_sources.append(IncomeSource(
            source_id=f"income-{i}",
            member_id=member,
            income_type=itype,
            annual_gross=_fv(_dec(gross_str)),
            work_jurisdiction="US",
        ))

    if not income_sources:
        income_sources.append(IncomeSource(
            source_id="income-0", member_id="primary",
            income_type=IncomeType.SALARY,
            annual_gross=_fv(Decimal("0")),
            work_jurisdiction="US",
        ))

    # ── Expenses ────────────────────────────────────────────────────────────
    monthly_essential = _dec(_get(fields, "monthly_essential", "0"))
    expenses = (Expense(
        expense_id="essential",
        category=ExpenseCategory.ESSENTIAL,
        label="Monthly essential expenses",
        monthly_amount=_fv(monthly_essential),
    ),)

    # ── Liquid savings (reserve account) ───────────────────────────────────
    liquid = _dec(_get(fields, "liquid_savings", "0"))
    accounts = (Account(
        account_id="cash",
        account_type=AccountType.CASH,
        owner_member_id="primary",
        balance=_fv(liquid),
    ),)

    # ── Employer 401(k) benefit ─────────────────────────────────────────────
    benefits: list[EmployerBenefit] = []
    for i, member_id in enumerate(["primary"] + (["partner"] if has_partner else [])):
        key = f"benefit_401k_{member_id}"
        if _get(fields, key) == "on":
            match_rate_str = _get(fields, f"benefit_match_rate_{member_id}", "50")
            match_cap_str = _get(fields, f"benefit_match_cap_{member_id}", "6")
            match_rate = _dec(match_rate_str) / Decimal("100")
            match_cap = _dec(match_cap_str) / Decimal("100")
            benefits.append(EmployerBenefit(
                benefit_id=f"401k-{member_id}",
                member_id=member_id,
                plan_type="401k",
                annual_employee_limit=_fv(Decimal("23000")),
                match_tiers=(EmployerMatchTier(
                    match_rate=match_rate,
                    up_to_percent_of_salary=match_cap,
                ),),
            ))

    # ── Debts ───────────────────────────────────────────────────────────────
    debts: list[HouseholdDebt] = []
    for i in range(MAX_DEBT):
        label = _get(fields, f"debt_label_{i}")
        balance_str = _get(fields, f"debt_balance_{i}")
        apr_str = _get(fields, f"debt_apr_{i}")
        if not label or not balance_str:
            continue
        cat = _DEBT_CAT_MAP.get(_get(fields, f"debt_category_{i}", "other"), DebtCategory.OTHER)
        apr = _dec(apr_str) / Decimal("100")
        minimum = _dec(_get(fields, f"debt_min_{i}", "0"))
        debts.append(HouseholdDebt(
            debt_id=f"debt-{i}",
            category=cat,
            label=label,
            balance=_fv(_dec(balance_str)),
            annual_rate=_fv(apr),
            monthly_minimum=_fv(minimum),
        ))

    # ── Goals ───────────────────────────────────────────────────────────────
    goals: list[Goal] = []
    for i in range(MAX_GOAL):
        label = _get(fields, f"goal_label_{i}")
        amount_str = _get(fields, f"goal_amount_{i}")
        if not label or not amount_str:
            continue
        pri_key = _get(fields, f"goal_priority_{i}", "medium")
        goals.append(Goal(
            goal_id=f"goal-{i}",
            label=label,
            target_amount=_fv(_dec(amount_str)),
            priority=_GOAL_PRI_MAP.get(pri_key, GoalPriority.MEDIUM),
            flexibility=_FLEX_MAP.get(pri_key, GoalFlexibility.AMOUNT_FLEXIBLE),
            owner_member_ids=("primary",),
            horizon_years=_int(_get(fields, f"goal_horizon_{i}", "5"), 5),
        ))

    if not goals:
        goals.append(Goal(
            goal_id="goal-0", label="General savings",
            target_amount=_fv(Decimal("10000")),
            priority=GoalPriority.MEDIUM, flexibility=GoalFlexibility.FULLY_FLEXIBLE,
            owner_member_ids=("primary",), horizon_years=5,
        ))

    # ── Assemble household ──────────────────────────────────────────────────
    hid = f"form-{TODAY.strftime('%Y%m%d')}"
    household = HouseholdState(
        household_id=hid,
        synthetic=True,
        members=tuple(members),
        income_sources=tuple(income_sources),
        expenses=expenses,
        accounts=accounts,
        debts=tuple(debts),
        benefits=tuple(benefits),
        goals=tuple(goals),
        constraints=(),
        tax_profile=TaxProfile(
            filing_status=filing_status,
            domicile_state="US",
            work_state="US",
        ),
    )

    result = optimize_household_allocation(household, RULES)
    ctx = OptimizerRenderContext(household=household, result=result)
    brief = render_combined_html(ctx)

    # Inject a back link at the top of the brief body
    back = (
        '<div style="padding:10px 20px;background:#f0f4f8;border-bottom:1px solid #c5d3de;">'
        '<a href="/" style="font-size:13px;color:#0c7057;text-decoration:none;font-family:'
        'ui-sans-serif,sans-serif;">&#8592; Edit inputs</a></div>'
    )
    return brief.replace("<body>", f"<body>{back}", 1)


# --------------------------------------------------------------------------- #
# Form HTML                                                                    #
# --------------------------------------------------------------------------- #

_FORM_CSS = """
:root {
  --bg: #F4F7FB; --surface: #FFFFFF; --surface-alt: #EBF0F7;
  --ink: #1B2736; --ink-2: #4D6070; --ink-3: #8298AC;
  --border: #C5D3DE; --accent: #0C7057; --accent-bg: #E0F0EB;
  --num-font: ui-monospace,"SF Mono",Menlo,monospace;
  --radius: 7px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0F1923; --surface: #182130; --surface-alt: #1E2B3C;
    --ink: #E0E8F0; --ink-2: #8099AE; --ink-3: #4D6070;
    --border: #253645; --accent: #12C08C; --accent-bg: #0B2922;
  }
}
:root[data-theme="dark"] {
  --bg: #0F1923; --surface: #182130; --surface-alt: #1E2B3C;
  --ink: #E0E8F0; --ink-2: #8099AE; --ink-3: #4D6070;
  --border: #253645; --accent: #12C08C; --accent-bg: #0B2922;
}
*, *::before, *::after { box-sizing: border-box; }
body {
  background: var(--bg); color: var(--ink); margin: 0;
  font-family: ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size: 15px; line-height: 1.5;
}
.wrap { max-width: 680px; margin: 0 auto; padding: 24px 20px 80px; }
header { padding-bottom: 20px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
header h1 { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; margin: 0 0 4px; }
header p  { font-size: 13px; color: var(--ink-2); margin: 0; }
.section {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px; margin-bottom: 14px;
}
.section h2 {
  font-size: 13px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--ink-3); margin: 0 0 16px;
}
.grid { display: grid; gap: 12px; }
.grid-2 { grid-template-columns: 1fr 1fr; }
.grid-3 { grid-template-columns: 1fr 1fr 1fr; }
.field { display: flex; flex-direction: column; gap: 4px; }
.field label {
  font-size: 12px; font-weight: 550; color: var(--ink-2);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.field input, .field select {
  height: 44px; padding: 0 12px;
  border: 1px solid var(--border); border-radius: 6px;
  background: var(--bg); color: var(--ink);
  font-size: 15px; font-family: inherit;
  transition: border-color 0.12s, box-shadow 0.12s;
  -webkit-appearance: none; appearance: none;
}
.field input:focus, .field select:focus {
  outline: none; border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-bg);
}
.field input[type=number] { font-family: var(--num-font); }
.field .hint { font-size: 11px; color: var(--ink-3); }
.slot {
  padding: 14px; border: 1px solid var(--border);
  border-radius: 6px; background: var(--surface-alt);
  margin-bottom: 8px;
}
.slot-header {
  font-size: 12px; font-weight: 600; color: var(--ink-3);
  text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: 10px;
}
.slot.hidden { display: none; }
.add-btn {
  display: inline-flex; align-items: center; gap: 5px;
  background: none; border: 1px dashed var(--border); border-radius: 6px;
  padding: 8px 14px; font-size: 13px; color: var(--ink-2);
  cursor: pointer; transition: border-color 0.12s, color 0.12s; width: 100%;
  justify-content: center; margin-top: 4px;
}
.add-btn:hover { border-color: var(--accent); color: var(--accent); }
.check-row { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.check-row input[type=checkbox] { width: 18px; height: 18px; cursor: pointer; }
.check-row label { font-size: 14px; color: var(--ink); cursor: pointer; }
.match-fields { padding-left: 26px; }
.match-fields.hidden { display: none; }
.divider { border: none; border-top: 1px solid var(--border); margin: 14px 0; }
.submit-btn {
  width: 100%; height: 52px; background: var(--accent); color: #fff;
  border: none; border-radius: var(--radius); font-size: 16px; font-weight: 600;
  cursor: pointer; margin-top: 8px; letter-spacing: -0.01em;
  transition: opacity 0.12s;
}
.submit-btn:hover { opacity: 0.88; }
.submit-btn:active { opacity: 0.75; }
.disclosure {
  font-size: 12px; color: var(--ink-3); text-align: center;
  margin-top: 12px; line-height: 1.4;
}
.member-select select { background: var(--bg); }
@media (max-width: 520px) {
  .wrap { padding: 16px 14px 80px; }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  header h1 { font-size: 19px; }
}
"""

_FORM_JS = """
function addSlot(groupId, max) {
  const slots = document.querySelectorAll('#' + groupId + ' .slot');
  for (let i = 0; i < slots.length; i++) {
    if (slots[i].classList.contains('hidden')) {
      slots[i].classList.remove('hidden');
      slots[i].querySelectorAll('input,select').forEach(el => el.disabled = false);
      if (i === max - 1) {
        document.getElementById('add-' + groupId).style.display = 'none';
      }
      return;
    }
  }
}

function toggleMatch(memberId) {
  const cb = document.getElementById('benefit_401k_' + memberId);
  const fields = document.getElementById('match_fields_' + memberId);
  if (cb && fields) {
    fields.classList.toggle('hidden', !cb.checked);
  }
}

// Disable hidden slot inputs on load so they don't submit empty values
document.querySelectorAll('.slot.hidden input, .slot.hidden select').forEach(el => {
  el.disabled = true;
});
"""


def _select(name: str, options: list[tuple[str, str]], selected: str = "") -> str:
    opts = "".join(
        f'<option value="{v}"{" selected" if v == selected else ""}>{e(label)}</option>'
        for v, label in options
    )
    return f'<select name="{name}">{opts}</select>'


def e(s: str) -> str:
    return escape(str(s))


def _income_slot(i: int, hidden: bool = False) -> str:
    cls = "slot hidden" if hidden else "slot"
    member_opts = [("primary", "You"), ("partner", "Partner")]
    type_opts = [
        ("salary", "Salary"),
        ("bonus", "Bonus"),
        ("equity_vesting", "Equity / RSU vesting"),
        ("self_employment", "Self-employment"),
        ("rental", "Rental income"),
        ("other", "Other"),
    ]
    return f"""
<div class="{cls}">
  <div class="slot-header">Source {i + 1}</div>
  <div class="grid grid-2">
    <div class="field" style="grid-column:1/-1">
      <label>Description</label>
      <input type="text" name="income_label_{i}" placeholder="e.g. Base salary">
    </div>
    <div class="field">
      <label>Type</label>
      {_select(f"income_type_{i}", type_opts)}
    </div>
    <div class="field">
      <label>Annual gross ($)</label>
      <input type="number" name="income_gross_{i}" placeholder="120000" min="0" step="1000">
    </div>
    <div class="field member-select">
      <label>Earner</label>
      {_select(f"income_member_{i}", member_opts)}
    </div>
  </div>
</div>"""


def _debt_slot(i: int, hidden: bool = False) -> str:
    cls = "slot hidden" if hidden else "slot"
    cat_opts = [
        ("credit_card", "Credit card"),
        ("student_loan", "Student loan"),
        ("mortgage", "Mortgage"),
        ("auto", "Auto loan"),
        ("personal_loan", "Personal loan"),
        ("other", "Other"),
    ]
    return f"""
<div class="{cls}">
  <div class="slot-header">Debt {i + 1}</div>
  <div class="grid grid-2">
    <div class="field" style="grid-column:1/-1">
      <label>Name</label>
      <input type="text" name="debt_label_{i}" placeholder="e.g. Chase Sapphire card">
    </div>
    <div class="field">
      <label>Type</label>
      {_select(f"debt_category_{i}", cat_opts)}
    </div>
    <div class="field">
      <label>Balance ($)</label>
      <input type="number" name="debt_balance_{i}" placeholder="8000" min="0" step="100">
    </div>
    <div class="field">
      <label>APR (%)</label>
      <input type="number" name="debt_apr_{i}" placeholder="24.9" min="0" max="100" step="0.1">
    </div>
    <div class="field">
      <label>Monthly minimum ($)</label>
      <input type="number" name="debt_min_{i}" placeholder="200" min="0" step="10">
    </div>
  </div>
</div>"""


def _goal_slot(i: int, hidden: bool = False) -> str:
    cls = "slot hidden" if hidden else "slot"
    pri_opts = [
        ("critical", "Critical — must achieve"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    return f"""
<div class="{cls}">
  <div class="slot-header">Goal {i + 1}</div>
  <div class="grid grid-2">
    <div class="field" style="grid-column:1/-1">
      <label>Goal</label>
      <input type="text" name="goal_label_{i}" placeholder="e.g. Home down payment">
    </div>
    <div class="field">
      <label>Target amount ($)</label>
      <input type="number" name="goal_amount_{i}" placeholder="80000" min="0" step="1000">
    </div>
    <div class="field">
      <label>Priority</label>
      {_select(f"goal_priority_{i}", pri_opts)}
    </div>
    <div class="field">
      <label>Horizon (years)</label>
      <input type="number" name="goal_horizon_{i}" placeholder="5" min="1" max="40" step="1">
    </div>
  </div>
</div>"""


def _benefit_fields(member_id: str, label: str) -> str:
    return f"""
<div>
  <div class="check-row">
    <input type="checkbox" id="benefit_401k_{member_id}" name="benefit_401k_{member_id}"
           value="on" onchange="toggleMatch('{member_id}')">
    <label for="benefit_401k_{member_id}">{e(label)} has a 401(k) with employer match</label>
  </div>
  <div class="match-fields hidden" id="match_fields_{member_id}">
    <div class="grid grid-2">
      <div class="field">
        <label>Match rate (%)</label>
        <input type="number" name="benefit_match_rate_{member_id}" value="50" min="0" max="100" step="5">
        <span class="hint">e.g. 50 = dollar-for-50-cents</span>
      </div>
      <div class="field">
        <label>Up to (% of salary)</label>
        <input type="number" name="benefit_match_cap_{member_id}" value="6" min="0" max="100" step="1">
        <span class="hint">e.g. 6 = first 6% of salary matched</span>
      </div>
    </div>
  </div>
</div>"""


def build_form_html(error: str = "") -> str:
    filing_opts = [
        ("mfj",    "Married filing jointly"),
        ("single", "Single"),
        ("hoh",    "Head of household"),
        ("mfs",    "Married filing separately"),
    ]
    error_html = (
        f'<div style="background:#fdeee9;border-left:3px solid #922810;padding:10px 14px;'
        f'border-radius:0 5px 5px 0;margin-bottom:14px;font-size:13px;color:#922810;">'
        f'{e(error)}</div>'
    ) if error else ""

    income_slots = "".join(_income_slot(i, hidden=(i > 0)) for i in range(MAX_INCOME))
    debt_slots   = "".join(_debt_slot(i,   hidden=(i > 0)) for i in range(MAX_DEBT))
    goal_slots   = "".join(_goal_slot(i,   hidden=(i > 0)) for i in range(MAX_GOAL))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kinvoryx — Allocation Brief</title>
  <style>{_FORM_CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Household Allocation Brief</h1>
    <p>Enter your household details to see how four allocation strategies compare
       across your income, debts, and goals.</p>
  </header>

  {error_html}

  <form method="post" action="/">

    <!-- Personal -->
    <div class="section">
      <h2>About you</h2>
      <div class="grid grid-3">
        <div class="field">
          <label>Filing status</label>
          {_select("filing_status", filing_opts)}
        </div>
        <div class="field">
          <label>Your birth year</label>
          <input type="number" name="primary_birth_year" placeholder="1985" min="1940" max="2006" step="1">
        </div>
        <div class="field">
          <label>Partner birth year</label>
          <input type="number" name="partner_birth_year" placeholder="Optional" min="1940" max="2006" step="1">
        </div>
      </div>
    </div>

    <!-- Income -->
    <div class="section">
      <h2>Income</h2>
      <div id="income-group">
        {income_slots}
      </div>
      <button type="button" class="add-btn" id="add-income-group"
              onclick="addSlot('income-group', {MAX_INCOME})">
        + Add income source
      </button>
    </div>

    <!-- Expenses + Savings -->
    <div class="section">
      <h2>Spending &amp; savings</h2>
      <div class="grid grid-2">
        <div class="field">
          <label>Monthly essential expenses ($)</label>
          <input type="number" name="monthly_essential" placeholder="5000" min="0" step="100">
          <span class="hint">Rent, groceries, utilities, transport, insurance, childcare</span>
        </div>
        <div class="field">
          <label>Liquid savings / checking ($)</label>
          <input type="number" name="liquid_savings" placeholder="15000" min="0" step="500">
          <span class="hint">Used to calculate your current emergency reserve</span>
        </div>
      </div>
    </div>

    <!-- Benefits -->
    <div class="section">
      <h2>Employer benefits</h2>
      {_benefit_fields("primary", "You")}
      <hr class="divider">
      {_benefit_fields("partner", "Partner")}
    </div>

    <!-- Debts -->
    <div class="section">
      <h2>Debts</h2>
      <div id="debt-group">
        {debt_slots}
      </div>
      <button type="button" class="add-btn" id="add-debt-group"
              onclick="addSlot('debt-group', {MAX_DEBT})">
        + Add debt
      </button>
    </div>

    <!-- Goals -->
    <div class="section">
      <h2>Goals</h2>
      <div id="goal-group">
        {goal_slots}
      </div>
      <button type="button" class="add-btn" id="add-goal-group"
              onclick="addSlot('goal-group', {MAX_GOAL})">
        + Add goal
      </button>
    </div>

    <button type="submit" class="submit-btn">Generate Brief</button>
    <p class="disclosure">
      Synthetic decision-support prototype only. Not financial, tax, or legal advice.
      All inputs are used locally and not stored.
    </p>

  </form>
</div>
<script>{_FORM_JS}</script>
</body>
</html>"""


# --------------------------------------------------------------------------- #
# HTTP handler                                                                 #
# --------------------------------------------------------------------------- #

class _Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = build_form_html().encode("utf-8")
        self._respond(200, "text/html; charset=utf-8", body)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        fields = urllib.parse.parse_qs(raw, keep_blank_values=True)
        try:
            html = parse_and_run(fields)
            body = html.encode("utf-8")
            self._respond(200, "text/html; charset=utf-8", body)
        except Exception as exc:
            error = f"Could not compute brief: {exc}"
            body = build_form_html(error=error).encode("utf-8")
            self._respond(400, "text/html; charset=utf-8", body)

    def _respond(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        pass


# --------------------------------------------------------------------------- #
# Entry point                                                                  #
# --------------------------------------------------------------------------- #

def _local_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "localhost"


def main() -> None:
    port = 8080
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])

    ip = _local_ip()
    print(f"Form server running.")
    print(f"  Local:   http://localhost:{port}/")
    print(f"  On phone: http://{ip}:{port}/  (same Wi-Fi)")
    print("Ctrl-C to stop.\n")

    with socketserver.TCPServer(("", port), _Handler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")


if __name__ == "__main__":
    main()
