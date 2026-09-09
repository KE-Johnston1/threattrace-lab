# Synthetic Telemetry Generator

## Purpose

The `offensive-simulation` directory contains a **controlled, synthetic security telemetry generator** for the ThreatTrace investigation pipeline.

It does not perform real attacks, connect to external systems, attempt authentication, or scan networks.

The goal is to create realistic, repeatable evidence that the defensive and analyst layers can process.

## Current Scenario: SSH Authentication Attack Pattern

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

## Run the Generator

From this directory:

```bash
python brute_force_simulator.py
```

Or use the repository-level pipeline:

```bash
python ../main.py
```

The generator writes synthetic test telemetry to `brute_force.log`.

## Why Generate Telemetry Instead of Attack?

ThreatTrace demonstrates defensive security detection without creating unnecessary risk. The generator produces the **telemetry an attack might create** without performing authentication attempts against a real service.

This keeps the project suitable for a public portfolio and makes the safety boundary explicit.

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

**Implemented:** controlled SSH authentication telemetry generation for local defensive analysis.
