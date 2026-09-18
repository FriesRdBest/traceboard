from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenCategory(Enum):
    COLOR = auto()
    SPACING = auto()
    TYPOGRAPHY = auto()
    RADIUS = auto()
    SHADOW = auto()
    OPACITY = auto()


@dataclass(frozen=True)
class TokenValue:
    """Atomic design token value with category and raw representation."""

    category: TokenCategory
    raw: str
    description: str | None = None
