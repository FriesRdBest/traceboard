from __future__ import annotations

import pytest

from traceboard.application.token_lab_service import (
    AddTokenCommand,
    CreateTokenLabCommand,
    TokenLabService,
)
from traceboard.domain.design_token import DesignToken
from traceboard.domain.token_value import TokenCategory, TokenValue
from traceboard.infrastructure.repositories.in_memory_token_lab_repository import (
    InMemoryTokenLabRepository,
)


def build_service() -> TokenLabService:
    return TokenLabService(InMemoryTokenLabRepository())


def test_create_lab_stores_lab_with_id() -> None:
    service = build_service()
    command = CreateTokenLabCommand(
        id="lab-1",
        name="Brand Tokens",
        description="Primary brand token lab",
    )

    lab = service.create_lab(command)

    assert lab.id == "lab-1"
    assert lab.name == "Brand Tokens"
    assert lab.description == "Primary brand token lab"
    assert service.get_lab(lab.id) == lab


def test_add_token_appends_token_to_lab() -> None:
    service = build_service()
    lab = service.create_lab(CreateTokenLabCommand(id="lab-1", name="Test Lab"))

    token_value = TokenValue(
        category=TokenCategory.COLOR,
        raw="#ffffff",
        description="White surface",
    )
    token = DesignToken(
        name="surface-primary",
        value=token_value,
    )

    updated_lab = service.add_token(
        AddTokenCommand(
            lab_id=lab.id,
            token_name="surface-primary",
            token_value=token,
        )
    )

    assert updated_lab.id == lab.id
    assert updated_lab.name == "Test Lab"

    fetched_token = updated_lab.get_token("surface-primary")
    assert fetched_token is not None
    assert fetched_token.name == "surface-primary"


def test_add_token_raises_when_lab_not_found() -> None:
    service = build_service()

    token_value = TokenValue(
        category=TokenCategory.COLOR,
        raw="#ffffff",
    )
    token = DesignToken(
        name="surface-primary",
        value=token_value,
    )

    with pytest.raises(ValueError, match="not found"):
        service.add_token(
            AddTokenCommand(
                lab_id="missing-lab",
                token_name="surface-primary",
                token_value=token,
            )
        )


def test_list_labs_returns_created_labs_in_order() -> None:
    service = build_service()
    first = service.create_lab(CreateTokenLabCommand(id="lab-1", name="First Lab"))
    second = service.create_lab(CreateTokenLabCommand(id="lab-2", name="Second Lab"))

    assert service.list_labs() == (first, second)
