"""Detect suspicious SSH authentication activity in ThreatTrace telemetry."""

from collections import defaultdict
from datetime import datetime, timedelta, timezone
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
        timestamp = datetime.fromisoformat(fields[0].replace("Z", "+00:00"))
    except ValueError:
        return None

    event = {
        "timestamp": timestamp,
        "event_type": fields[1],
    }

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

    Detection rule SSH-BRUTE-001 fires when a source produces at least five
    failed SSH authentications within five minutes. A successful login from
    the same source during the detection window raises the alert severity to
    HIGH because it represents a potential account compromise.
    """
    failures_by_source = defaultdict(list)
    alerts = []

    for event in events:
        if event.get("protocol") != "SSH":
            continue

        source = event["src"]

        if event["event_type"] == "SSH_AUTH_FAILURE":
            failures_by_source[source].append(event)
            cutoff = event["timestamp"] - timedelta(minutes=WINDOW_MINUTES)
            failures_by_source[source] = [
                failure
                for failure in failures_by_source[source]
                if failure["timestamp"] >= cutoff
            ]

            if len(failures_by_source[source]) >= FAILURE_THRESHOLD:
                failures = failures_by_source[source]
                success = next(
                    (
                        candidate
                        for candidate in events
                        if candidate["event_type"] == "SSH_AUTH_SUCCESS"
                        and candidate["src"] == source
                        and event["timestamp"] <= candidate["timestamp"]
                        <= event["timestamp"] + timedelta(minutes=WINDOW_MINUTES)
                    ),
                    None,
                )

                alerts.append(
                    {
                        "alert_id": ALERT_ID,
                        "rule_id": RULE_ID,
                        "severity": "HIGH" if success else "MEDIUM",
                        "source_ip": source,
                        "destination_ip": event["dst"],
                        "account": success["user"] if success else failures[-1]["user"],
                        "failed_attempts": len(failures),
                        "successful_login": success is not None,
                        "first_seen": failures[0]["timestamp"],
                        "last_seen": success["timestamp"] if success else failures[-1]["timestamp"],
                    }
                )

                # Avoid emitting the same alert repeatedly for every failure
                # after the threshold has already been reached.
                failures_by_source[source] = []

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
