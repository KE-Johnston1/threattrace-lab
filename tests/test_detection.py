import unittest
from datetime import datetime, timezone, timedelta

from defensive_detection.log_parser import detect_ssh_brute_force, parse_event


def event(minutes=0, seconds=0, event_type="SSH_AUTH_FAILURE", user="admin", source="10.10.10.50"):
    timestamp = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc) + timedelta(
        minutes=minutes, seconds=seconds
    )
    return {
        "timestamp": timestamp,
        "event_type": event_type,
        "protocol": "SSH",
        "src": source,
        "dst": "10.10.10.10",
        "dst_port": "22",
        "user": user,
    }


class ParseEventTests(unittest.TestCase):
    def test_parse_valid_event(self):
        line = (
            "2026-01-01T12:00:00Z | SSH_AUTH_FAILURE | protocol=SSH | "
            "src=10.10.10.50 | dst=10.10.10.10 | dst_port=22 | user=admin"
        )
        parsed = parse_event(line)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["src"], "10.10.10.50")
        self.assertEqual(parsed["user"], "admin")

    def test_malformed_event_is_ignored(self):
        self.assertIsNone(parse_event("not valid telemetry"))


class DetectionTests(unittest.TestCase):
    def test_four_failures_do_not_alert(self):
        events = [event(seconds=i * 30) for i in range(4)]
        self.assertEqual(detect_ssh_brute_force(events), [])

    def test_five_failures_within_window_alert(self):
        events = [event(seconds=i * 30) for i in range(5)]
        alerts = detect_ssh_brute_force(events)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "MEDIUM")
        self.assertFalse(alerts[0]["successful_login"])
        self.assertEqual(alerts[0]["failed_attempts"], 5)

    def test_failures_outside_window_do_not_alert(self):
        events = [event(minutes=i * 2) for i in range(5)]
        self.assertEqual(detect_ssh_brute_force(events), [])

    def test_success_after_threshold_escalates_to_high(self):
        events = [event(seconds=i * 30) for i in range(5)]
        events.append(event(minutes=3, event_type="SSH_AUTH_SUCCESS"))
        alerts = detect_ssh_brute_force(events)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "HIGH")
        self.assertTrue(alerts[0]["successful_login"])
        self.assertEqual(alerts[0]["account"], "admin")

    def test_different_source_does_not_combine_failures(self):
        events = [event(seconds=i * 30, source="10.10.10.50") for i in range(3)]
        events += [event(seconds=i * 30, source="10.10.10.60") for i in range(3)]
        self.assertEqual(detect_ssh_brute_force(events), [])

    def test_non_ssh_events_are_ignored(self):
        events = [event(seconds=i * 30) for i in range(5)]
        for item in events:
            item["protocol"] = "HTTP"
        self.assertEqual(detect_ssh_brute_force(events), [])


if __name__ == "__main__":
    unittest.main()
