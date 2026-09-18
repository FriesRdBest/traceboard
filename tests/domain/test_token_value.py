from __future__ import annotations

from traceboard.domain.token_value import TokenCategory, TokenValue


def test_token_value_creation_with_all_fields() -> None:
    value = TokenValue(
        category=TokenCategory.COLOR,
        raw="#1a1a1a",
        description="Primary text color",
    )

    assert value.category is TokenCategory.COLOR
    assert value.raw == "#1a1a1a"
    assert value.description == "Primary text color"


def test_token_value_creation_without_description() -> None:
    value = TokenValue(
        category=TokenCategory.SPACING,
        raw="8px",
    )

    assert value.category is TokenCategory.SPACING
    assert value.raw == "8px"
    assert value.description is None
