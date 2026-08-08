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

    def test_ac_cib_017_pilot_gate_requires_all_governance_evidence(self) -> None:
        ready = evaluate_pilot_gate(
            coverage=self.coverage, privacy_review=self.privacy,
            review_state=ReviewState.APPROVED, validation_passed=True,
            unresolved_annotation_count=0,
        )
        self.assertTrue(ready.ready)
        blocked = evaluate_pilot_gate(
            coverage=replace(self.coverage, status="prototype"),
            privacy_review=replace(self.privacy, open_findings=("retention review",)),
            review_state=ReviewState.SUBMITTED, validation_passed=False,
            unresolved_annotation_count=1,
        )
        self.assertFalse(blocked.ready)
        self.assertEqual(len(blocked.blockers), 5)


if __name__ == "__main__":
    unittest.main()
