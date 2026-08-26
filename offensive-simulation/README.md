# Offensive Simulation

## Purpose

The offensive-simulation module generates **controlled, synthetic security telemetry** for the ThreatTrace SOC investigation pipeline.

It does not perform real attacks, connect to external systems, attempt authentication, or scan networks.

The purpose is to create repeatable security events that can be consumed by the defensive detection and analyst investigation layers.

## Current Scenario: SSH Brute Force

The current simulator creates a controlled SSH authentication scenario:

```text
12 authentication failures
        ↓
Repeated targeting of the admin account
        ↓
Successful admin authentication
```

All events originate from the same synthetic source IP so that the defensive layer can identify the activity as a correlated authentication attack.

## Generated Telemetry

Each event contains:

- UTC timestamp
- Event type
- Protocol
- Source IP
- Destination IP
- Destination port
- Username

Example:

```text
2026-08-26T11:30:00Z | SSH_AUTH_FAILURE | protocol=SSH | src=10.10.10.50 | dst=10.10.10.10 | dst_port=22 | user=admin
```

## Reproducibility

The simulator uses a fixed random seed by default so that the same scenario can be reproduced during testing and demonstrations.

```bash
python brute_force_simulator.py
```

The generated telemetry is written to:

```text
brute_force.log
```

`brute_force.log` is generated test data and should not be treated as source code or real system telemetry.

## SOC Integration

The intended ThreatTrace workflow is:

```text
Synthetic Attack Scenario
          ↓
Security Telemetry
          ↓
Detection Engine
          ↓
SOC Alert
          ↓
Analyst Triage
          ↓
IOC Extraction + Timeline
          ↓
MITRE ATT&CK Mapping
          ↓
Incident Report
          ↓
Response Recommendations
```

## Safety and Ethical Use

This module is designed exclusively for defensive learning, testing, and portfolio demonstration. The simulator produces local synthetic data and does not interact with real hosts or services.

## Status

**Implemented:** SSH brute-force telemetry simulation.

**Next:** Integrate the generated telemetry with the defensive detection engine and produce a SOC alert for correlated failed and successful SSH authentication events.
