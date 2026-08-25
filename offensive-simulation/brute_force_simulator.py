"""Generate safe, synthetic SSH authentication telemetry for ThreatTrace Lab.

This simulator does not perform real authentication attempts. It only writes
synthetic security events to a local log file for defensive analysis.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import random

LOG_FILE = Path(__file__).with_name("brute_force.log")

SOURCE_IP = "10.10.10.50"
DESTINATION_IP = "10.10.10.10"
DESTINATION_PORT = 22

TARGET_USERNAME = "admin"
OTHER_USERNAMES = ["root", "user", "test"]

FAILURE_COUNT = 12
DEFAULT_SEED = 42


def generate_event(timestamp, event_type, username, source_ip=SOURCE_IP):
    """Return one structured synthetic SSH security event."""
    return (
        f"{timestamp.isoformat().replace('+00:00', 'Z')} | "
        f"{event_type} | protocol=SSH | src={source_ip} | "
        f"dst={DESTINATION_IP} | dst_port={DESTINATION_PORT} | "
        f"user={username}\n"
    )


def simulate_brute_force(output_file=LOG_FILE, seed=DEFAULT_SEED):
    """Generate a repeatable SSH brute-force scenario for SOC analysis.

    The scenario contains repeated authentication failures, including repeated
    targeting of the admin account, followed by a successful admin login from
    the same source IP. No real network connection or authentication occurs.

    Args:
        output_file: Destination path for the synthetic telemetry.
        seed: Seed used to make the generated scenario reproducible.
    """
    output_file = Path(output_file)
    rng = random.Random(seed)

    start = datetime.now(timezone.utc).replace(microsecond=0)
    events = []
    current = start

    # Ensure the scenario contains repeated targeting of the account that is
    # eventually authenticated successfully.
    usernames = [
        TARGET_USERNAME,
        TARGET_USERNAME,
        TARGET_USERNAME,
        TARGET_USERNAME,
        TARGET_USERNAME,
    ] + OTHER_USERNAMES

    for attempt in range(FAILURE_COUNT):
        username = TARGET_USERNAME if attempt < 8 else rng.choice(usernames)
        events.append(generate_event(current, "SSH_AUTH_FAILURE", username))
        current += timedelta(seconds=rng.randint(2, 8))

    # Investigation pivot: repeated failures are followed by a successful
    # authentication to the same account from the same source.
    current += timedelta(seconds=5)
    events.append(generate_event(current, "SSH_AUTH_SUCCESS", TARGET_USERNAME))

    output_file.write_text("".join(events), encoding="utf-8")

    print(f"Generated {len(events)} synthetic SSH events.")
    print(f"Scenario seed: {seed}")
    print(f"Telemetry written to: {output_file}")


if __name__ == "__main__":
    simulate_brute_force()
