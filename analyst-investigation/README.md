# Analyst Investigation

## Purpose

The `analyst-investigation` module represents the investigation stage of the ThreatTrace SOC workflow.

It takes the evidence produced by the detection pipeline and turns it into information an analyst can use to assess an incident.

## Investigation Workflow

```text
SOC Alert
   ↓
IOC Extraction
   ↓
Timeline Reconstruction
   ↓
Visual Analysis
   ↓
MITRE ATT&CK Mapping
   ↓
Analyst Assessment
   ↓
Incident Report
```

## Components

### `ioc_extractor.py`

Extracts investigation indicators from structured telemetry, including source and destination IPs, accounts, protocol, port, event types, and observed time range.

### `timeline_builder.py`

Reconstructs authentication activity chronologically so the analyst can identify the sequence of failures and successful authentication.

### `timeline_chart.py`

Provides a visual representation of the investigation timeline.

### `mitre_mapping.md`

Documents the mapping of the simulated behaviour to **T1110 — Brute Force** under the Credential Access tactic.

### `incident_report.md`

Documents the complete case assessment, evidence, response recommendations, and lessons learned.

## Key Investigation Principle

The successful login is an investigation pivot, not automatic proof of compromise.

The analyst should validate whether the authentication was authorised and review post-authentication activity before concluding that an account was compromised.

## Safety

All evidence in the current scenario is synthetic and generated for a controlled portfolio environment.

## Status

**Implemented:** IOC extraction, timeline reconstruction, ATT&CK mapping, and incident reporting for the SSH scenario.
