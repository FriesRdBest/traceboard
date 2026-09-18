from __future__ import annotations

import pytest

from traceboard.application.component_contract_service import (
    AddRequirementCommand,
    ComponentContractService,
    CreateComponentContractCommand,
    EvaluatePlatformCommand,
)
from traceboard.application.ports.component_contract_repository import (
    ComponentContractRepository,
)
from traceboard.domain.component_contract import RequirementSeverity
from traceboard.domain.platform_divergence import DivergenceSeverity, DivergenceType
from traceboard.infrastructure.repositories.in_memory_component_contract_repository import (
    InMemoryComponentContractRepository,
)


@pytest.fixture
def repository() -> ComponentContractRepository:
    return InMemoryComponentContractRepository()


@pytest.fixture
def service(repository: ComponentContractRepository) -> ComponentContractService:
    return ComponentContractService(repository)


def test_create_contract(service: ComponentContractService) -> None:
    command = CreateComponentContractCommand(
        id="button-1",
        component_name="Button",
        version="1.0.0",
        description="Primary button contract",
    )

    contract = service.create_contract(command)

    assert contract.id == "button-1"
    assert contract.component_name == "Button"
    assert contract.version == "1.0.0"
    assert contract.description == "Primary button contract"

    fetched = service.get_contract("button-1")
    assert fetched is not None
    assert fetched.id == "button-1"


def test_add_requirement(service: ComponentContractService) -> None:
    create_command = CreateComponentContractCommand(
        id="button-1",
        component_name="Button",
    )
    service.create_contract(create_command)

    add_command = AddRequirementCommand(
        contract_id="button-1",
        requirement_id="req-1",
        description="Must use primary color token",
        token_names=("--color-primary",),
        severity=RequirementSeverity.MUST,
    )

    updated = service.add_requirement(add_command)

    assert len(updated.requirements) == 1
    assert updated.requirements[0].id == "req-1"
    assert updated.requirements[0].token_names == ("--color-primary",)

    fetched = service.get_contract("button-1")
    assert fetched is not None
    assert len(fetched.requirements) == 1


def test_add_requirement_contract_not_found(service: ComponentContractService) -> None:
    add_command = AddRequirementCommand(
        contract_id="nonexistent",
        requirement_id="req-1",
        description="Requirement",
    )

    with pytest.raises(ValueError, match="Contract 'nonexistent' not found"):
        service.add_requirement(add_command)


def test_evaluate_platform(service: ComponentContractService) -> None:
    # Create contract
    create_command = CreateComponentContractCommand(
        id="button-1",
        component_name="Button",
    )
    service.create_contract(create_command)

    # Add requirement with MUST severity
    add_command = AddRequirementCommand(
        contract_id="button-1",
        requirement_id="req-1",
        description="Must use primary color",
        token_names=("--color-primary", "--color-text"),
        severity=RequirementSeverity.MUST,
    )
    service.add_requirement(add_command)

    # Evaluate platform missing --color-text
    eval_command = EvaluatePlatformCommand(
        contract_id="button-1",
        platform_name="web",
        token_names=("--color-primary",),
        token_values={"--color-primary": "#0066cc"},
        behaviors={},
    )

    report = service.evaluate_platform(eval_command)

    assert report.has_divergences
    # Missing a MUST requirement results in BLOCKER severity
    assert report.blocker_count == 1

    divergence = report.divergences[0]
    assert divergence.divergence_type == DivergenceType.MISSING_TOKEN
    assert divergence.severity == DivergenceSeverity.BLOCKER
    assert divergence.details["token_name"] == "--color-text"

    # Report is persisted
    fetched_report = service.get_divergence_report("button-1", "web")
    assert fetched_report is not None
    assert fetched_report.blocker_count == 1
