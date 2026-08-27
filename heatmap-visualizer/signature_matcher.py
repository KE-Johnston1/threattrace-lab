"""Match defensive activity patterns in ThreatTrace SSH telemetry."""

import argparse
from pathlib import Path


def load_events(log_file):
    """Parse structured ThreatTrace telemetry into event dictionaries."""
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
            if event.get("protocol") == "SSH":
                events.append(event)
    return events


def match_signatures(events):
    """Return defensive signatures supported by the observed telemetry."""
    failures = [event for event in events if event["event_type"] == "SSH_AUTH_FAILURE"]
    successes = [event for event in events if event["event_type"] == "SSH_AUTH_SUCCESS"]

    signatures = []
    if failures:
        signatures.append(
            {
                "name": "SSH Authentication Failure Activity",
                "rule": "SSH-AUTH-FAILURE",
                "matches": len(failures),
            }
        )

    if len(failures) >= 5:
        signatures.append(
            {
                "name": "SSH Brute Force Pattern",
                "rule": "SSH-BRUTE-001",
                "matches": len(failures),
            }
        )

    if successes and failures:
        signatures.append(
            {
                "name": "Failed Authentication Followed by Success",
                "rule": "SSH-COMPROMISE-PIVOT",
                "matches": len(successes),
            }
        )

    return signatures


def main():
    parser = argparse.ArgumentParser(description="Match SSH activity signatures.")
    parser.add_argument(
        "--log",
        default="../offensive-simulation/brute_force.log",
        help="Path to structured ThreatTrace telemetry.",
    )
    args = parser.parse_args()

    signatures = match_signatures(load_events(args.log))

    print("Matched defensive signatures:")
    if not signatures:
        print("None detected.")
        return

    for signature in signatures:
        print(
            f"  {signature['rule']}: {signature['name']} "
            f"({signature['matches']} event(s))"
        )


if __name__ == "__main__":
    main()
