# Hypothesis-Driven Investigation

ThreatTrace treats an alert as an investigation lead rather than a verdict.

The analyst should consider competing explanations and identify the evidence that would increase or decrease confidence in each one.

## Case TT-SSH-001

**Observed:** 12 SSH authentication failures from `10.10.10.50`, followed by a successful authentication to `admin`.

| Hypothesis | Supporting evidence | Evidence that would challenge it | Useful next telemetry |
|---|---|---|---|
| Legitimate user activity | Known administrator; expected login time/location | User denies activity; unusual source; unexplained post-login actions | User/account context, authentication logs |
| Misconfigured automated service | Repeated predictable attempts | No associated service; interactive login follows | Service inventory, endpoint telemetry |
| Credential attack | Many failures against accounts followed by success | Authorised source and normal admin behaviour | Authentication logs, network telemetry |
| Account compromise | Successful admin login plus suspicious post-authentication behaviour | Login is verified as authorised and no anomalous activity follows | Endpoint/process telemetry, network telemetry |
| Unknown / novel behaviour | Activity does not match known patterns | Evidence fits a known benign or malicious explanation | Broader correlation and historical baseline |

## Analyst Principle

Do not choose a hypothesis because it sounds dramatic. Choose the assessment best supported by the available evidence, and state what evidence is still missing.

## Evidence Priorities

1. **Authentication context** — who authenticated, from where, when, and whether it was expected.
2. **Network context** — whether the source and destination relationship is expected and whether related connections occurred.
3. **Endpoint/post-authentication activity** — what happened after successful authentication.
4. **Historical context** — whether this behaviour is normal for the account, host, and source.

## Monitoring Unknown Activity

Insufficient evidence is not a reason to invent a conclusion. Preserve relevant telemetry, maintain monitoring, and look for recurrence or new indicators. Previously unknown attack behaviour is one possible explanation, but it requires supporting evidence before being treated as a zero-day or novel exploit.
