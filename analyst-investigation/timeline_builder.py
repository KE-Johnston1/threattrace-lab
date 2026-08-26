"""Build an analyst-friendly incident timeline from ThreatTrace telemetry."""

from datetime import datetime
from pathlib import Path


def parse_event(line):
    """Parse a structured ThreatTrace event."""
    fields = [field.strip() for field in line.strip().split("|")]
    if len(fields) < 7:
        return None

    try:
        timestamp = datetime.fromisoformat(fields[0].replace("Z", "+00:00"))
    except ValueError:
        return None

    event = {"timestamp": timestamp, "event_type": fields[1]}
    for field in fields[2:]:
        if "=" in field:
            key, value = field.split("=", 1)
            event[key.strip()] = value.strip()

    required = {"protocol", "src", "dst", "dst_port", "user"}
    return event if required.issubset(event) else None


def describe_event(event):
    """Return a concise analyst description for an event."""
    if event["event_type"] == "SSH_AUTH_FAILURE":
        return f"Failed SSH authentication for account '{event['user']}'"
    if event["event_type"] == "SSH_AUTH_SUCCESS":
        return f"Successful SSH authentication for account '{event['user']}'"
    return f"{event['event_type']} for account '{event['user']}'"


def build_timeline(file_path):
    """Build, print, and return the chronological incident timeline."""
    timeline = []

    with Path(file_path).open("r", encoding="utf-8") as log:
        for line in log:
            event = parse_event(line)
            if event:
                timeline.append(event)

    timeline.sort(key=lambda event: event["timestamp"])

    print("Incident Timeline")
    print("=" * 72)
    for event in timeline:
        print(
            f"{event['timestamp'].isoformat()} | "
            f"{event['src']} -> {event['dst']}:{event['dst_port']} | "
            f"{describe_event(event)}"
        )

    return timeline


if __name__ == "__main__":
    log_file = Path(__file__).parent.parent / "offensive-simulation" / "brute_force.log"
    build_timeline(log_file)
