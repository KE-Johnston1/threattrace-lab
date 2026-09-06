"""Post-investigation documentation helpers for ThreatTrace.

These structures keep response, closure, and continuous improvement explicit.
They are documentation aids, not automatic incident declarations.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImprovementAction:
    title: str
    category: str
    owner: str
    priority: str
    status: str = "Open"
    verification: str = ""


@dataclass(frozen=True)
class LessonsLearned:
    case_id: str
    outcome: str
    what_happened: str
    what_went_well: tuple[str, ...]
    what_did_not_go_well: tuple[str, ...]
    detection_improvements: tuple[str, ...]
    investigation_improvements: tuple[str, ...]
    playbook_improvements: tuple[str, ...]
    telemetry_improvements: tuple[str, ...]
    training_lessons: tuple[str, ...]
    follow_up_actions: tuple[ImprovementAction, ...]


def validate_lessons(lessons: LessonsLearned) -> None:
    """Validate the minimum fields required for a useful review."""
    required = {
        "case_id": lessons.case_id,
        "outcome": lessons.outcome,
        "what_happened": lessons.what_happened,
    }
    missing = [name for name, value in required.items() if not value.strip()]
    if missing:
        raise ValueError(f"Missing required lessons-learned fields: {', '.join(missing)}")

    for action in lessons.follow_up_actions:
        if not action.title.strip() or not action.category.strip() or not action.owner.strip():
            raise ValueError("Improvement actions require title, category, and owner")
        if action.priority not in {"Low", "Medium", "High", "Critical"}:
            raise ValueError("Improvement action priority must be Low, Medium, High, or Critical")
        if action.status not in {"Open", "In Progress", "Complete", "Deferred"}:
            raise ValueError("Improvement action status is invalid")


def improvement_summary(lessons: LessonsLearned) -> dict[str, int]:
    """Return counts suitable for a post-case review summary."""
    validate_lessons(lessons)
    actions = lessons.follow_up_actions
    return {
        "total_actions": len(actions),
        "open_actions": sum(action.status == "Open" for action in actions),
        "high_or_critical": sum(action.priority in {"High", "Critical"} for action in actions),
    }
