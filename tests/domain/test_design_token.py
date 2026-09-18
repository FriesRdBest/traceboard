from __future__ import annotations

import pytest

from traceboard.domain.design_token import DesignToken
from traceboard.domain.token_value import TokenCategory, TokenValue


def build_token_value() -> TokenValue:
    return TokenValue(category=TokenCategory.COLOR, raw="#ffffff")


def test_design_token_creation_with_minimal_fields() -> None:
    token = DesignToken(name="surface-primary", value=build_token_value())

    assert token.name == "surface-primary"
    assert token.value.raw == "#ffffff"
    assert token.aliases == ()
    assert token.metadata == {}


def test_design_token_creation_with_aliases_and_metadata() -> None:
    token = DesignToken(
        name="surface-primary",
        value=build_token_value(),
        aliases=("--surface-bg",),
        metadata={"section": "surfaces"},
    )

    assert token.aliases == ("--surface-bg",)
    assert token.metadata == {"section": "surfaces"}


def test_design_token_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name must be non-empty"):
        DesignToken(name="", value=build_token_value())


def test_design_token_rejects_empty_raw_value() -> None:
    with pytest.raises(ValueError, match="raw must be non-empty"):
        DesignToken(name="test", value=TokenValue(category=TokenCategory.COLOR, raw=""))
