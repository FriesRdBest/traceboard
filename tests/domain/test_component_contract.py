from __future__ import annotations

import pytest

from traceboard.domain.component_contract import (
    ComponentContract,
    ContractRequirement,
    RequirementSeverity,
)


def test_create_contract() -> None:
    contract = ComponentContract(
        id="button-1",
        component_name="Button",
        version="1.0.0",
        description="Primary button contract",
    )

    assert contract.id == "button-1"
    assert contract.component_name == "Button"
    assert contract.version == "1.0.0"
    assert contract.description == "Primary button contract"
    assert len(contract.requirements) == 0


def test_add_requirement() -> None:
    contract = ComponentContract(id="button-1", component_name="Button")

    requirement = ContractRequirement(
        id="req-1",
        description="Must use primary color token",
        token_names=("--color-primary",),
        severity=RequirementSeverity.MUST,
    )

    updated = contract.add_requirement(requirement)

    assert len(updated.requirements) == 1
    assert updated.requirements[0].id == "req-1"
    assert updated.requirements[0].token_names == ("--color-primary",)


def test_add_requirement_duplicate_id_raises() -> None:
    contract = ComponentContract(id="button-1", component_name="Button")

    requirement1 = ContractRequirement(
        id="req-1",
        description="First requirement",
        token_names=("--color-primary",),
    )

    requirement2 = ContractRequirement(
        id="req-1",
        description="Duplicate requirement",
        token_names=("--color-secondary",),
    )

    updated = contract.add_requirement(requirement1)

    with pytest.raises(ValueError, match="Requirement 'req-1' already exists"):
        updated.add_requirement(requirement2)


def test_get_requirement() -> None:
    contract = ComponentContract(id="button-1", component_name="Button")

    requirement = ContractRequirement(
        id="req-1",
        description="Must use primary color token",
        token_names=("--color-primary",),
    )

    updated = contract.add_requirement(requirement)

    fetched = updated.get_requirement("req-1")
    assert fetched is not None
    assert fetched.description == "Must use primary color token"

    not_found = updated.get_requirement("nonexistent")
    assert not_found is None
