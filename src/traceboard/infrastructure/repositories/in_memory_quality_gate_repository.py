from __future__ import annotations

from ...application.ports.quality_gate_repository import QualityGateRepository
from ...domain.quality_gate import GateEvaluationResult, QualityGate


class InMemoryQualityGateRepository(QualityGateRepository):
    """In-memory adapter for QualityGateRepository."""

    def __init__(self) -> None:
        self._gates: dict[str, QualityGate] = {}
        self._evaluation_results: dict[str, GateEvaluationResult] = {}

    def add(self, gate: QualityGate) -> None:
        self._gates[gate.id] = gate

    def get(self, gate_id: str) -> QualityGate | None:
        return self._gates.get(gate_id)

    def get_all(self) -> tuple[QualityGate, ...]:
        return tuple(self._gates.values())

    def save_evaluation_result(self, result: GateEvaluationResult) -> None:
        self._evaluation_results[result.gate_id] = result

    def get_evaluation_result(self, gate_id: str) -> GateEvaluationResult | None:
        return self._evaluation_results.get(gate_id)
