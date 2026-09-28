import unittest
from unittest.mock import patch

from kinvoryx.housing_sources import (
    SourceCheckResult,
    configured_secret,
    run_source_checks,
    source_policies,
)


class HousingSourceTests(unittest.TestCase):
    def test_source_policies_do_not_allow_raw_payload_retention_by_default(self):
        policies = source_policies()

        self.assertIn("trellistate_public_listings", policies)
        self.assertIn("fema_nfhl_metadata", policies)
        self.assertTrue(all(not policy.raw_payload_retention_allowed for policy in policies.values()))

    def test_configured_secret_ignores_placeholders(self):
        config = {
            "airnow": {"api_key": "replace_with_airnow_key"},
            "wmata": {"api_key": "realistic-token"},
        }

        self.assertIsNone(configured_secret(config, "airnow.api_key"))
        self.assertEqual(configured_secret(config, "wmata.api_key"), "realistic-token")

    def test_run_source_checks_returns_metadata_report_without_raw_payloads(self):
        def fake_metadata_get(*, source_id, endpoint_family, url, headers=None, method="GET", body=None):
            return SourceCheckResult(
                source_id=source_id,
                status="ok",
                checked_at_utc="2026-09-27T00:00:00+00:00",
                endpoint_family=endpoint_family,
                http_status=200,
                response_shape="object",
                top_level_keys=["example"],
                result_count_hint=1,
                raw_payload_retained=False,
                message="test",
            )

        config = {
            "wmata": {"api_key": "wmata-token"},
            "usajobs": {"authorization_key": "usajobs-token", "user_agent": "test@example.com"},
            "airnow": {"api_key": "airnow-token"},
            "noaa_cdo": {"token": "noaa-token"},
            "nws": {"contact_user_agent": "KinvoryxHomeSweetHome/0.1 (test@example.com)"},
        }

        with patch("kinvoryx.housing_sources.metadata_get", side_effect=fake_metadata_get):
            report = run_source_checks(config)

        self.assertEqual(report["schema_version"], 1)
        self.assertFalse(report["raw_payloads_retained"])
        self.assertGreaterEqual(len(report["policies"]), 10)
        self.assertGreaterEqual(len(report["results"]), 10)
        self.assertTrue(all(not result["raw_payload_retained"] for result in report["results"]))


if __name__ == "__main__":
    unittest.main()
