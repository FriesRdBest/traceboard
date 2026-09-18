from __future__ import annotations

import pytest

from traceboard.domain.design_token import DesignToken
from traceboard.domain.token_lab import TokenLab
from traceboard.domain.token_value import TokenCategory, TokenValue


def build_token(name: str = "surface-primary") -> DesignToken:
    return DesignToken(
        name=name,
        value=TokenValue(category=TokenCategory.COLOR, raw="#ffffff"),
    )


def build_lab(lab_id: str = "lab-001") -> TokenLab:
    return TokenLab(id=lab_id, name="Test Lab")


def test_token_lab_creation_with_empty_tokens() -> None:
    lab = build_lab()

    assert lab.id == "lab-001"
    assert lab.name == "Test Lab"
    assert lab.tokens == ()


def test_token_lab_add_token_appends_to_collection() -> None:
    lab = build_lab()
    token = build_token()

    updated = lab.add_token(token)

    assert updated.tokens == (token,)
    assert updated.get_token("surface-primary") == token


def test_token_lab_add_token_rejects_duplicate_name() -> None:
    lab = build_lab()
    token = build_token()
    lab = lab.add_token(token)

    with pytest.raises(ValueError, match="already exists"):
        lab.add_token(token)


def test_token_lab_get_token_returns_none_when_not_found() -> None:
    lab = build_lab()

    assert lab.get_token("missing-token") is None
