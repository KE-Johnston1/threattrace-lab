"""Detect suspicious SSH authentication activity in ThreatTrace telemetry."""

from collections import defaultdict
from datetime import timedelta
from pathlib import Path

FAILURE_THRESHOLD = 5
WINDOW_MINUTES = 5
RULE_ID = "SSH-BRUTE-001"
ALERT_ID = "TT-SSH-001"


def parse_event(line):
    """Parse one structured ThreatTrace event into a dictionary."""
    fields = [field.strip() for field in line.strip().split("|")]
    if len(fields) < 7:
        return None

    try:
        timestamp = __import__("datetime").datetime.fromisoformat(
            fields[0].replace("Z", "+00:00")
        )
    except ValueError:
        return None

    event = {"timestamp": timestamp, "event_type": fields[1]}

    for field in fields[2:]:
        if "=" not in field:
            continue
        key, value = field.split("=", 1)
        event[key.strip()] = value.strip()

    required = {"protocol", "src", "dst", "dst_port", "user"}
    if not required.issubset(event):
        return None

    return event


def load_events(file_path):
    """Load valid structured events from a telemetry file."""
    events = []
    with Path(file_path).open("r", encoding="utf-8") as log:
        for line in log:
            event = parse_event(line)
            if event is not None:
                events.append(event)
    return sorted(events, key=lambda event: event["timestamp"])


def detect_ssh_brute_force(events):
    """Detect repeated SSH failures followed by successful authentication.

    SSH-BRUTE-001 fires once per source when at least five failed SSH
    authentications occur within five minutes. If a successful login from the
    same source follows the threshold event within five minutes, severity is
    raised to HIGH because the activity may represent account compromise.
    """
    ssh_events_by_source = defaultdict(list)

    for event in events:
        if event.get("protocol") == "SSH":
            ssh_events_by_source[event["src"]].append(event)

    alerts = []
    window = timedelta(minutes=WINDOW_MINUTES)

    for source, source_events in ssh_events_by_source.items():
        source_events.sort(key=lambda event: event["timestamp"])
        failures = [
            event
            for event in source_events
            if event["event_type"] == "SSH_AUTH_FAILURE"
        ]
        successes = [
            event
            for event in source_events
            if event["event_type"] == "SSH_AUTH_SUCCESS"
        ]

        if len(failures) < FAILURE_THRESHOLD:
            continue

        detection_window = None
        for index in range(len(failures) - FAILURE_THRESHOLD + 1):
            window_failures = failures[index : index + FAILURE_THRESHOLD]
            if (
                window_failures[-1]["timestamp"] - window_failures[0]["timestamp"]
                <= window
            ):
                detection_window = window_failures
                break

        if detection_window is None:
            continue

        threshold_event = detection_window[-1]
        successful_login = next(
            (
                success
                for success in successes
                if threshold_event["timestamp"]
                <= success["timestamp"]
                <= threshold_event["timestamp"] + window
            ),
            None,
        )

        destination_ip = threshold_event["dst"]
        account = (
            successful_login["user"]
            if successful_login
            else detection_window[-1]["user"]
        )

        # Include all failures that belong to the five-minute detection window
        # rather than only the minimum threshold of five.
        all_window_failures = [
            failure
            for failure in failures
            if detection_window[0]["timestamp"]
            <= failure["timestamp"]
            <= threshold_event["timestamp"]
        ]

        alerts.append(
            {
                "alert_id": ALERT_ID,
                "rule_id": RULE_ID,
                "severity": "HIGH" if successful_login else "MEDIUM",
                "source_ip": source,
                "destination_ip": destination_ip,
                "account": account,
                "failed_attempts": len(all_window_failures),
                "successful_login": successful_login is not None,
                "first_seen": all_window_failures[0]["timestamp"],
                "last_seen": (
                    successful_login["timestamp"]
                    if successful_login
                    else all_window_failures[-1]["timestamp"]
                ),
            }
        )

    return alerts


def print_alert(alert):
    """Display a SOC-style alert for an analyst."""
    print("=" * 58)
    print(" SECURITY ALERT")
    print("=" * 58)
    print(f"Alert ID:           {alert['alert_id']}")
    print(f"Detection Rule:     {alert['rule_id']}")
    print(f"Severity:           {alert['severity']}")
    print(f"Source IP:          {alert['source_ip']}")
    print(f"Destination IP:     {alert['destination_ip']}")
    print(f"Target Account:     {alert['account']}")
    print(f"Failed Attempts:    {alert['failed_attempts']}")
    print(f"Successful Login:   {'YES' if alert['successful_login'] else 'NO'}")
    print(f"First Seen:         {alert['first_seen'].isoformat()}")
    print(f"Last Seen:          {alert['last_seen'].isoformat()}")
    print()
    print("Detection Rationale:")
    print("Multiple SSH authentication failures from the same source")
    print("were observed within a five-minute window.")
    if alert["successful_login"]:
        print("A successful authentication followed the failed attempts.")
    print()
    print("Recommended Action:")
    print("Investigate the source host and successful authentication session.")
    print("Validate whether the target account was legitimately used.")
    print("=" * 58)


def run_detection(file_path):
    """Run the SSH brute-force detector against a telemetry file."""
    events = load_events(file_path)
    alerts = detect_ssh_brute_force(events)

    print(f"Loaded {len(events)} security events.")
    print(f"Generated {len(alerts)} detection alert(s).")

    for alert in alerts:
        print_alert(alert)

    return alerts


if __name__ == "__main__":
    log_file = Path(__file__).parent.parent / "offensive-simulation" / "brute_force.log"
    run_detection(log_file)
