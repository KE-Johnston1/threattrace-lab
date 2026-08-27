"""Identify unusually active source IPs in ThreatTrace telemetry."""

import argparse
from collections import Counter
from pathlib import Path


def load_events(log_file):
    """Return parsed event dictionaries from structured ThreatTrace telemetry."""
    events = []
    with Path(log_file).open("r", encoding="utf-8") as file:
        for line in file:
            fields = [field.strip() for field in line.strip().split("|")]
            if len(fields) < 2:
                continue
            event = {"event_type": fields[1]}
            for field in fields[2:]:
                if "=" in field:
                    key, value = field.split("=", 1)
                    event[key.strip()] = value.strip()
            if "src" in event:
                events.append(event)
    return events


def detect_anomalies(events, threshold=5):
    """Return source IPs with at least ``threshold`` observed events."""
    counts = Counter(event["src"] for event in events)
    return {ip: count for ip, count in counts.items() if count >= threshold}


def main():
    parser = argparse.ArgumentParser(description="Detect unusually active source IPs.")
    parser.add_argument(
        "--log",
        default="../offensive-simulation/brute_force.log",
        help="Path to structured ThreatTrace telemetry.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Minimum event count required to flag a source IP.",
    )
    args = parser.parse_args()

    anomalies = detect_anomalies(load_events(args.log), args.threshold)

    print("Anomalous source IPs:")
    if not anomalies:
        print("None detected.")
        return

    for ip, count in sorted(anomalies.items(), key=lambda item: item[1], reverse=True):
        print(f"  {ip}: {count} events")


if __name__ == "__main__":
    main()
