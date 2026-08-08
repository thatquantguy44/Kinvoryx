"""Slice D governed pilot-readiness tests for Spec 011."""

from dataclasses import replace
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from kinvoryx.cash_inflow import build_decision_brief
from kinvoryx.cash_inflow_governance import (
    REQUIRED_PRIVACY_CONTROLS,
    GovernedPolicy,
    JurisdictionCoverage,
    PrivacySecurityReview,
    ReviewState,
    create_governed_decision_brief,
    create_audit_record,
    evaluate_pilot_gate,
    transition_review,
)
from kinvoryx.cash_inflow_validation import golden_case_fixtures


class CashInflowGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.household = golden_case_fixtures()[0].household
        self.policy = GovernedPolicy(
            policy_id="cib-defaults",
            version="1.0.0",
            effective_from="2026-08-08T00:00:00Z",
            approved_by_role="risk-owner",
        )
        self.coverage = JurisdictionCoverage(
            jurisdiction="US-FEDERAL-PROTOTYPE",
            decision_type="post-tax-cash-inflow-comparison",
            status="reviewed",
            effective_as_of="2026-08-08",
            supported_claims=("deterministic allocation comparison",),
            unsupported_claims=("tax eligibility", "state-specific rules"),
            source_refs=("docs/specs/011-cash-inflow-allocation-decision-brief.md",),
            reviewed_by_role="domain-reviewer",
        )
        self.privacy = PrivacySecurityReview(
            review_id="psr-001",
            reviewer_role="security-reviewer",
            reviewed_at="2026-08-08T00:00:00Z",
            approved_controls=REQUIRED_PRIVACY_CONTROLS,
        )

    def test_ac_cib_014_governed_policy_drives_engine_and_rejects_invalid_values(self) -> None:
        brief = build_decision_brief(self.household, self.policy.engine_policy())
        self.assertIn("7%", brief.assumptions[3])
        with self.assertRaisesRegex(ValueError, "resilience"):
            replace(self.policy, resilience_reserve_months=Decimal("2"))

    def test_ac_cib_015_audit_hashes_are_reproducible_and_case_bound(self) -> None:
        brief = build_decision_brief(self.household, self.policy.engine_policy())
        first = create_audit_record(
            self.household, brief, self.policy, self.coverage,
            audit_id="audit-001", created_at="2026-08-08T01:00:00Z",
        )
        second = create_audit_record(
            self.household, brief, self.policy, self.coverage,
            audit_id="audit-002", created_at="2026-08-08T02:00:00Z",
        )
        self.assertEqual(first.input_sha256, second.input_sha256)
        self.assertEqual(first.output_sha256, second.output_sha256)
        self.assertEqual(len(first.input_sha256), 64)

    def test_ac_cib_016_human_review_state_machine_fails_closed(self) -> None:
        event = transition_review(
            ReviewState.DRAFT, ReviewState.SUBMITTED,
            event_id="review-001", actor_role="analyst", reason="ready for review",
            occurred_at="2026-08-08T01:00:00Z",
        )
        self.assertEqual(event.to_state, ReviewState.SUBMITTED)
        with self.assertRaisesRegex(ValueError, "invalid review transition"):
            transition_review(
                ReviewState.DRAFT, ReviewState.APPROVED,
                event_id="review-002", actor_role="analyst", reason="skip",
                occurred_at="2026-08-08T01:00:00Z",
            )

    def _approved_review_events(self):
        submitted = transition_review(
            ReviewState.DRAFT, ReviewState.SUBMITTED,
            event_id="review-submit", actor_role="analyst", reason="ready for review",
            occurred_at="2026-08-08T01:00:00Z",
        )
        approved = transition_review(
            ReviewState.SUBMITTED, ReviewState.APPROVED,
            event_id="review-approve", actor_role="risk-reviewer", reason="evidence accepted",
            occurred_at="2026-08-08T02:00:00Z",
        )
        return submitted, approved

    def test_ac_gdb_001_pilot_gate_is_derived_from_case_bound_evidence(self) -> None:
        result = create_governed_decision_brief(
            self.household, self.policy, self.coverage,
            annotations=(), privacy_review=self.privacy,
            review_events=self._approved_review_events(),
            workflow_id="workflow-001", audit_id="audit-001",
            created_at="2026-08-08T03:00:00Z",
        )
        self.assertTrue(result.pilot_gate.ready)
        self.assertEqual(result.evidence.household.case_id, result.evidence.validation.case_id)
        self.assertEqual(result.evidence.brief, result.evidence.validation.brief)
        self.assertEqual(result.evidence.audit.review_state, ReviewState.APPROVED)

    def test_ac_gdb_002_gate_rejects_tampered_or_cross_workflow_evidence(self) -> None:
        result = create_governed_decision_brief(
            self.household, self.policy, self.coverage,
            annotations=(), privacy_review=self.privacy,
            review_events=self._approved_review_events(),
            workflow_id="workflow-002", audit_id="audit-002",
            created_at="2026-08-08T03:00:00Z",
        )
        tampered = replace(
            result.evidence,
            coverage=replace(self.coverage, jurisdiction="US-OTHER"),
        )
        gate = evaluate_pilot_gate(tampered)
        self.assertFalse(gate.ready)
        self.assertIn("audit record belongs to different jurisdiction coverage", gate.blockers)
        self.assertIn("audit coverage fingerprint does not match retained evidence", gate.blockers)


if __name__ == "__main__":
    unittest.main()
