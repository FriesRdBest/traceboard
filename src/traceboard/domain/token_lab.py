from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from traceboard.domain.design_token import DesignToken


@dataclass(frozen=True)
class TokenLab:
    """Aggregate root for a token laboratory session."""

    id: str
    name: str
    tokens: tuple[DesignToken, ...] = field(default_factory=tuple)
    description: str | None = None

    def add_token(self, token: DesignToken) -> TokenLab:
        if any(t.name == token.name for t in self.tokens):
            raise ValueError(f"Token '{token.name}' already exists in lab '{self.id}'")

        return TokenLab(
            id=self.id,
            name=self.name,
            tokens=(*self.tokens, token),
            description=self.description,
        )

    def get_token(self, name: str) -> DesignToken | None:
        for token in self.tokens:
            if token.name == name:
                return token
        return None
