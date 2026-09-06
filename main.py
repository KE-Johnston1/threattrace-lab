"""ThreatTrace Lab - end-to-end SOC investigation launcher.

Run this file from the repository root to execute the synthetic SSH
investigation and evidence-based triage workflow.

All activity is local and synthetic. No network connections are performed.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from soc_triage.post_investigation import (
    ImprovementAction,
    LessonsLearned,
    improvement_summary,
)
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

    print("[1/7] Generating synthetic telemetry...")
    simulator.simulate_brute_force(LOG_FILE)
    print()

    print("[2/7] Running detection engine...")
    alerts = detector.run_detection(LOG_FILE)
    print()

    print("[3/7] Extracting investigation indicators...")
    iocs = ioc_extractor.extract_iocs(LOG_FILE)
    print()

    print("[4/7] Building incident timeline...")
    timeline = timeline_builder.build_timeline(LOG_FILE)
    print()

    triage = None
    if alerts:
        print("[5/7] Performing evidence-based SOC triage...")
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
        print("[5/7] No detection alert was generated; no triage case was created.")
    print()

    print("[6/7] Applying investigation playbook guidance...")
    print("Playbook:       PB-AUTH-001 — Suspicious Authentication")
    print("Escalation:     Follow escalation criteria when evidence and risk justify it")
    print("Closure rule:   Do not close as expected activity while required evidence gaps remain")
    print()

    print("[7/7] Recording lessons learned and improvement actions...")
    lessons = LessonsLearned(
        case_id=alerts[0]["alert_id"] if alerts else "NO-ALERT",
        outcome="Investigation remains evidence-dependent; closure requires applicable verification.",
        what_happened="Repeated SSH authentication failures were followed by a successful authentication in synthetic telemetry.",
        what_went_well=("Detection and timeline correlation identified the authentication sequence.",),
        what_did_not_go_well=("Ownership, authorization and post-authentication context are not established by the alert alone.",),
        detection_improvements=("Retain correlation between authentication failures and subsequent successful logins.",),
        investigation_improvements=("Verify account ownership and authorization early in triage.",),
        playbook_improvements=("Require explicit post-authentication review before closure.",),
        telemetry_improvements=("Improve endpoint and network context available to the analyst.",),
        training_lessons=("An alert is an investigation lead, not proof of compromise.",),
        follow_up_actions=(
            ImprovementAction(
                "Add ownership and authorization verification to the triage checklist",
                "Investigation",
                "SOC",
                "Medium",
            ),
            ImprovementAction(
                "Improve post-authentication telemetry coverage",
                "Telemetry",
                "Security Engineering",
                "High",
            ),
        ),
    )
    summary = improvement_summary(lessons)
    print(f"Improvement actions: {summary['total_actions']}")
    print(f"Open actions:        {summary['open_actions']}")
    print(f"High/Critical:       {summary['high_or_critical']}")
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
    print("Playbook:                  playbooks/suspicious-authentication.md")
    print("Lessons learned:           docs/lessons-learned.md")
    print()
    print("Analyst principle: the detection is a lead; the assessment depends on")
    print("validated context and correlated evidence, not the alert alone.")


if __name__ == "__main__":
    main()
