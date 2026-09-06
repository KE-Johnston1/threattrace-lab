# Playbook PB-AUTH-001 — Suspicious Authentication

**Version:** 1.0  
**Purpose:** Provide a repeatable investigation path for unusual authentication activity.  
**Scope:** Synthetic ThreatTrace training cases.

## Trigger

Use when authentication telemetry shows an unusual failure pattern, an unusual successful login, privileged-account activity, or another authentication anomaly.

## Initial triage

- Record the exact alert ID, timestamp and timezone.
- Confirm source, destination, protocol, port and account.
- Confirm the affected asset and account owner.
- Establish asset criticality and account privilege.
- Determine whether the source and activity are authorised.
- Check expected timing, baseline behaviour, maintenance, deployment, change or security-testing activity.

## Evidence to collect

- Authentication logs and related identity-provider records.
- Source-host and destination-host context.
- Network/firewall/IDS/IPS telemetry.
- Endpoint or EDR-style post-authentication activity.
- Process, session and persistence indicators where available.
- Historical activity for the source, account and destination.

## Investigation questions

- Were the failed attempts genuine authentication failures?
- Was the successful authentication legitimate?
- Does the account owner recognise the activity?
- Is the source host expected to access the destination?
- What happened immediately after successful authentication?
- Is there evidence of lateral movement, persistence, C2 or data access?
- Could maintenance, automation, testing or misconfiguration explain the pattern?

## Escalation criteria

Escalate according to the applicable organisational procedure when evidence indicates, or potentially indicates:

- unauthorised privileged access;
- suspicious post-authentication activity;
- confirmed malicious infrastructure or malware;
- lateral movement or persistence;
- sensitive data access or possible exfiltration;
- multiple correlated alerts or affected assets;
- significant business impact;
- legal, privacy or regulatory considerations;
- inability to safely resolve the case at the current analyst tier.

**Important:** potential escalation criteria are not themselves proof of compromise.

## Response considerations

Depending on evidence and authorisation, actions may include continued monitoring, additional evidence collection, SOC Tier 2 review, incident-response escalation, account protection, credential rotation, network restriction, or remediation. Do not perform containment solely because an alert fired unless the applicable playbook and evidence justify it.

## Legal / privacy consideration

If the investigation involves personal data, sensitive information, regulated systems, customers, employees, contractual obligations or potential reportable impact, preserve evidence and refer the matter through the organisation's legal, privacy or compliance process. This playbook does not provide legal advice or determine that a breach has occurred.

## Closure criteria

Do not close as expected activity until required ownership, authorization, timing, network, change/testing and post-authentication checks are complete. Document the evidence, remaining gaps, rationale, response and escalation decision.

## Lessons learned prompts

- Did the detection provide enough context?
- Was the required telemetry available?
- Were ownership and authorization easy to establish?
- Did the playbook contain the right investigation questions?
- Should a detection, telemetry source or playbook step change?
- What follow-up action has an owner and priority?
