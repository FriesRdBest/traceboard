from __future__ import annotations

from typing import TYPE_CHECKING

from traceboard.application.ports.contribution_repository import ContributionRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.domain.contribution import Contribution


class InMemoryContributionRepository(ContributionRepository):
    """In-memory Contribution repository for local application sessions and tests."""

    def __init__(self) -> None:
        self._contributions_by_id: dict[str, Contribution] = {}
        self._ordered_ids: list[str] = []

    def add(self, contribution: Contribution) -> None:
        if contribution.id in self._contributions_by_id:
            raise ValueError(f"Contribution with id '{contribution.id}' already exists")

        self._contributions_by_id[contribution.id] = contribution
        self._ordered_ids.append(contribution.id)

    def get_by_id(self, contribution_id: str) -> Contribution | None:
        return self._contributions_by_id.get(contribution_id)

    def list_all(self) -> Sequence[Contribution]:
        return tuple(
            self._contributions_by_id[contribution_id] for contribution_id in self._ordered_ids
        )
