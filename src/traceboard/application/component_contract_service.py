from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from ..domain.component_contract import ComponentContract, ContractRequirement, RequirementSeverity
from ..domain.divergence_evaluator import PlatformState

if TYPE_CHECKING:
    from ..domain.platform_divergence import DivergenceReport
    from .ports.component_contract_repository import ComponentContractRepository


@dataclass(frozen=True)
class CreateComponentContractCommand:
    id: str
    component_name: str
    version: str = "1.0.0"
    description: str | None = None


@dataclass(frozen=True)
class AddRequirementCommand:
    contract_id: str
    requirement_id: str
    description: str
    token_names: tuple[str, ...] = ()
    severity: RequirementSeverity = RequirementSeverity.MUST
    notes: str | None = None


@dataclass(frozen=True)
class EvaluatePlatformCommand:
    contract_id: str
    platform_name: str
    token_names: tuple[str, ...]
    token_values: dict[str, Any]
    behaviors: dict[str, Any]


class ComponentContractService:
    """Application service for component contract and divergence workflows."""

    def __init__(self, repository: ComponentContractRepository) -> None:
        self.repository = repository

    def create_contract(self, command: CreateComponentContractCommand) -> ComponentContract:
        contract = ComponentContract(
            id=command.id,
            component_name=command.component_name,
            version=command.version,
            description=command.description,
        )
        self.repository.add(contract)
        return contract

    def add_requirement(self, command: AddRequirementCommand) -> ComponentContract:
        contract = self.repository.get(command.contract_id)
        if contract is None:
            raise ValueError(f"Contract '{command.contract_id}' not found")

        requirement = ContractRequirement(
            id=command.requirement_id,
            description=command.description,
            token_names=command.token_names,
            severity=command.severity,
            notes=command.notes,
        )

        updated = contract.add_requirement(requirement)
        self.repository.add(updated)
        return updated

    def evaluate_platform(self, command: EvaluatePlatformCommand) -> DivergenceReport:
        contract = self.repository.get(command.contract_id)
        if contract is None:
            raise ValueError(f"Contract '{command.contract_id}' not found")

        platform_state = PlatformState(
            component_name=contract.component_name,
            platform_name=command.platform_name,
            token_names=command.token_names,
            token_values=command.token_values,
            behaviors=command.behaviors,
        )

        from ..domain.divergence_evaluator import DivergenceEvaluator

        evaluator = DivergenceEvaluator(contract)
        report = evaluator.evaluate(platform_state)

        self.repository.save_divergence_report(report)
        return report

    def get_contract(self, contract_id: str) -> ComponentContract | None:
        return self.repository.get(contract_id)

    def get_divergence_report(
        self, contract_id: str, platform_name: str
    ) -> DivergenceReport | None:
        return self.repository.get_divergence_report(contract_id, platform_name)
