# MITRE ATT&CK Mapping

## Incident

**Case:** TT-SSH-001 — Suspected SSH Brute-Force / Account Compromise

## Technique Mapping

### T1110 — Brute Force

**Tactic:** Credential Access

**Evidence:**

- Multiple `SSH_AUTH_FAILURE` events were generated from the same source IP.
- The failures occurred within the detection window used by `SSH-BRUTE-001`.
- The activity repeatedly targeted the `admin` account.
- A successful SSH authentication followed the failed attempts.

**Assessment:**

The observed authentication pattern is consistent with a brute-force credential attack against an SSH service. Because the scenario includes a subsequent successful authentication from the same source, the event should be investigated as a potential account compromise rather than treated as failed authentication noise.

**Confidence:** High

## Analyst Notes

The simulator produces synthetic telemetry for defensive analysis. The ATT&CK mapping describes the simulated behaviour and does not claim that a real system was compromised.

## Investigation Pivot

The successful authentication is the key pivot for the analyst. Further investigation should determine whether the `admin` login was authorised and, if not, identify activity performed during the resulting session.

## Recommended Follow-up

1. Investigate the source host associated with the source IP.
2. Validate whether the `admin` login was expected.
3. Review commands and activity after authentication.
4. Search for the source IP across available security telemetry.
5. Reset or otherwise protect the account if compromise is confirmed.
