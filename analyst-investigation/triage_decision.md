# Evidence-Based Triage Decision

ThreatTrace treats an alert as an investigation lead, not a verdict.

## Case: TT-SSH-001

**Observed:** 12 SSH authentication failures from `10.10.10.50`, targeting multiple usernames, followed by a successful `admin` authentication.

## Triage principle

A user's confirmation that they performed an action is useful evidence, but it should not be the sole reason to close a security alert. The analyst should verify the identity/account context and correlate the claim with telemetry before closing the case.

## Closure checklist

Before closing as **Benign / Expected**, verify as applicable:

- [ ] The individual/account owner has been verified using an appropriate organisational process.
- [ ] The source IP or host is consistent with the user's expected environment.
- [ ] The authentication time is consistent with expected activity.
- [ ] The successful session is attributable to the verified user/account.
- [ ] No suspicious post-authentication activity is identified.
- [ ] Relevant network telemetry has been reviewed or its absence documented.
- [ ] The applicable organisational playbook/policy does not require escalation.
- [ ] The evidence and rationale for closure are documented.

## If verification fails

Do **not** close the case simply because the user claimed the activity was legitimate. Continue investigation and gather additional evidence. Escalate when the applicable organisational policy or playbook requires it.

## Example decision

> The account owner confirms the login, but confirmation alone is insufficient for closure. The analyst verifies the account owner, confirms the source and timing are expected, reviews the successful session for anomalous activity, and checks the relevant playbook. If the evidence is consistent with legitimate activity and no escalation criteria are met, the alert can be documented and closed as Benign / Expected.

## Important distinction

**Detection:** identifies a pattern worth investigating.

**Triage:** determines whether the pattern has a plausible benign explanation and what evidence is still needed.

**Incident response:** follows organisational policy and playbooks when escalation criteria are met.

ThreatTrace intentionally keeps these stages separate so that automation does not silently convert an alert into an incident declaration.