"""Generate safe, synthetic SSH authentication telemetry for ThreatTrace Lab.

This simulator does not perform real authentication attempts. It only writes
synthetic security events to a local log file for defensive analysis.
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import random

LOG_FILE = Path(__file__).with_name("brute_force.log")

SOURCE_IP = "10.10.10.50"
DESTINATION_IP = "10.10.10.10"
DESTINATION_PORT = 22
USERNAMES = ["admin", "root", "user", "test"]


def generate_event(timestamp, event_type, username, source_ip=SOURCE_IP):
    """Return one structured synthetic SSH security event."""
    return (
        f"{timestamp.isoformat().replace('+00:00', 'Z')} | "
        f"{event_type} | protocol=SSH | src={source_ip} | "
        f"dst={DESTINATION_IP} | dst_port={DESTINATION_PORT} | "
        f"user={username}\n"
    )


def simulate_brute_force(output_file=LOG_FILE):
    """Generate failed SSH attempts followed by a successful login.

    The resulting telemetry is intentionally deterministic enough to support
    repeatable detection and investigation exercises while retaining small
    variations in timing and targeted usernames.
    """
    output_file = Path(output_file)
    start = datetime.now(timezone.utc).replace(microsecond=0)
    events = []

    # Generate 12 failed attempts from one source within a short window.
    current = start
    for _ in range(12):
        username = random.choice(USERNAMES)
        events.append(generate_event(current, "SSH_AUTH_FAILURE", username))
        current += timedelta(seconds=random.randint(2, 8))

    # Simulate the important investigation pivot: a successful login follows
    # repeated failures from the same source.
    events.append(generate_event(current + timedelta(seconds=5), "SSH_AUTH_SUCCESS", "admin"))

    output_file.write_text("".join(events), encoding="utf-8")

    print(f"Generated {len(events)} synthetic SSH events.")
    print(f"Telemetry written to: {output_file}")


if __name__ == "__main__":
    simulate_brute_force()
