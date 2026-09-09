# ThreatTrace Security Audit

**Scope:** ThreatTrace Lab repository as a local educational/portfolio project.

**Audit objective:** identify security, privacy, safety and legal-risk areas before public portfolio use. This is a portfolio security review, not a legal opinion or a penetration test.

## Executive assessment

**Overall risk: Low for the current intended use.**

The project is designed around synthetic telemetry and local processing. The simulator does not create network connections or attempt authentication. The browser demonstrations are static and do not contact external systems.

The main risks are not active exploitation paths; they are portfolio hygiene risks such as accidentally introducing real credentials, personal data, public targets, unsafe attack functionality, or unreviewed AI-generated code.

## Findings

| ID | Area | Severity | Finding | Status |
|---|---|---:|---|---|
| TT-SEC-001 | Network activity | Low | The simulator generates text telemetry locally and does not perform real authentication or scanning. | Pass |
| TT-SEC-002 | Data privacy | Low | Current sample data is synthetic and uses private/documentation-safe addresses. Real personal, customer or employer data must not be added. | Pass / ongoing control |
| TT-SEC-003 | Browser demo | Low | The demo uses `innerHTML`, but its current values are hard-coded. If future telemetry becomes user-controlled, DOM injection/XSS must be addressed. | Accepted risk |
| TT-SEC-004 | File output | Low | Python helpers accept local output paths. They do not execute shell commands or make network requests. Callers should use trusted local paths. | Accepted risk |
| TT-SEC-005 | Dependencies | Low | The heatmap component uses third-party Python packages. Dependencies should be reviewed and updated periodically. | Open maintenance item |
| TT-SEC-006 | CI permissions | Low | GitHub Actions now explicitly requests read-only repository contents permission. | Fixed |
| TT-SEC-007 | Offensive capability | Low | The former offensive-simulation component is a synthetic telemetry generator, not a network attack tool. Its documentation must continue to make that distinction explicit. | Pass |
| TT-SEC-008 | Secrets | Low | No credentials, API keys or tokens are required by the project. Do not add real secrets to examples, tests or screenshots. | Pass / ongoing control |

## Safety boundaries

ThreatTrace should remain within these boundaries:

- Generate or analyse synthetic/local telemetry only.
- Do not add real credential attacks, scanning of third-party systems, exploitation, persistence, credential harvesting, phishing delivery or automated containment against external systems.
- Use RFC 1918/private or documentation-safe IP addresses in examples.
- Do not commit real employee, customer, employer or personal data.
- Do not commit passwords, API keys, access tokens, private keys or session cookies.
- Keep the project clearly labelled as an educational portfolio lab rather than production SOC tooling.

## Secure-development controls

The repository uses version control and automated testing. The CI workflow now declares `contents: read` permissions rather than relying on broader default permissions.

When modifying the project, review:

1. New dependencies and their provenance.
2. Any new network access.
3. Any file-writing or command-execution functionality.
4. Any browser output that could contain untrusted data.
5. Any telemetry that could contain personal or confidential information.
6. GitHub Actions permissions and third-party actions.

## AI-assisted development

AI assistance is not itself a security problem. The important control is human review. AI-generated code can contain vulnerabilities or incorrect assumptions, so generated or suggested code should be reviewed, understood, tested and security-checked before being treated as finished work.

The project should not claim that every line was manually authored if that is not true. A short AI-use disclosure is recommended for transparency, while the author remains responsible for the final code and decisions.

## Legal / ethical boundary

This repository is intentionally defensive and synthetic. Its documentation should never imply that real systems were attacked or that production incident-response experience was obtained from this lab.

Whether a particular activity is lawful depends on the system, authorisation, facts and applicable law. The safest portfolio position is therefore to keep demonstrations local, synthetic and explicitly authorised.

## Review result

**No high-severity issue was identified in the reviewed ThreatTrace components.**

The most important ongoing controls are:

- keep the project synthetic;
- avoid real targets and credentials;
- review AI-assisted code rather than blindly accepting it;
- keep dependencies and CI under review; and
- preserve the distinction between a portfolio lab and production SOC experience.

**Next review trigger:** any addition involving network communication, external APIs, authentication, user-supplied telemetry, new dependencies, or automated response actions.
