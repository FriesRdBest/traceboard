from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from traceboard.application.component_contract_service import (
    AddRequirementCommand,
    ComponentContractService,
    CreateComponentContractCommand,
    EvaluatePlatformCommand,
)
from traceboard.domain.component_contract import RequirementSeverity
from traceboard.domain.platform_divergence import DivergenceSeverity, DivergenceType
from traceboard.infrastructure.repositories.in_memory_component_contract_repository import (
    InMemoryComponentContractRepository,
)

if TYPE_CHECKING:
    from traceboard.application.ports.component_contract_repository import (
        ComponentContractRepository,
    )


def build_repository() -> ComponentContractRepository:
    return InMemoryComponentContractRepository()


def build_service() -> ComponentContractService:
    return ComponentContractService(build_repository())


def test_create_contract() -> None:
    service = build_service()

    command = CreateComponentContractCommand(
        id="contract-1",
        component_name="Button",
        version="1.0.0",
        description="Primary button contract",
    )

    contract = service.create_contract(command)

    assert contract.id == "contract-1"
    assert contract.component_name == "Button"
    assert contract.version == "1.0.0"
    assert contract.description == "Primary button contract"

    fetched = service.get_contract("contract-1")
    assert fetched is not None
    assert fetched.id == "contract-1"


def test_add_requirement() -> None:
    service = build_service()

    service.create_contract(
        CreateComponentContractCommand(id="contract-1", component_name="Button")
    )

    command = AddRequirementCommand(
        contract_id="contract-1",
        requirement_id="req-1",
        description="Must use primary color token",
        token_names=("--color-primary",),
        severity=RequirementSeverity.MUST,
    )

    updated = service.add_requirement(command)

    assert len(updated.requirements) == 1
    assert updated.requirements[0].id == "req-1"
    assert updated.requirements[0].token_names == ("--color-primary",)

    fetched = service.get_contract("contract-1")
    assert fetched is not None
    assert len(fetched.requirements) == 1


def test_add_requirement_contract_not_found() -> None:
    service = build_service()

    command = AddRequirementCommand(
        contract_id="nonexistent",
        requirement_id="req-1",
        description="Requirement",
    )

    with pytest.raises(ValueError, match="Contract 'nonexistent' not found"):
        service.add_requirement(command)


def test_evaluate_platform() -> None:
    service = build_service()

    service.create_contract(
        CreateComponentContractCommand(id="contract-1", component_name="Button")
    )

    service.add_requirement(
        AddRequirementCommand(
            contract_id="contract-1",
            requirement_id="req-1",
            description="Must use primary color",
            token_names=("--color-primary", "--color-text"),
            severity=RequirementSeverity.MUST,
        )
    )

    command = EvaluatePlatformCommand(
        contract_id="contract-1",
        platform_name="web",
        token_names=("--color-primary",),
        token_values={"--color-primary": "#0066cc"},
        behaviors={},
    )

    report = service.evaluate_platform(command)

    assert report.has_divergences
    assert report.blocker_count == 1

    divergence = report.divergences[0]
    assert divergence.divergence_type == DivergenceType.MISSING_TOKEN
    assert divergence.severity == DivergenceSeverity.BLOCKER
    assert divergence.details["token_name"] == "--color-text"

    fetched_report = service.get_divergence_report("contract-1", "web")
    assert fetched_report is not None
    assert fetched_report.blocker_count == 1
