from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from traceboard.domain.contribution import (
    Contribution,
    ContributionLink,
    ContributionStatus,
    Platform,
    Surface,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.application.ports.contribution_repository import ContributionRepository


@dataclass(frozen=True)
class CreateContributionCommand:
    """Input boundary for creating a Contribution."""

    title: str
    problem_statement: str
    user_context: str
    surface: Surface
    platforms: tuple[Platform, ...]
    submitted_by: str | None = None
    links: tuple[ContributionLink, ...] = field(default_factory=tuple)
    related_token_ids: tuple[str, ...] = field(default_factory=tuple)
    related_component_ids: tuple[str, ...] = field(default_factory=tuple)


class ContributionService:
    """Application service for contribution creation and retrieval."""

    def __init__(self, repository: ContributionRepository) -> None:
        self._repository = repository

    def create(self, command: CreateContributionCommand) -> Contribution:
        contribution = Contribution(
            title=command.title,
            problem_statement=command.problem_statement,
            user_context=command.user_context,
            surface=command.surface,
            platforms=command.platforms,
            status=ContributionStatus.DRAFT,
            submitted_by=command.submitted_by,
            links=command.links,
            related_token_ids=command.related_token_ids,
            related_component_ids=command.related_component_ids,
        )
        self._repository.add(contribution)
        return contribution

    def get_by_id(self, contribution_id: str) -> Contribution | None:
        return self._repository.get_by_id(contribution_id)

    def list_contributions(self) -> Sequence[Contribution]:
        return self._repository.list_all()
