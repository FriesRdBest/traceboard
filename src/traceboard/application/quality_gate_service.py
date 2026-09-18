from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from traceboard.domain.policy_engine import PolicyContext, PolicyEngine
from traceboard.domain.quality_gate import (
    GateEvaluationResult,
    QualityGate,
    QualityGateRule,
    RuleType,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from traceboard.application.ports.quality_gate_repository import QualityGateRepository
    from traceboard.domain.component_contract import ComponentContract
    from traceboard.domain.divergence_evaluator import PlatformState
    from traceboard.domain.platform_divergence import DivergenceReport
    from traceboard.domain.token_value import TokenValue


@dataclass(frozen=True)
class CreateQualityGateCommand:
    id: str
    name: str
    description: str | None = None


@dataclass(frozen=True)
class AddRuleCommand:
    gate_id: str
    rule_id: str
    rule_type: RuleType
    description: str
    threshold: float | None = None
    component_contract_id: str | None = None
    platform_name: str | None = None


@dataclass(frozen=True)
class EvaluateGateCommand:
    gate_id: str
    component_contract: ComponentContract | None = None
    divergence_report: DivergenceReport | None = None
    platform_state: PlatformState | None = None
    foreground: TokenValue | None = None
    background: TokenValue | None = None


class QualityGateService:
    """Application service for quality gate and policy evaluation."""

    def __init__(self, repository: QualityGateRepository) -> None:
        self.repository = repository
        self.engine = PolicyEngine()

    def create_gate(self, command: CreateQualityGateCommand) -> QualityGate:
        gate = QualityGate(
            id=command.id,
            name=command.name,
            description=command.description,
        )
        self.repository.add(gate)
        return gate

    def add_rule(self, command: AddRuleCommand) -> QualityGate:
        gate = self.repository.get(command.gate_id)
        if gate is None:
            raise ValueError(f"QualityGate '{command.gate_id}' not found")

        rule = QualityGateRule(
            id=command.rule_id,
            rule_type=command.rule_type,
            description=command.description,
            threshold=command.threshold,
        )

        updated = gate.add_rule(rule)
        self.repository.add(updated)
        return updated

    def evaluate_gate(self, command: EvaluateGateCommand) -> GateEvaluationResult:
        gate = self.repository.get(command.gate_id)
        if gate is None:
            raise ValueError(f"QualityGate '{command.gate_id}' not found")

        context = PolicyContext(
            component_contract=command.component_contract,
            divergence_report=command.divergence_report,
            platform_state=command.platform_state,
            foreground=command.foreground,
            background=command.background,
        )

        result = self.engine.evaluate(gate, context)
        self.repository.save_evaluation_result(result)
        return result

    def get_gate(self, gate_id: str) -> QualityGate | None:
        return self.repository.get(gate_id)

    def list_gates(self) -> Sequence[QualityGate]:
        return self.repository.get_all()

    def get_evaluation_result(
        self, gate_id: str, context_id: str = "default"
    ) -> GateEvaluationResult | None:
        return self.repository.get_evaluation_result(gate_id, context_id)
