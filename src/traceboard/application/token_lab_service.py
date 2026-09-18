from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from traceboard.domain.token_lab import TokenLab

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.application.ports.token_lab_repository import TokenLabRepository
    from traceboard.domain.design_token import DesignToken


@dataclass(frozen=True)
class CreateTokenLabCommand:
    id: str
    name: str
    description: str | None = None


@dataclass(frozen=True)
class AddTokenCommand:
    lab_id: str
    token_name: str
    token_value: DesignToken


class TokenLabService:
    """Application service for Token Lab operations."""

    def __init__(self, repository: TokenLabRepository) -> None:
        self.repository = repository

    def create_lab(self, command: CreateTokenLabCommand) -> TokenLab:
        lab = TokenLab(
            id=command.id,
            name=command.name,
            description=command.description,
        )
        self.repository.add(lab)
        return lab

    def add_token(self, command: AddTokenCommand) -> TokenLab:
        lab = self.repository.get_by_id(command.lab_id)
        if lab is None:
            raise ValueError(f"TokenLab '{command.lab_id}' not found")

        updated = lab.add_token(command.token_value)
        self.repository.add(updated)
        return updated

    def get_lab(self, lab_id: str) -> TokenLab | None:
        return self.repository.get_by_id(lab_id)

    def list_labs(self) -> Sequence[TokenLab]:
        return self.repository.list_all()
