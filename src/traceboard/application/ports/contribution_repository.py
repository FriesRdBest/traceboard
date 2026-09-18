from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.domain.contribution import Contribution


class ContributionRepository(Protocol):
    """Persistence boundary for Contribution aggregates."""

    def add(self, contribution: Contribution) -> None:
        """Store a new contribution.

        Raises:
            ValueError: If a contribution with the same identifier already exists.
        """
        ...

    def get_by_id(self, contribution_id: str) -> Contribution | None:
        """Return a contribution by identifier, or None when it does not exist."""
        ...

    def list_all(self) -> Sequence[Contribution]:
        """Return all contributions in repository-defined order."""
        ...
