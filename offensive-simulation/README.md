# Offensive Simulation

## Purpose

The `offensive-simulation` module generates **controlled, synthetic security telemetry** for the ThreatTrace SOC investigation pipeline.

It does not perform real attacks, connect to external systems, attempt authentication, or scan networks.

The goal is to create realistic, repeatable evidence that the defensive and analyst layers can process.

## Current Scenario: SSH Brute Force

The simulator models:

```text
Repeated SSH authentication failures
            ↓
Targeted account activity
            ↓
Successful SSH authentication
```

The scenario uses a synthetic source and destination and writes structured events locally.

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

## Run the Simulator

From this directory:

```bash
python brute_force_simulator.py
```

Or use the repository-level pipeline:

```bash
python ../main.py
```

The simulator writes generated test telemetry to `brute_force.log`.

## Why Simulate Instead of Attack?

ThreatTrace demonstrates security detection without creating unnecessary risk. The simulator produces the **telemetry an attack might create** without performing authentication attempts against a real service.

This makes the project safe to share as a public portfolio repository.

## SOC Integration

```text
Synthetic Scenario
       ↓
Structured Telemetry
       ↓
Detection Engine
       ↓
SOC Alert
       ↓
Analyst Investigation
```

## Status

**Implemented:** controlled SSH authentication telemetry simulation.
