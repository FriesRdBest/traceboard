from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal


class TokenTier(StrEnum):
    PRIMITIVE = "primitive"
    SEMANTIC = "semantic"
    COMPONENT = "component"


class TokenCategory(StrEnum):
    COLOR = "color"
    TYPOGRAPHY = "typography"
    SPACING = "spacing"
    RADIUS = "radius"
    SHADOW = "shadow"
    MOTION = "motion"
    BORDER = "border"
    OTHER = "other"


class ContrastRequirement(StrEnum):
    """
    WCAG contrast constraints for text / UI tokens.

    AA_NORMAL: ≥ 4.5:1 (normal text)
    AA_LARGE: ≥ 3:1 (large text)
    AA_UI: ≥ 3:1 (UI components / non-text contrast)
    AAA_NORMAL: ≥ 7:1
    """

    AA_NORMAL = "aa_normal"
    AA_LARGE = "aa_large"
    AA_UI = "aa_ui"
    AAA_NORMAL = "aaa_normal"


@dataclass(frozen=True)
class ColorValue:
    """
    Strict color primitive wrapper.

    Values are stored as hex strings (e.g. '#0A2528', '#F9FBF9').
    Validation of hex format should be done at ingestion (e.g., in a factory).
    """

    hex: str


def _is_empty_string(value: str | ColorValue | None) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return False


@dataclass
class TokenPrimitive:
    """
    Tier 1: Primitive token.

    Examples:
      - color.teal.950 = #0A2528
      - color.ivory.50 = #F9FBF9
      - spacing.4 = 1rem
    """

    name: str  # e.g. "color.teal.950"
    category: TokenCategory
    tier: Literal[TokenTier.PRIMITIVE] = field(default=TokenTier.PRIMITIVE, init=False)
    value: str | ColorValue
    description: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        if _is_empty_string(self.value):
            raise ValueError("value cannot be empty")


@dataclass
class TokenSemantic:
    """
    Tier 2: Semantic token.

    Maps primitives to roles:
      - surface.base.light = #F9FBF9
      - surface.base.dark = #0A2528
      - text.primary, text.secondary, etc.
    """

    name: str  # e.g. "surface.base"
    category: TokenCategory
    tier: Literal[TokenTier.SEMANTIC] = field(default=TokenTier.SEMANTIC, init=False)
    light_value: str | ColorValue
    dark_value: str | ColorValue
    contrast_requirement: ContrastRequirement = ContrastRequirement.AA_NORMAL
    description: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    primitive_refs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        if _is_empty_string(self.light_value):
            raise ValueError("light_value cannot be empty")
        if _is_empty_string(self.dark_value):
            raise ValueError("dark_value cannot be empty")


@dataclass
class TokenComponent:
    """
    Tier 3: Component-level token.

    Binds semantic tokens to specific component roles:
      - card.background = semantic.surface.raised
      - button.primary.background = semantic.color.brand.primary
    """

    name: str  # e.g. "card.background"
    category: TokenCategory
    tier: Literal[TokenTier.COMPONENT] = field(default=TokenTier.COMPONENT, init=False)
    semantic_ref: str
    platforms: tuple[Literal["web", "ios", "android", "desktop"], ...] = field(
        default_factory=lambda: ("web", "ios", "android", "desktop")
    )
    description: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    divergence_notes: str | None = None
    """
    Optional notes describing intentional divergence across platforms.
    """

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        if not self.semantic_ref.strip():
            raise ValueError("semantic_ref cannot be empty")
        if len(self.platforms) == 0:
            raise ValueError("platforms must contain at least one platform")
