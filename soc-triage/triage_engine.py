"""Deterministic SOC alert triage for synthetic ThreatTrace cases.

The engine separates detection from analyst assessment. It never labels an
alert as compromised solely because a detection rule fired.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TriageInput:
    alert_id: str
    source_ip: str
    destination_ip: str
    account: str
    successful_login: bool
    owner_verified: bool = False
    authorization_verified: bool = False
    timing_verified: bool = False
    post_auth_reviewed: bool = False
    network_reviewed: bool = False
    change_or_testing_checked: bool = False


@dataclass(frozen=True)
class TriageResult:
    assessment: str
    confidence: str
    next_action: str
    rationale: str
    evidence_gaps: tuple[str, ...]


def triage_alert(case: TriageInput) -> TriageResult:
    """Return the least-assumptive assessment supported by the supplied evidence."""
    gaps = []

    if not case.owner_verified:
        gaps.append("asset or account ownership is not verified")
    if not case.authorization_verified:
        gaps.append("authorization for the activity is not verified")
    if not case.timing_verified:
        gaps.append("activity timing is not verified against expected use")
    if not case.network_reviewed:
        gaps.append("related network evidence has not been reviewed")
    if not case.change_or_testing_checked:
        gaps.append("maintenance, deployment, change, or security-testing context has not been checked")
    if case.successful_login and not case.post_auth_reviewed:
        gaps.append("successful session and post-authentication activity have not been reviewed")

    if not case.owner_verified or not case.authorization_verified:
        return TriageResult(
            assessment="Insufficient Evidence",
            confidence="Low",
            next_action="Continue investigation",
            rationale="The alert identifies suspicious authentication activity, but ownership and authorization are not established.",
            evidence_gaps=tuple(gaps),
        )

    if case.successful_login and not case.post_auth_reviewed:
        return TriageResult(
            assessment="Requires Investigation",
            confidence="Medium",
            next_action="Review the successful session and correlate endpoint/network evidence",
            rationale="A successful authentication followed the detected failure pattern; this requires validation before any compromise conclusion.",
            evidence_gaps=tuple(gaps),
        )

    if gaps:
        return TriageResult(
            assessment="Requires Investigation",
            confidence="Medium",
            next_action="Collect the remaining contextual evidence",
            rationale="Some contextual checks remain incomplete, so the alert should not be closed as expected activity yet.",
            evidence_gaps=tuple(gaps),
        )

    return TriageResult(
        assessment="Expected",
        confidence="High",
        next_action="Document rationale and close if the applicable playbook permits",
        rationale="Ownership, authorization, timing, network context, change/testing context, and post-authentication review are all verified.",
        evidence_gaps=(),
    )


def summarise_gaps(results: Iterable[TriageResult]) -> list[str]:
    """Return unique evidence gaps across triage results."""
    return sorted({gap for result in results for gap in result.evidence_gaps})
