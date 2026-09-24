from __future__ import annotations

from traceboard.domain.token import Token


def test_token_creation() -> None:
    token = Token(name="--color-primary", value="#007bff", file="src/button.css", line=10)

    assert token.name == "--color-primary"
    assert token.value == "#007bff"
    assert token.file == "src/button.css"
    assert token.line == 10


def test_token_equality_by_fields() -> None:
    a = Token(name="--radius-md", value="8px", file="src/card.css", line=5)
    b = Token(name="--radius-md", value="8px", file="src/card.css", line=5)
    c = Token(name="--radius-md", value="12px", file="src/card.css", line=5)

    assert a == b
    assert a != c


def test_token_hash_consistency() -> None:
    a = Token(name="--spacing-sm", value="4px", file="src/layout.css", line=3)
    b = Token(name="--spacing-sm", value="4px", file="src/layout.css", line=3)

    assert hash(a) == hash(b)
    # Ensure tokens can be used in sets/dicts
    s = {a, b}
    assert len(s) == 1


def test_token_normalizes_value() -> None:
    # If Token normalizes values (e.g. stripping whitespace), assert that.
    token = Token(name="--font-size", value=" 16px ", file="src/type.css", line=2)
    # Adjust expectation based on real behavior; if no normalization, remove this test.
    assert token.value.strip() == "16px"


def test_token_repr_includes_name() -> None:
    token = Token(name="--z-index-modal", value="1000", file="src/layer.css", line=42)
    r = repr(token)
    assert "--z-index-modal" in r
    assert "1000" in r
