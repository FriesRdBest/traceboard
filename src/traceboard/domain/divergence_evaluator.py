from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .component_contract import ComponentContract, ContractRequirement, RequirementSeverity
from .platform_divergence import (
    DivergenceReport,
    DivergenceSeverity,
    DivergenceType,
    PlatformDivergence,
)


@dataclass(frozen=True)
class PlatformState:
    """Snapshot of a platform's tokens and behaviors for a component."""

    component_name: str
    platform_name: str
    token_names: tuple[str, ...]
    token_values: dict[str, Any]  # token_name -> value
    behaviors: dict[str, Any]  # behavior_name -> value


class DivergenceEvaluator:
    """Pure-domain evaluator comparing platform state against a component contract."""

    def __init__(self, contract: ComponentContract) -> None:
        self.contract = contract

    def evaluate(self, platform_state: PlatformState) -> DivergenceReport:
        report = DivergenceReport(
            component_contract_id=self.contract.id,
            platform_name=platform_state.platform_name,
        )

        for requirement in self.contract.requirements:
            divergences = self._evaluate_requirement(requirement, platform_state)
            for divergence in divergences:
                report = report.add_divergence(divergence)

        # Check for unexpected tokens (not required by any requirement)
        required_tokens: set[str] = set()
        for req in self.contract.requirements:
            required_tokens.update(req.token_names)

        for token_name in platform_state.token_names:
            if token_name not in required_tokens:
                report = report.add_divergence(
                    PlatformDivergence(
                        id=f"unexpected-{token_name}",
                        component_contract_id=self.contract.id,
                        platform_name=platform_state.platform_name,
                        requirement_id=None,
                        divergence_type=DivergenceType.UNEXPECTED_TOKEN,
                        severity=DivergenceSeverity.INFO,
                        description=f"Token '{token_name}' is present but not required by contract",
                        details={"token_name": token_name},
                    )
                )

        return report

    def _evaluate_requirement(
        self, requirement: ContractRequirement, platform_state: PlatformState
    ) -> tuple[PlatformDivergence, ...]:
        divergences: list[PlatformDivergence] = []

        # Check missing tokens
        for token_name in requirement.token_names:
            if token_name not in platform_state.token_names:
                severity = self._severity_for_requirement(requirement, DivergenceType.MISSING_TOKEN)
                divergences.append(
                    PlatformDivergence(
                        id=f"missing-{token_name}",
                        component_contract_id=self.contract.id,
                        platform_name=platform_state.platform_name,
                        requirement_id=requirement.id,
                        divergence_type=DivergenceType.MISSING_TOKEN,
                        severity=severity,
                        description=f"Required token '{token_name}' is missing",
                        details={"token_name": token_name, "requirement_id": requirement.id},
                    )
                )

        # Behavior checks can be added later when requirements support behavior metadata

        return tuple(divergences)

    def _severity_for_requirement(
        self, requirement: ContractRequirement, divergence_type: DivergenceType
    ) -> DivergenceSeverity:
        if requirement.severity == RequirementSeverity.MUST:
            return DivergenceSeverity.BLOCKER
        elif requirement.severity == RequirementSeverity.SHOULD:
            return DivergenceSeverity.MAJOR
        else:
            return DivergenceSeverity.MINOR
