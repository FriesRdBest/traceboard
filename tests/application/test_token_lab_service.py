from __future__ import annotations

import pytest

from traceboard.application.token_lab_service import (
    AddTokenCommand,
    CreateTokenLabCommand,
    TokenLabService,
)
from traceboard.domain.token_value import TokenCategory
from traceboard.infrastructure.repositories.in_memory_token_lab_repository import (
    InMemoryTokenLabRepository,
)


def build_service() -> TokenLabService:
    return TokenLabService(InMemoryTokenLabRepository())


def test_create_lab_stores_lab_with_generated_id() -> None:
    service = build_service()
    command = CreateTokenLabCommand(name="Brand Tokens", description="Primary brand token lab")

    lab = service.create_lab(command)

    assert lab.name == "Brand Tokens"
    assert lab.description == "Primary brand token lab"
    assert service.get_lab(lab.id) == lab


def test_add_token_appends_token_to_lab() -> None:
    service = build_service()
    lab = service.create_lab(CreateTokenLabCommand(name="Test Lab"))

    token = service.add_token(
        AddTokenCommand(
            lab_id=lab.id,
            token_name="surface-primary",
            token_category=TokenCategory.COLOR,
            token_raw="#ffffff",
        )
    )

    assert token.name == "surface-primary"
    updated_lab = service.get_lab(lab.id)
    assert updated_lab is not None
    assert updated_lab.get_token("surface-primary") == token


def test_add_token_raises_when_lab_not_found() -> None:
    service = build_service()

    with pytest.raises(ValueError, match="not found"):
        service.add_token(
            AddTokenCommand(
                lab_id="missing-lab",
                token_name="surface-primary",
                token_category=TokenCategory.COLOR,
                token_raw="#ffffff",
            )
        )


def test_list_labs_returns_created_labs_in_order() -> None:
    service = build_service()
    first = service.create_lab(CreateTokenLabCommand(name="First Lab"))
    second = service.create_lab(CreateTokenLabCommand(name="Second Lab"))

    assert service.list_labs() == (first, second)
