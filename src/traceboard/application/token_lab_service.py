from dataclasses import dataclass, field
from typing import Dict

from traceboard.domain.design_token import DesignToken
from traceboard.domain.token_lab import TokenLab
from traceboard.domain.token_value import TokenCategory, TokenValue

from traceboard.application.ports.token_lab_repository import TokenLabRepository
from collections.abc import Sequence


def _empty_str_dict() -> Dict[str, str]:
    return {}


@dataclass(frozen=True)
class CreateTokenLabCommand:
    """Input boundary for creating a TokenLab."""

    name: str
    description: str | None = None


@dataclass(frozen=True)
class AddTokenCommand:
    """Input boundary for adding a DesignToken to a TokenLab."""

    lab_id: str
    token_name: str
    token_category: TokenCategory
    token_raw: str
    token_description: str | None = None
    token_aliases: tuple[str, ...] = field(default_factory=tuple)
    token_metadata: Dict[str, str] = field(default_factory=_empty_str_dict)


class TokenLabService:
    """Application service for token lab and token management."""

    def __init__(self, repository: TokenLabRepository) -> None:
        self._repository = repository

    def create_lab(self, command: CreateTokenLabCommand) -> TokenLab:
        lab = TokenLab(
            id=f"lab-{len(self._repository.list_all()) + 1:03d}",
            name=command.name,
            description=command.description,
        )
        self._repository.add(lab)
        return lab

    def add_token(self, command: AddTokenCommand) -> DesignToken:
        lab = self._repository.get_by_id(command.lab_id)
        if lab is None:
            raise ValueError(f"TokenLab '{command.lab_id}' not found")

        token = DesignToken(
            name=command.token_name,
            value=TokenValue(
                category=command.token_category,
                raw=command.token_raw,
                description=command.token_description,
            ),
            aliases=command.token_aliases,
            metadata=command.token_metadata,
        )

        updated_lab = lab.add_token(token)
        self._repository.add(updated_lab)
        return token

    def get_lab(self, lab_id: str) -> TokenLab | None:
        return self._repository.get_by_id(lab_id)

    def list_labs(self) -> Sequence[TokenLab]:
        return self._repository.list_all()
