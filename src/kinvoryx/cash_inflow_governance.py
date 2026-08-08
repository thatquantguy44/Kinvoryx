"""Governed pilot-readiness controls for the synthetic Spec 011 prototype."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
import hashlib
import json
from typing import Any, Iterable

from kinvoryx.cash_inflow import (
    DecisionBrief,
    HouseholdCase,
    PrototypePolicy,
    build_decision_brief,
)
from kinvoryx.cash_inflow_validation import (
    ReviewerAnnotation,
    ValidationEvidence,
    unresolved_pilot_blockers,
    validate_decision_brief,
)


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
    validation_sha256: str | None
    annotations_sha256: str | None
    privacy_review_sha256: str | None
    review_events_sha256: str | None
    coverage_sha256: str | None
    policy_sha256: str | None
    review_state: ReviewState


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_json_value(item) for item in value)
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
    validation: ValidationEvidence | None = None,
    annotations: tuple[ReviewerAnnotation, ...] | None = None,
    privacy_review: PrivacySecurityReview | None = None,
    review_events: tuple[ReviewEvent, ...] | None = None,
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
        validation_sha256=_sha256(validation) if validation is not None else None,
        annotations_sha256=_sha256(annotations) if annotations is not None else None,
        privacy_review_sha256=_sha256(privacy_review) if privacy_review is not None else None,
        review_events_sha256=_sha256(review_events) if review_events is not None else None,
        coverage_sha256=_sha256(coverage),
        policy_sha256=_sha256(policy),
        review_state=review_state,
    )


@dataclass(frozen=True)
class PilotGateResult:
    ready: bool
    blockers: tuple[str, ...]


@dataclass(frozen=True)
class GovernedWorkflowEvidence:
    """One immutable evidence graph for a case and its calculation."""

    workflow_id: str
    household: HouseholdCase
    policy: GovernedPolicy
    coverage: JurisdictionCoverage
    brief: DecisionBrief
    validation: ValidationEvidence
    annotations: tuple[ReviewerAnnotation, ...]
    privacy_review: PrivacySecurityReview
    review_events: tuple[ReviewEvent, ...]
    audit: AuditRecord


@dataclass(frozen=True)
class GovernedDecisionBrief:
    """Completed governed workflow and its evidence-derived pilot gate."""

    evidence: GovernedWorkflowEvidence
    pilot_gate: PilotGateResult


def _review_state(events: tuple[ReviewEvent, ...]) -> tuple[ReviewState, list[str]]:
    blockers: list[str] = []
    current = ReviewState.DRAFT
    seen_ids: set[str] = set()
    for event in events:
        if event.event_id in seen_ids:
            blockers.append("review event identifiers are not unique")
        seen_ids.add(event.event_id)
        if event.from_state != current or event.to_state not in _TRANSITIONS[current]:
            blockers.append("review event chain is invalid")
            break
        current = event.to_state
    return current, blockers


def evaluate_pilot_gate(evidence: GovernedWorkflowEvidence) -> PilotGateResult:
    """Evaluate retained evidence, never caller-supplied readiness summaries."""
    blockers: list[str] = []
    if evidence.coverage.status != "reviewed":
        blockers.append("jurisdiction coverage is not reviewed")
    if evidence.coverage.decision_type != "post-tax-cash-inflow-comparison":
        blockers.append("jurisdiction coverage does not support this decision type")
    if not evidence.privacy_review.passed:
        blockers.append("privacy/security review is incomplete")
    review_state, review_blockers = _review_state(evidence.review_events)
    blockers.extend(review_blockers)
    if review_state != ReviewState.APPROVED:
        blockers.append("human review is not approved")
    if evidence.validation.case_id != evidence.household.case_id:
        blockers.append("validation evidence belongs to a different case")
    if evidence.validation.brief != evidence.brief:
        blockers.append("validation evidence belongs to a different calculation")
    if not evidence.validation.passed:
        blockers.append("deterministic validation did not pass")
    if evidence.validation.blocker_annotations != unresolved_pilot_blockers(evidence.annotations):
        blockers.append("validation annotation evidence does not match retained annotations")
    if unresolved_pilot_blockers(evidence.annotations):
        blockers.append("unresolved high-severity reviewer annotations remain")
    audit = evidence.audit
    expected_hashes = {
        "input": (audit.input_sha256, _sha256(evidence.household)),
        "output": (audit.output_sha256, _sha256(evidence.brief)),
        "validation": (audit.validation_sha256, _sha256(evidence.validation)),
        "annotations": (audit.annotations_sha256, _sha256(evidence.annotations)),
        "privacy review": (audit.privacy_review_sha256, _sha256(evidence.privacy_review)),
        "review events": (audit.review_events_sha256, _sha256(evidence.review_events)),
        "coverage": (audit.coverage_sha256, _sha256(evidence.coverage)),
        "policy": (audit.policy_sha256, _sha256(evidence.policy)),
    }
    if audit.case_id != evidence.household.case_id:
        blockers.append("audit record belongs to a different case")
    if (audit.policy_id, audit.policy_version) != (evidence.policy.policy_id, evidence.policy.version):
        blockers.append("audit record belongs to a different policy")
    if audit.jurisdiction != evidence.coverage.jurisdiction:
        blockers.append("audit record belongs to different jurisdiction coverage")
    if audit.review_state != review_state:
        blockers.append("audit review state does not match review events")
    for label, (actual, expected) in expected_hashes.items():
        if actual != expected:
            blockers.append(f"audit {label} fingerprint does not match retained evidence")
    return PilotGateResult(ready=not blockers, blockers=tuple(blockers))


def create_governed_decision_brief(
    household: HouseholdCase,
    policy: GovernedPolicy,
    coverage: JurisdictionCoverage,
    *,
    annotations: Iterable[ReviewerAnnotation],
    privacy_review: PrivacySecurityReview,
    review_events: Iterable[ReviewEvent],
    workflow_id: str,
    audit_id: str,
    created_at: str | None = None,
) -> GovernedDecisionBrief:
    """Run calculation through one case-bound governance and gate workflow."""
    if not workflow_id.strip():
        raise ValueError("workflow_id is required")
    retained_annotations = tuple(annotations)
    retained_events = tuple(review_events)
    brief = build_decision_brief(household, policy.engine_policy())
    validation = validate_decision_brief(
        household,
        brief,
        retained_annotations,
        policy.engine_policy(),
        evidence_id=f"{workflow_id}:validation",
    )
    final_review_state, _ = _review_state(retained_events)
    audit = create_audit_record(
        household,
        brief,
        policy,
        coverage,
        audit_id=audit_id,
        created_at=created_at,
        review_state=final_review_state,
        validation=validation,
        annotations=retained_annotations,
        privacy_review=privacy_review,
        review_events=retained_events,
    )
    evidence = GovernedWorkflowEvidence(
        workflow_id=workflow_id,
        household=household,
        policy=policy,
        coverage=coverage,
        brief=brief,
        validation=validation,
        annotations=retained_annotations,
        privacy_review=privacy_review,
        review_events=retained_events,
        audit=audit,
    )
    return GovernedDecisionBrief(evidence=evidence, pilot_gate=evaluate_pilot_gate(evidence))
