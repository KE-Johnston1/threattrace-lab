# Defensive Detection

## Purpose

The `defensive-detection` module converts structured SSH telemetry into actionable SOC alerts.

The detector is deliberately explainable: an analyst can trace an alert back to the event pattern that triggered it.

## Detection Rule

### SSH-BRUTE-001 — Multiple SSH Authentication Failures

The rule correlates SSH authentication failures from the same source within a five-minute window.

The scenario is escalated to **HIGH** when successful authentication follows the failed attempts because that creates a potential account-compromise investigation pivot.

The detector does not automatically claim that compromise occurred.

## Example

```text
12 failures
     ↓
successful admin authentication
     ↓
SSH-BRUTE-001
     ↓
HIGH
```

## Run

The repository-level entry point is:

```bash
python main.py
```

The parser can also be run directly against generated telemetry where supported by its command-line interface.

## Analyst Value

The detector demonstrates:

- structured security log parsing
- event correlation
- time-window analysis
- threshold-based detection
- severity escalation
- alert deduplication
- explainable detection rationale

## Important SOC Principle

A detection is **not the same thing as proof of compromise**.

Authentication failures can have benign causes, including user error or misconfigured services. The detector therefore creates an investigation lead; the analyst uses additional evidence to determine what happened.

## Safety

The module processes synthetic local telemetry and does not perform network scanning, authentication attempts, or attacks against external systems.

## Status

**Implemented:** SSH brute-force detection and correlated successful-authentication escalation.
