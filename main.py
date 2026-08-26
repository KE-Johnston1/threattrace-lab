"""ThreatTrace Lab - end-to-end SOC investigation launcher.

Run this file from the repository root to execute the complete synthetic SSH
brute-force investigation workflow:

1. Generate synthetic security telemetry
2. Run the SSH brute-force detection rule
3. Extract investigation indicators
4. Build the incident timeline
5. Display the investigation report location

All activity is local and synthetic. No network connections are performed.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "offensive-simulation" / "brute_force.log"


def load_module(name, path):
    """Load a Python module from a repository path."""
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module: {path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("=" * 72)
    print("THREATTRACE LAB - SOC INVESTIGATION")
    print("=" * 72)
    print("Scenario: SSH brute-force followed by successful authentication")
    print("Environment: Synthetic / controlled lab")
    print()

    simulator = load_module(
        "threattrace_simulator",
        ROOT / "offensive-simulation" / "brute_force_simulator.py",
    )
    detector = load_module(
        "threattrace_detector",
        ROOT / "defensive-detection" / "log_parser.py",
    )
    ioc_extractor = load_module(
        "threattrace_iocs",
        ROOT / "analyst-investigation" / "ioc_extractor.py",
    )
    timeline_builder = load_module(
        "threattrace_timeline",
        ROOT / "analyst-investigation" / "timeline_builder.py",
    )

    print("[1/4] Generating synthetic telemetry...")
    simulator.simulate_brute_force(LOG_FILE)
    print()

    print("[2/4] Running detection engine...")
    alerts = detector.run_detection(LOG_FILE)
    print()

    print("[3/4] Extracting investigation indicators...")
    iocs = ioc_extractor.extract_iocs(LOG_FILE)
    print()

    print("[4/4] Building incident timeline...")
    timeline = timeline_builder.build_timeline(LOG_FILE)
    print()

    print("=" * 72)
    print("INVESTIGATION COMPLETE")
    print("=" * 72)
    print(f"Security events processed: {len(timeline)}")
    print(f"Detection alerts:          {len(alerts)}")
    print(f"Source IPs identified:     {len(iocs['source_ips'])}")
    print(f"Accounts observed:         {len(iocs['usernames'])}")
    print(f"Telemetry file:            {LOG_FILE.relative_to(ROOT)}")
    print(
        "Incident report:           "
        f"{(ROOT / 'analyst-investigation' / 'incident_report.md').relative_to(ROOT)}"
    )
    print(
        "MITRE mapping:             "
        f"{(ROOT / 'analyst-investigation' / 'mitre_mapping.md').relative_to(ROOT)}"
    )
    print()
    print("Next analyst action: review TT-SSH-001 and validate the successful")
    print("admin authentication and any post-authentication activity.")


if __name__ == "__main__":
    main()
