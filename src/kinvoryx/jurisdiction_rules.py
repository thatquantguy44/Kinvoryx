"""Jurisdiction intelligence placeholder — Spec 006 stub.

Federal 2024 contribution limits and simplified marginal bracket lookup.
A full jurisdiction registry with coverage claims, legal sourcing, and
multi-jurisdiction support is deferred to Spec 006.

Information class: INSTITUTIONAL_POLICY. Not legal or tax advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from kinvoryx.household_state import FilingStatus


ZERO = Decimal("0")


@dataclass(frozen=True)
class ContributionLimits:
    """IRS contribution limits for tax-advantaged accounts (employee side)."""

    k401_employee: Decimal
    ira: Decimal
    hsa_individual: Decimal
    hsa_family: Decimal


@dataclass(frozen=True)
class _Bracket:
    floor: Decimal
    ceiling: Optional[Decimal]
    rate: Decimal


@dataclass(frozen=True)
class JurisdictionRules:
    """
    Planning assumptions for one jurisdiction and tax year.

    Marginal rate estimates use only the standard deduction and federal
    ordinary income brackets. Does not model NIIT, AMT, FICA, or state taxes.
    Scope must be asserted explicitly; callers are responsible for confirming
    the household's jurisdiction falls within scope.
    """

    scope: str
    contribution_limits: ContributionLimits
    standard_deduction_single: Decimal
    standard_deduction_mfj: Decimal
    income_brackets_single: tuple[_Bracket, ...]
    income_brackets_mfj: tuple[_Bracket, ...]

    def marginal_rate(self, gross_income: Decimal, filing_status: FilingStatus) -> Decimal:
        """Estimated federal marginal ordinary income tax rate."""
        if filing_status == FilingStatus.MARRIED_FILING_JOINTLY:
            std = self.standard_deduction_mfj
            brackets = self.income_brackets_mfj
        else:
            std = self.standard_deduction_single
            brackets = self.income_brackets_single
        taxable = max(ZERO, gross_income - std)
        rate = brackets[0].rate
        for b in brackets:
            if taxable > b.floor:
                rate = b.rate
        return rate


def federal_rules_2024() -> JurisdictionRules:
    """
    Federal income tax rules for 2024. Source: IRS Rev. Proc. 2023-34.

    Scope: federal_income_2024. Standard deduction only; no deduction
    phase-outs, FICA, NIIT, or state taxes modeled.
    """
    return JurisdictionRules(
        scope="federal_income_2024",
        contribution_limits=ContributionLimits(
            k401_employee=Decimal("23000"),
            ira=Decimal("7000"),
            hsa_individual=Decimal("4150"),
            hsa_family=Decimal("8300"),
        ),
        standard_deduction_single=Decimal("14600"),
        standard_deduction_mfj=Decimal("29200"),
        income_brackets_single=(
            _Bracket(Decimal("0"),       Decimal("11600"),   Decimal("0.10")),
            _Bracket(Decimal("11600"),   Decimal("47150"),   Decimal("0.12")),
            _Bracket(Decimal("47150"),   Decimal("100525"),  Decimal("0.22")),
            _Bracket(Decimal("100525"),  Decimal("191950"),  Decimal("0.24")),
            _Bracket(Decimal("191950"),  Decimal("243725"),  Decimal("0.32")),
            _Bracket(Decimal("243725"),  Decimal("609350"),  Decimal("0.35")),
            _Bracket(Decimal("609350"),  None,               Decimal("0.37")),
        ),
        income_brackets_mfj=(
            _Bracket(Decimal("0"),       Decimal("23200"),   Decimal("0.10")),
            _Bracket(Decimal("23200"),   Decimal("94300"),   Decimal("0.12")),
            _Bracket(Decimal("94300"),   Decimal("201050"),  Decimal("0.22")),
            _Bracket(Decimal("201050"),  Decimal("383900"),  Decimal("0.24")),
            _Bracket(Decimal("383900"),  Decimal("487450"),  Decimal("0.32")),
            _Bracket(Decimal("487450"),  Decimal("731200"),  Decimal("0.35")),
            _Bracket(Decimal("731200"),  None,               Decimal("0.37")),
        ),
    )
