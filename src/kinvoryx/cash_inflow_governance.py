"""Governed pilot-readiness controls for the synthetic Spec 011 prototype."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
import hashlib
import json
from typing import Any

from kinvoryx.cash_inflow import DecisionBrief, HouseholdCase, PrototypePolicy


GOVERNANCE_VERSION = "cib-governance-1.0.0"


def _positive(name: str, value: Decimal) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


@dataclass(frozen=True)
class GovernedPolicy:
    """Approved, effective-dated wrapper around deterministic engine settings."""

    policy_id: str
    version: str
    effective_from: str
    approved_by_role: str
    safety_reserve_months: Decimal = Decimal("3")
    resilience_reserve_months: Decimal = Decimal("6")
    goal_first_minimum_reserve_months: Decimal = Decimal("1")
    high_cost_debt_rate: Decimal = Decimal("0.07")
    job_loss_months: Decimal = Decimal("3")
    market_decline_rate: Decimal = Decimal("0.20")
    goal_cost_increase_rate: Decimal = Decimal("0.10")

    def __post_init__(self) -> None:
        for field in ("policy_id", "version", "effective_from", "approved_by_role"):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} is required")
        try:
            datetime.fromisoformat(self.effective_from.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("effective_from must be an ISO-8601 timestamp") from exc
        for field in (
            "safety_reserve_months",
            "resilience_reserve_months",
            "goal_first_minimum_reserve_months",
            "job_loss_months",
        ):
            _positive(field, getattr(self, field))
        for field in ("high_cost_debt_rate", "market_decline_rate", "goal_cost_increase_rate"):
            value = getattr(self, field)
            if value < 0 or value > 1:
                raise ValueError(f"{field} must be between zero and one")
        if self.resilience_reserve_months < self.safety_reserve_months:
            raise ValueError("resilience reserve target cannot be below safety target")

    def engine_policy(self) -> PrototypePolicy:
        """Return the exact deterministic settings consumed by the engine."""
        return PrototypePolicy(
            safety_reserve_months=self.safety_reserve_months,
            resilience_reserve_months=self.resilience_reserve_months,
            goal_first_minimum_reserve_months=self.goal_first_minimum_reserve_months,
            high_cost_debt_rate=self.high_cost_debt_rate,
            job_loss_months=self.job_loss_months,
            market_decline_rate=self.market_decline_rate,
            goal_cost_increase_rate=self.goal_cost_increase_rate,
        )


@dataclass(frozen=True)
class JurisdictionCoverage:
    """Explicit claim boundary for one decision type and jurisdiction."""

    jurisdiction: str
    decision_type: str
    status: str
    effective_as_of: str
    supported_claims: tuple[str, ...]
    unsupported_claims: tuple[str, ...]
    source_refs: tuple[str, ...]
    reviewed_by_role: str

    def __post_init__(self) -> None:
        if self.status not in {"prototype", "reviewed", "suspended"}:
            raise ValueError("unsupported jurisdiction coverage status")
        if not all((self.jurisdiction, self.decision_type, self.effective_as_of, self.reviewed_by_role)):
            raise ValueError("jurisdiction coverage identity and review fields are required")
        if not self.supported_claims or not self.unsupported_claims or not self.source_refs:
            raise ValueError("coverage requires supported, unsupported, and source entries")


class ReviewState(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    REJECTED = "rejected"


_TRANSITIONS = {
    ReviewState.DRAFT: {ReviewState.SUBMITTED},
    ReviewState.SUBMITTED: {
        ReviewState.CHANGES_REQUESTED,
        ReviewState.APPROVED,
        ReviewState.REJECTED,
    },
    ReviewState.CHANGES_REQUESTED: {ReviewState.SUBMITTED},
    ReviewState.APPROVED: set(),
    ReviewState.REJECTED: set(),
}


@dataclass(frozen=True)
class ReviewEvent:
    event_id: str
    from_state: ReviewState
    to_state: ReviewState
    actor_role: str
    reason: str
    occurred_at: str


def transition_review(
    current: ReviewState,
    target: ReviewState,
    *,
    event_id: str,
    actor_role: str,
    reason: str,
    occurred_at: str,
) -> ReviewEvent:
    """Apply the fail-closed human-review state machine."""
    if target not in _TRANSITIONS[current]:
        raise ValueError(f"invalid review transition: {current.value} -> {target.value}")
    if not all(value.strip() for value in (event_id, actor_role, reason, occurred_at)):
        raise ValueError("review event identity, actor, reason, and timestamp are required")
    return ReviewEvent(event_id, current, target, actor_role, reason, occurred_at)


REQUIRED_PRIVACY_CONTROLS = frozenset(
    {
        "synthetic_data_only",
        "no_persistence",
        "no_external_transmission",
        "no_secrets_or_pii",
        "manual_deletion_verified",
    }
)


@dataclass(frozen=True)
class PrivacySecurityReview:
    review_id: str
    reviewer_role: str
    reviewed_at: str
    approved_controls: frozenset[str]
    open_findings: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return REQUIRED_PRIVACY_CONTROLS <= self.approved_controls and not self.open_findings


@dataclass(frozen=True)
class AuditRecord:
    audit_id: str
    case_id: str
    created_at: str
    calculation_version: str
    governance_version: str
    policy_id: str
    policy_version: str
    jurisdiction: str
    input_sha256: str
    output_sha256: str
    review_state: ReviewState


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, (Decimal, Enum)):
        return str(value.value if isinstance(value, Enum) else value)
    return value


def _sha256(value: Any) -> str:
    payload = json.dumps(_json_value(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_audit_record(
    household: HouseholdCase,
    brief: DecisionBrief,
    policy: GovernedPolicy,
    coverage: JurisdictionCoverage,
    *,
    audit_id: str,
    created_at: str | None = None,
    calculation_version: str = "cib-core-1.0.0",
    review_state: ReviewState = ReviewState.DRAFT,
) -> AuditRecord:
    """Create a tamper-evident metadata record without retaining raw case data."""
    if household.case_id != brief.case_id:
        raise ValueError("household and decision brief case identifiers must match")
    if not audit_id.strip():
        raise ValueError("audit_id is required")
    return AuditRecord(
        audit_id=audit_id,
        case_id=household.case_id,
        created_at=created_at or datetime.now(timezone.utc).isoformat(),
        calculation_version=calculation_version,
        governance_version=GOVERNANCE_VERSION,
        policy_id=policy.policy_id,
        policy_version=policy.version,
        jurisdiction=coverage.jurisdiction,
        input_sha256=_sha256(household),
        output_sha256=_sha256(brief),
        review_state=review_state,
    )


@dataclass(frozen=True)
class PilotGateResult:
    ready: bool
    blockers: tuple[str, ...]


def evaluate_pilot_gate(
    *,
    coverage: JurisdictionCoverage,
    privacy_review: PrivacySecurityReview,
    review_state: ReviewState,
    validation_passed: bool,
    unresolved_annotation_count: int,
) -> PilotGateResult:
    """Combine Slice D evidence; every unmet control fails closed."""
    blockers: list[str] = []
    if coverage.status != "reviewed":
        blockers.append("jurisdiction coverage is not reviewed")
    if not privacy_review.passed:
        blockers.append("privacy/security review is incomplete")
    if review_state != ReviewState.APPROVED:
        blockers.append("human review is not approved")
    if not validation_passed:
        blockers.append("deterministic validation did not pass")
    if unresolved_annotation_count:
        blockers.append("unresolved high-severity reviewer annotations remain")
    return PilotGateResult(ready=not blockers, blockers=tuple(blockers))
