# ThreatTrace Lab

> **Interactive SOC investigation laboratory demonstrating detection engineering, threat investigation, visual analysis, MITRE ATT&CK mapping, and incident response.**

[![Status](https://img.shields.io/badge/status-active-success)](#project-status)
[![Safety](https://img.shields.io/badge/safety-synthetic%20telemetry-blue)](#safety-and-scope)

## Start Here

### Recruiter Demo

Open [`docs/recruiter-demo.html`](docs/recruiter-demo.html) to explore the interactive investigation experience.

The demo walks through a simulated SSH brute-force scenario:

**Case → telemetry → detection → evidence → investigation → ATT&CK → analyst verdict → response/monitoring**

### Run the Python pipeline

From the repository root:

```bash
python main.py
```

The pipeline generates synthetic SSH telemetry and runs the defensive investigation workflow.

---

## Why I Built ThreatTrace

After completing CySA+, I wanted to demonstrate my understanding through practical work rather than relying on the certification alone. ThreatTrace is my attempt to show that I can investigate a security alert logically and methodically.

The project is built around a simple idea: **an alert should start an investigation, not end it.**

I think of the alert as an allegation and the telemetry as evidence. The analyst's job is to examine the evidence, consider alternative explanations, correlate additional information, and reach an assessment that the evidence supports.

This is also why ThreatTrace uses a **human-in-the-loop** approach. Automation is valuable for processing telemetry and identifying patterns quickly, but it should work in partnership with human judgement rather than replace it. If an automated component fails, produces an incorrect result, or encounters behaviour it does not understand, the analyst still needs enough visibility to challenge the result and investigate further.

---

## What is ThreatTrace?

ThreatTrace is a deliberately safe cybersecurity portfolio project designed to demonstrate how a junior SOC analyst can move from raw security events to an actionable investigation.

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

## Analyst Verdicts

ThreatTrace provides five possible assessments:

| Verdict | Meaning |
|---|---|
| **Benign / Expected** | Evidence supports legitimate activity. |
| **Suspicious — Continue Investigation** | Activity is concerning but intent is not established. |
| **Likely Malicious** | Multiple indicators strongly support malicious activity, but further confirmation may still be required. |
| **Confirmed Malicious** | Available evidence establishes malicious activity. |
| **Insufficient Evidence — Continue Monitoring** | Evidence is not sufficient for a reliable conclusion; preserve visibility, correlate additional telemetry, and monitor for recurrence or new indicators. |

The final category is important: uncertainty is itself an assessment. A previously unknown attack technique is one possibility when activity remains unexplained, but a zero-day should never be assumed without supporting evidence.

---

## SOC Workflow

```text
Synthetic Security Activity
            ↓
       Structured Logs
            ↓
      Detection Engine
            ↓
         SOC Alert
            ↓
      Evidence Review
            ↓
      IOC Extraction
            ↓
        Timeline
            ↓
    Visual Analysis
            ↓
    MITRE ATT&CK Mapping
            ↓
     Analyst Assessment
            ↓
   Response / Monitoring
```

This separation is intentional: a detection identifies suspicious behaviour; an investigation gathers evidence; an analyst makes the final assessment.

---

## Detection Scenario

ThreatTrace currently demonstrates:

- SSH authentication failures
- Correlation by source IP
- A five-minute detection window
- A threshold of repeated failures
- Successful authentication following failed attempts
- High-severity escalation when the failure pattern is followed by success
- IOC extraction
- Chronological investigation timelines
- Hypothesis-driven investigation
- MITRE ATT&CK mapping to **T1110 — Brute Force**
- Incident reporting and response recommendations

The scenario is synthetic and uses documentation-safe private IP addresses.

---

## Hypothesis-Driven Investigation

ThreatTrace does not require the analyst to accept the first explanation that fits the alert.

For the current SSH case, possible explanations include:

- legitimate user activity
- a misconfigured automated service
- credential attack activity
- account compromise
- previously unexplained or novel behaviour

Each hypothesis should be tested against available evidence.

See [`analyst-investigation/hypothesis_matrix.md`](analyst-investigation/hypothesis_matrix.md).

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
│   └── README.md
├── heatmap-visualizer/
│   ├── heatmap_builder.py
│   ├── anomaly_detector.py
│   ├── signature_matcher.py
│   ├── case-study.md
│   ├── requirements.txt
│   └── samples/
├── docs/
│   └── recruiter-demo.html
├── shared-assets/
└── LICENSE
```

---

## Components

### Offensive Simulation

Generates controlled, synthetic SSH authentication telemetry. It models the evidence of a brute-force scenario without performing real authentication attempts.

### Defensive Detection

Parses structured telemetry and correlates authentication failures to identify suspicious SSH activity. The detection rule is documented as `SSH-BRUTE-001`.

### Analyst Investigation

Extracts investigation indicators, builds a chronological timeline, evaluates competing hypotheses, maps the behaviour to MITRE ATT&CK, and documents the incident assessment.

### Heatmap Visualizer

Provides visual analysis of authentication activity so an analyst can identify concentrated activity and use the visualisation as supporting evidence during investigation.

### Recruiter Demo

Provides a browser-based, dependency-free demonstration of the investigation flow so a reviewer can explore the project without first installing the Python environment.

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

It covers:

- executive summary
- detection evidence
- investigation indicators
- timeline
- ATT&CK mapping
- analyst assessment
- containment
- remediation
- preventive controls
- lessons learned

---

## Testing

Automated tests are a planned next step. Until the test suite is added, the recommended validation is to run the simulator and then the detection pipeline locally and inspect the generated output.

```bash
python main.py
```

The project is being developed with a focus on deterministic, explainable detection logic rather than opaque scoring.

---

## Skills Demonstrated

This project is intended to demonstrate practical exposure to:

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
- Technical documentation
- Safe security lab design

---

## Safety and Scope

ThreatTrace is an educational and portfolio environment.

The attack scenario is simulated locally and generates synthetic security telemetry. It does not scan, attack, authenticate to, or otherwise interact with production or third-party systems.

Any future expansion should retain the same controlled-lab principle.

---

## Project Status

**Current:** SSH brute-force detection and investigation workflow implemented, with an interactive evidence-driven recruiter demonstration, hypothesis matrix, and visual analysis components.

**Next priorities:** automated tests, stronger end-to-end integration, additional scenarios, and continued documentation refinement.

---

## Author

**KE-Johnston1**

This repository is maintained as a practical cybersecurity portfolio project and learning environment.
