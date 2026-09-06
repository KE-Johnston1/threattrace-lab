import unittest

from soc_triage.post_investigation import (
    ImprovementAction,
    LessonsLearned,
    improvement_summary,
    validate_lessons,
)


class LessonsLearnedTests(unittest.TestCase):
    def lesson(self, **overrides):
        values = {
            "case_id": "TT-SSH-001",
            "outcome": "Investigation closed after required verification",
            "what_happened": "Repeated SSH failures were followed by successful admin authentication.",
            "what_went_well": ("Authentication events were correlated",),
            "what_did_not_go_well": ("Endpoint telemetry was initially unavailable",),
            "detection_improvements": ("Detect failure-to-success authentication sequences",),
            "investigation_improvements": ("Verify asset ownership earlier",),
            "playbook_improvements": ("Add explicit post-authentication review",),
            "telemetry_improvements": ("Improve endpoint/network coverage",),
            "training_lessons": ("Suspicious authentication is not proof of compromise",),
            "follow_up_actions": (
                ImprovementAction(
                    "Add ownership check to triage",
                    "Investigation",
                    "SOC",
                    "Medium",
                ),
                ImprovementAction(
                    "Add post-auth telemetry requirement",
                    "Telemetry",
                    "Security Engineering",
                    "High",
                    status="In Progress",
                ),
            ),
        }
        values.update(overrides)
        return LessonsLearned(**values)

    def test_valid_lessons_have_summary(self):
        summary = improvement_summary(self.lesson())
        self.assertEqual(summary["total_actions"], 2)
        self.assertEqual(summary["open_actions"], 1)
        self.assertEqual(summary["high_or_critical"], 1)

    def test_missing_case_id_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_lessons(self.lesson(case_id=""))

    def test_invalid_action_priority_is_rejected(self):
        action = ImprovementAction("Improve detection", "Detection", "SOC", "Extreme")
        with self.assertRaises(ValueError):
            validate_lessons(self.lesson(follow_up_actions=(action,)))

    def test_invalid_action_status_is_rejected(self):
        action = ImprovementAction("Improve detection", "Detection", "SOC", "Low", status="Unknown")
        with self.assertRaises(ValueError):
            validate_lessons(self.lesson(follow_up_actions=(action,)))


if __name__ == "__main__":
    unittest.main()
