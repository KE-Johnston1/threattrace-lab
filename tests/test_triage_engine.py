import unittest

from soc_triage.triage_engine import TriageInput, triage_alert


class TriageEngineTests(unittest.TestCase):
    def base_case(self, **overrides):
        values = {
            "alert_id": "TT-SSH-001",
            "source_ip": "10.10.10.50",
            "destination_ip": "10.10.10.10",
            "account": "admin",
            "successful_login": True,
            "owner_verified": True,
            "authorization_verified": True,
            "timing_verified": True,
            "post_auth_reviewed": True,
            "network_reviewed": True,
            "change_or_testing_checked": True,
        }
        values.update(overrides)
        return TriageInput(**values)

    def test_missing_authorization_is_insufficient(self):
        result = triage_alert(self.base_case(authorization_verified=False))
        self.assertEqual(result.assessment, "Insufficient Evidence")
        self.assertIn("authorization", " ".join(result.evidence_gaps))

    def test_successful_login_without_post_auth_review_requires_investigation(self):
        result = triage_alert(self.base_case(post_auth_reviewed=False))
        self.assertEqual(result.assessment, "Requires Investigation")
        self.assertIn("successful session", " ".join(result.evidence_gaps))

    def test_complete_expected_context_can_close(self):
        result = triage_alert(self.base_case())
        self.assertEqual(result.assessment, "Expected")
        self.assertEqual(result.confidence, "High")
        self.assertEqual(result.evidence_gaps, ())

    def test_missing_network_context_prevents_expected_closure(self):
        result = triage_alert(self.base_case(network_reviewed=False))
        self.assertEqual(result.assessment, "Requires Investigation")


if __name__ == "__main__":
    unittest.main()
