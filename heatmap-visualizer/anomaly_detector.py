"""Summarise unusually concentrated source activity for visual investigation.

This module is an investigative aid, not a second detection engine. The
canonical SSH detection rule lives in defensive-detection/log_parser.py.
"""

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
            if event.get("src"):
                events.append(event)
    return events


def summarise_source_activity(events, threshold=5):
    """Return source counts meeting a visual-analysis threshold.

    The result describes concentration only. It does not classify the source
    as malicious and should not be treated as a security alert.
    """
    counts = Counter(event["src"] for event in events)
    return {ip: count for ip, count in counts.items() if count >= threshold}


def main():
    parser = argparse.ArgumentParser(description="Summarise concentrated source activity.")
    parser.add_argument("--log", default="../offensive-simulation/brute_force.log")
    parser.add_argument("--threshold", type=int, default=5)
    args = parser.parse_args()

    activity = summarise_source_activity(load_events(args.log), args.threshold)
    print("Sources with concentrated activity (investigative aid):")
    if not activity:
        print("None detected.")
        return
    for ip, count in sorted(activity.items(), key=lambda item: item[1], reverse=True):
        print(f"  {ip}: {count} events")


if __name__ == "__main__":
    main()
