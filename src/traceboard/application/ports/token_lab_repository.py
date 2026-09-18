from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.domain.token_lab import TokenLab


class TokenLabRepository(Protocol):
    """Persistence boundary for TokenLab aggregates."""

    def add(self, lab: TokenLab) -> None:
        """Store a new token lab.

        Raises:
            ValueError: If a lab with the same identifier already exists.
        """
        ...

    def get_by_id(self, lab_id: str) -> TokenLab | None:
        """Return a token lab by identifier, or None when it does not exist."""
        ...

    def list_all(self) -> Sequence[TokenLab]:
        """Return all token labs in repository-defined order."""
        ...
