"""ThreatTrace Lab - end-to-end SOC investigation launcher.

Run this file from the repository root to execute the synthetic SSH
investigation and evidence-based triage workflow.

All activity is local and synthetic. No network connections are performed.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from soc_triage.triage_engine import TriageInput, triage_alert

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
    print("THREATTRACE LAB - SOC ALERT TRIAGE & INVESTIGATION")
    print("=" * 72)
    print("Scenario: SSH brute-force pattern followed by successful authentication")
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

    print("[1/5] Generating synthetic telemetry...")
    simulator.simulate_brute_force(LOG_FILE)
    print()

    print("[2/5] Running detection engine...")
    alerts = detector.run_detection(LOG_FILE)
    print()

    print("[3/5] Extracting investigation indicators...")
    iocs = ioc_extractor.extract_iocs(LOG_FILE)
    print()

    print("[4/5] Building incident timeline...")
    timeline = timeline_builder.build_timeline(LOG_FILE)
    print()

    print("[5/5] Performing evidence-based SOC triage...")
    if alerts:
        alert = alerts[0]
        triage = triage_alert(
            TriageInput(
                alert_id=alert["alert_id"],
                source_ip=alert["source_ip"],
                destination_ip=alert["destination_ip"],
                account=alert["account"],
                successful_login=alert["successful_login"],
            )
        )
        print(f"Assessment:    {triage.assessment}")
        print(f"Confidence:    {triage.confidence}")
        print(f"Next action:   {triage.next_action}")
        print(f"Rationale:     {triage.rationale}")
        print("Evidence gaps:")
        for gap in triage.evidence_gaps:
            print(f"  - {gap}")
    else:
        print("No detection alert was generated; no triage case was created.")
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
    print("Analyst principle: the detection is a lead; the assessment depends on")
    print("validated context and correlated evidence, not the alert alone.")


if __name__ == "__main__":
    main()
