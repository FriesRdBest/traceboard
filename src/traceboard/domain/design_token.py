from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from traceboard.domain.token_value import TokenValue


def _empty_str_dict() -> dict[str, str]:
    return {}


@dataclass(frozen=True)
class DesignToken:
    """Design token with semantic identity and value."""

    name: str
    value: TokenValue
    aliases: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=_empty_str_dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Token name must be non-empty")
        if not self.value.raw:
            raise ValueError("Token value raw must be non-empty")
