from __future__ import annotations

import pytest

from traceboard.domain.theme_alias import ThemeAlias, ThemeAliasSet


def test_theme_alias_creation() -> None:
    alias = ThemeAlias(alias="--surface-bg", token_name="surface-primary")

    assert alias.alias == "--surface-bg"
    assert alias.token_name == "surface-primary"
    assert alias.theme == "default"


def test_theme_alias_with_explicit_theme() -> None:
    alias = ThemeAlias(
        alias="--surface-bg",
        token_name="surface-primary",
        theme="dark",
    )

    assert alias.theme == "dark"


def test_theme_alias_rejects_empty_alias() -> None:
    with pytest.raises(ValueError, match="Alias must be non-empty"):
        ThemeAlias(alias="", token_name="surface-primary")


def test_theme_alias_rejects_empty_token_name() -> None:
    with pytest.raises(ValueError, match="Token name must be non-empty"):
        ThemeAlias(alias="--surface-bg", token_name="")


def test_theme_alias_set_add_appends_alias() -> None:
    alias_set = ThemeAliasSet(theme="default")
    alias = ThemeAlias(alias="--surface-bg", token_name="surface-primary")

    updated = alias_set.add(alias)

    assert updated.aliases == (alias,)
    assert updated.resolve("--surface-bg") == "surface-primary"


def test_theme_alias_set_rejects_mismatched_theme() -> None:
    alias_set = ThemeAliasSet(theme="light")
    alias = ThemeAlias(alias="--surface-bg", token_name="surface-primary", theme="dark")

    with pytest.raises(ValueError, match="does not match"):
        alias_set.add(alias)


def test_theme_alias_set_rejects_duplicate_alias() -> None:
    alias_set = ThemeAliasSet(theme="default")
    alias = ThemeAlias(alias="--surface-bg", token_name="surface-primary")
    alias_set = alias_set.add(alias)

    with pytest.raises(ValueError, match="already exists"):
        alias_set.add(alias)


def test_theme_alias_set_resolve_returns_none_when_not_found() -> None:
    alias_set = ThemeAliasSet(theme="default")

    assert alias_set.resolve("--missing") is None
