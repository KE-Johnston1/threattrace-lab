# SOC Alert Triage

ThreatTrace now includes a focused SOC alert triage layer on top of the existing SSH detection and investigation workflow.

## Analyst workflow

```text
Alert intake → validate → identify asset/account/owner
      ↓
Expected activity / authorization / change context
      ↓
Authentication + network + endpoint correlation
      ↓
Timeline + evidence gaps
      ↓
Least-assumptive assessment
      ↓
Investigate / monitor / escalate / contain / remediate / close
```

## Triage principle

**An alert is an investigation lead, not a verdict.** A high-severity detection can justify prompt investigation without proving compromise. The analyst distinguishes what telemetry directly shows from what remains a hypothesis.

## Assessment states

- **Expected** — evidence supports legitimate activity and required closure checks are complete.
- **Requires Investigation** — activity is concerning or inconsistent with expectations, but intent or compromise is not established.
- **Insufficient Evidence** — key ownership, authorization, timing, network, endpoint, or contextual evidence is missing.
- **Security Concern** — correlated indicators support escalation under the applicable incident-response process.

The engine intentionally does not create a `Confirmed Compromise` verdict from a single detection signal.

## Evidence priorities

1. Exact alert timestamp and timezone.
2. Source, destination, protocol, port and affected account.
3. Asset ownership, business purpose and criticality.
4. Authorization and expected activity.
5. Maintenance, deployment, change, or authorised security-testing context.
6. Authentication, network and endpoint/post-authentication telemetry.
7. Business impact and applicable escalation criteria.

## Synthetic cases

`data/soc_alerts.json` contains documentation-safe training cases using private lab addresses. No production credentials, customer data, or real attack traffic are required.

## Python triage engine

`triage_engine.py` provides deterministic, explainable decisions from explicit evidence fields and records evidence gaps instead of assuming missing facts.

```python
from soc_triage.triage_engine import TriageInput, triage_alert

result = triage_alert(TriageInput(
    alert_id="TT-SSH-001",
    source_ip="10.10.10.50",
    destination_ip="10.10.10.10",
    account="admin",
    successful_login=True,
))

print(result.assessment)
print(result.evidence_gaps)
```

## Relationship to ThreatTrace

The new layer does not replace the existing detection, timeline, hypothesis, ATT&CK, or incident-report components. It makes the SOC sequence explicit:

**Detection → Triage → Evidence Correlation → Investigation → Assessment → Response**
