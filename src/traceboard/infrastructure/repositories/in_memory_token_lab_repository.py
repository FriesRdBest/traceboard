from __future__ import annotations

from typing import TYPE_CHECKING

from traceboard.application.ports.token_lab_repository import TokenLabRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.domain.token_lab import TokenLab


class InMemoryTokenLabRepository(TokenLabRepository):
    """In-memory TokenLab repository for local sessions and tests."""

    def __init__(self) -> None:
        self._labs_by_id: dict[str, TokenLab] = {}
        self._ordered_ids: list[str] = []

    def add(self, lab: TokenLab) -> None:
        if lab.id not in self._labs_by_id:
            self._ordered_ids.append(lab.id)
        self._labs_by_id[lab.id] = lab

    def get_by_id(self, lab_id: str) -> TokenLab | None:
        return self._labs_by_id.get(lab_id)

    def list_all(self) -> Sequence[TokenLab]:
        return tuple(self._labs_by_id[lab_id] for lab_id in self._ordered_ids)
