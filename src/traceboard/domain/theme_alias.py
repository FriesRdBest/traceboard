from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ThemeAlias:
    """Mapping from semantic alias to concrete token value."""

    alias: str
    token_name: str
    theme: str = "default"

    def __post_init__(self) -> None:
        if not self.alias:
            raise ValueError("Alias must be non-empty")
        if not self.token_name:
            raise ValueError("Token name must be non-empty")


@dataclass(frozen=True)
class ThemeAliasSet:
    """Collection of theme aliases for a given theme."""

    theme: str
    aliases: tuple[ThemeAlias, ...] = field(default_factory=tuple)

    def add(self, alias: ThemeAlias) -> ThemeAliasSet:
        if alias.theme != self.theme:
            raise ValueError(f"Alias theme '{alias.theme}' does not match set theme '{self.theme}'")
        if any(a.alias == alias.alias for a in self.aliases):
            raise ValueError(f"Alias '{alias.alias}' already exists in theme '{self.theme}'")

        return ThemeAliasSet(
            theme=self.theme,
            aliases=(*self.aliases, alias),
        )

    def resolve(self, alias: str) -> str | None:
        for a in self.aliases:
            if a.alias == alias:
                return a.token_name
        return None
