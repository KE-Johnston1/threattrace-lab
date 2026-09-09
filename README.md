# ThreatTrace Lab

> **Interactive SOC investigation portfolio lab: synthetic telemetry → detection → evidence → assessment.**

[![Status](https://img.shields.io/badge/status-active-success)](#project-status)
[![Safety](https://img.shields.io/badge/safety-synthetic%20telemetry-blue)](#data-and-safety)

## Start Here

### Recruiter Demo

Open [`docs/recruiter-demo.html`](docs/recruiter-demo.html) for the guided investigation experience.

For a visual evidence summary, open [`docs/analyst-dashboard.html`](docs/analyst-dashboard.html).

For the evidence-correlation experience, open [`docs/investigation-console.html`](docs/investigation-console.html).

The project follows one simple model:

**Alert → evidence → investigation → assessment → response/monitoring**

### Run the Python pipeline

From the repository root:

```bash
python main.py
```

The pipeline generates synthetic SSH telemetry and runs the defensive investigation workflow.

### Run the tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions also runs the test suite automatically on pushes and pull requests.

---

## Why I Built ThreatTrace

After completing CySA+, I wanted to demonstrate my understanding through practical work rather than relying on the certification alone. ThreatTrace is my attempt to show that I can investigate a security alert logically and methodically.

The core principle is simple: **an alert should start an investigation, not end it.**

The alert is an allegation; telemetry is evidence. The analyst's job is to examine the evidence, consider alternative explanations, correlate additional information, and reach an assessment that the evidence supports.

This is a learning project, not production SOC experience. It uses synthetic telemetry and does not represent operation of a live SOC.

---

## What is ThreatTrace?

ThreatTrace is a deliberately safe cybersecurity portfolio project demonstrating how a junior SOC analyst can move from raw security events to an actionable investigation.

The current scenario focuses on suspicious SSH authentication activity: repeated failures from one source followed by a successful authentication to an administrative account.

The project does **not** perform real brute-force attacks or attempt authentication against external systems. The activity is simulated locally as structured telemetry.

---

## The ThreatTrace Investigation Model

```text
                    ALERT
                      │
                The allegation
                      │
                      ▼
                  EVIDENCE
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
 Authentication    Network        Account /
     logs          telemetry       endpoint
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                 INVESTIGATION
                      │
                      ▼
                 ASSESSMENT
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
     Benign       Suspicious      Malicious
                      │
                      ▼
             RESPONSE / MONITORING
```

The application deliberately keeps the analyst involved. Detection logic can identify a pattern, but the analyst decides what the evidence supports.

---

## Current Scenario

ThreatTrace demonstrates:

- SSH authentication failures
- Correlation by source IP
- A five-minute detection window
- A repeated-failure threshold
- Successful authentication following failed attempts
- Severity escalation when the failure pattern is followed by success
- IOC extraction
- Chronological investigation timelines
- Hypothesis-driven investigation
- Visual evidence correlation
- MITRE ATT&CK mapping to **T1110 — Brute Force**
- Incident reporting and response recommendations
- Automated unit tests
- GitHub Actions continuous integration

The scenario is synthetic and uses private/documentation-safe IP addresses.

---

## Hypothesis-Driven Investigation

ThreatTrace does not require the analyst to accept the first explanation that fits the alert.

For the current SSH case, possible explanations include:

- legitimate user activity
- a misconfigured automated service
- credential attack activity
- account compromise
- previously unexplained behaviour

Each hypothesis should be tested against available evidence.

See [`analyst-investigation/hypothesis_matrix.md`](analyst-investigation/hypothesis_matrix.md).

---

## Analyst Verdicts

ThreatTrace uses evidence-based assessments rather than automatically declaring compromise:

| Verdict | Meaning |
|---|---|
| **Benign / Expected** | Evidence supports legitimate activity. |
| **Suspicious — Continue Investigation** | Activity is concerning but intent is not established. |
| **Likely Malicious** | Multiple indicators strongly support malicious activity, but further confirmation may still be required. |
| **Confirmed Malicious** | Available evidence establishes malicious activity. |
| **Insufficient Evidence — Continue Monitoring** | Evidence is not sufficient for a reliable conclusion. |

The current case supports **Likely Malicious — Continue Investigation**, because the failure pattern is followed by successful administrative authentication. It does not by itself prove compromise.

---

## Repository Structure

```text
threattrace-lab/
├── main.py
├── offensive-simulation/
│   ├── brute_force_simulator.py
│   └── README.md
├── defensive-detection/
│   ├── log_parser.py
│   └── README.md
├── analyst-investigation/
│   ├── ioc_extractor.py
│   ├── timeline_builder.py
│   ├── timeline_chart.py
│   ├── hypothesis_matrix.md
│   ├── mitre_mapping.md
│   ├── incident_report.md
│   ├── triage_decision.md
│   └── README.md
├── heatmap-visualizer/
│   ├── heatmap_builder.py
│   ├── case-study.md
│   ├── requirements.txt
│   └── samples/
├── soc_triage/
│   └── post_investigation.py
├── docs/
│   ├── recruiter-demo.html
│   ├── analyst-dashboard.html
│   └── investigation-console.html
├── tests/
│   └── test_detection.py
├── SECURITY-AUDIT.md
├── .github/workflows/
│   └── tests.yml
└── LICENSE
```

The project intentionally avoids turning into a full SIEM, SOAR platform or case-management application.

---

## Components

### Synthetic Telemetry Generator

Generates controlled SSH authentication telemetry locally. It models the evidence of a brute-force scenario without performing real authentication attempts.

### Defensive Detection

Parses structured telemetry and correlates authentication failures to identify suspicious SSH activity. The detection rule is documented as `SSH-BRUTE-001`.

### Analyst Investigation

Extracts investigation indicators, builds a chronological timeline, evaluates competing hypotheses, maps the behaviour to MITRE ATT&CK, and documents the incident assessment.

### Visual Analysis

The heatmap component provides a compact visual view of authentication activity. The browser-based analyst dashboard provides a dependency-free visual summary of the evidence, timeline and assessment.

### Recruiter Demo / Investigation Console

Provides browser-based demonstrations of the investigation flow so a reviewer can explore the project without first installing the Python environment.

### Tests and CI

The test suite validates parsing and SSH detection behaviour, including threshold handling, time-window correlation, successful-login escalation, source separation and protocol filtering. GitHub Actions runs these tests automatically on repository changes.

---

## Example Alert

```text
SSH-BRUTE-001
Severity: HIGH

Source IP:        10.10.10.50
Destination IP:   10.10.10.10
Protocol:         SSH
Destination Port: 22
Target Account:   admin
Failed Attempts:  12
Successful Login: YES
```

The correct analyst conclusion is **not automatically "the server was compromised."** The evidence indicates suspicious authentication activity consistent with brute-force behaviour and requires investigation of the successful session and post-authentication activity.

---

## MITRE ATT&CK

The current scenario maps to:

- **T1110 — Brute Force**
- **Tactic:** Credential Access

See [`analyst-investigation/mitre_mapping.md`](analyst-investigation/mitre_mapping.md).

---

## Incident Report

The completed case study is available at [`analyst-investigation/incident_report.md`](analyst-investigation/incident_report.md).

It covers detection evidence, investigation indicators, timeline, ATT&CK mapping, analyst assessment, containment, remediation, preventive controls and lessons learned.

---

## Security Audit

A focused security and safety review is available in [`SECURITY-AUDIT.md`](SECURITY-AUDIT.md).

The current assessment is **low risk for its intended local, synthetic use**. The most important controls are keeping the telemetry synthetic, avoiding real credentials and targets, reviewing AI-assisted code, and maintaining least-privilege CI permissions.

---

## AI-Assisted Development

AI tools were used during development for assistance with coding, debugging, documentation and review. The final project remains the author's responsibility: generated suggestions were reviewed, adapted and tested rather than treated as authoritative.

AI assistance does not mean the project represents production experience. The important claim is what can be demonstrated and explained in the code and investigation workflow.

---

## Data and Safety

ThreatTrace is an educational portfolio environment and is designed to use synthetic security telemetry.

- No real credentials are required or included.
- No production or third-party systems are scanned, attacked or authenticated against.
- The sample authentication events are generated locally for defensive analysis.
- The sample IP addresses use private/documentation-safe address space rather than identifiable public hosts.
- The project should not be populated with real employee, customer, production or other personal data.
- Third-party material, where referenced, remains subject to its original licence and attribution requirements.

This repository is not intended to provide legal advice. If real organisational or personal data is introduced in the future, applicable data-protection, security, contractual and retention requirements must be assessed before use.

---

## Skills Demonstrated

- SOC alert triage
- Detection engineering
- Security log analysis
- Event correlation
- IOC identification
- Hypothesis-driven investigation
- Timeline reconstruction
- MITRE ATT&CK
- Incident response concepts
- Python scripting
- Data visualisation
- Defensive security automation
- Human-in-the-loop analysis
- Automated testing
- Continuous integration
- Technical documentation
- Safe security lab design

---

## Project Status

**Current:** SSH brute-force detection and investigation workflow implemented with interactive demonstrations, visual evidence aids, automated tests, CI and a documented security review.

**Future development:** only small defensive scenarios, targeted test coverage and documentation improvements. The project is intentionally not being expanded into a full SIEM/SOAR or production platform.

---

## Author

**KE-Johnston1**

This repository is maintained as a practical cybersecurity portfolio project and learning environment.
