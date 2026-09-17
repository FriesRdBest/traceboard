from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal


class ContributionStatus(StrEnum):
    DRAFT = "draft"
    INTAKE = "intake"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTING = "implementing"
    RELEASED = "released"


class Surface(StrEnum):
    ANSWER = "answer"
    SEARCH = "search"
    FOLLOW_UP = "follow_up"
    NAVIGATION = "navigation"
    SETTINGS = "settings"
    OTHER = "other"


class Platform(StrEnum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"
    DESKTOP = "desktop"


@dataclass(frozen=True)
class ContributionLink:
    """
    Lightweight link contract for attaching related component/token IDs
    or external references (e.g., Figma, Linear, PRs).
    """

    link_type: Literal["component", "token", "figma", "linear", "pr", "other"]
    url: str | None = None
    ref_id: str | None = None

    def __post_init__(self) -> None:
        if self.url is None and self.ref_id is None:
            raise ValueError("ContributionLink must define either url or ref_id")


@dataclass
class Contribution:
    """
    Core domain model for a design-system contribution.

    This model is completely decoupled from persistence and UI.
    It acts as a stable contract for intake, review, and release workflows.
    """

    title: str
    problem_statement: str
    user_context: str
    surface: Surface
    platforms: tuple[Platform, ...]
    status: ContributionStatus = ContributionStatus.DRAFT
    submitted_by: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    links: tuple[ContributionLink, ...] = field(default_factory=tuple)

    # Optional references to domain tokens/components (IDs only)
    related_token_ids: tuple[str, ...] = field(default_factory=tuple)
    related_component_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.problem_statement.strip():
            raise ValueError("problem_statement cannot be empty")
        if not self.user_context.strip():
            raise ValueError("user_context cannot be empty")
        if len(self.platforms) == 0:
            raise ValueError("platforms must contain at least one platform")
