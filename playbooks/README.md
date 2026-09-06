# ThreatTrace SOC Playbooks

Playbooks define repeatable analyst actions without forcing a predetermined verdict.

## Standard playbook structure

1. Purpose
2. Trigger conditions
3. Initial triage
4. Evidence to collect
5. Questions to answer
6. Containment considerations
7. Escalation criteria
8. Legal/privacy considerations
9. Communication requirements
10. Recovery and remediation
11. Closure criteria
12. Required documentation
13. Lessons-learned prompts

## Analyst rule

A playbook is a decision-support procedure, not proof that an incident occurred. An alert may trigger a playbook while the final assessment remains **Expected**, **Requires Investigation**, **Insufficient Evidence**, or **Security Concern**.

## Current playbook

- [`suspicious-authentication.md`](suspicious-authentication.md)

Future playbooks can cover phishing, impersonation, malware, C2, possible exfiltration, insider-threat indicators, vulnerability exploitation, and identity/MFA attacks.
