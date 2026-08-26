"""Extract investigation indicators from ThreatTrace security telemetry."""

from collections import Counter
from pathlib import Path
from datetime import datetime


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


def extract_iocs(file_path):
    """Extract and return useful investigation indicators from telemetry."""
    events = []
    with Path(file_path).open("r", encoding="utf-8") as log:
        for line in log:
            event = parse_event(line)
            if event:
                events.append(event)

    source_ips = Counter(event["src"] for event in events)
    destination_ips = Counter(event["dst"] for event in events)
    usernames = Counter(event["user"] for event in events)
    event_types = Counter(event["event_type"] for event in events)
    protocols = Counter(event["protocol"] for event in events)
    ports = Counter(event["dst_port"] for event in events)

    iocs = {
        "source_ips": source_ips,
        "destination_ips": destination_ips,
        "usernames": usernames,
        "event_types": event_types,
        "protocols": protocols,
        "destination_ports": ports,
        "first_seen": min((event["timestamp"] for event in events), default=None),
        "last_seen": max((event["timestamp"] for event in events), default=None),
    }

    print("Extracted Investigation Indicators")
    print("=" * 42)
    print("Source IPs:")
    for value, count in source_ips.items():
        print(f"- {value} ({count} events)")

    print("\nDestination IPs:")
    for value, count in destination_ips.items():
        print(f"- {value} ({count} events)")

    print("\nTargeted Accounts:")
    for value, count in usernames.items():
        print(f"- {value} ({count} events)")

    print("\nProtocols / Ports:")
    for protocol, count in protocols.items():
        print(f"- {protocol}: {count} events")
    for port, count in ports.items():
        print(f"- Destination port {port}: {count} events")

    print("\nEvent Types:")
    for event_type, count in event_types.items():
        print(f"- {event_type}: {count}")

    print("\nObserved Window:")
    print(f"- First seen: {iocs['first_seen']}")
    print(f"- Last seen:  {iocs['last_seen']}")

    return iocs


if __name__ == "__main__":
    log_file = Path(__file__).parent.parent / "offensive-simulation" / "brute_force.log"
    extract_iocs(log_file)
