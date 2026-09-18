from __future__ import annotations

from abc import ABC, abstractmethod

from ...domain.quality_gate import GateEvaluationResult, QualityGate


class QualityGateRepository(ABC):
    """Repository port for QualityGate aggregates and results."""

    @abstractmethod
    def add(self, gate: QualityGate) -> None:
        """Add or update a quality gate."""
        pass

    @abstractmethod
    def get(self, gate_id: str) -> QualityGate | None:
        """Get a quality gate by ID."""
        pass

    @abstractmethod
    def get_all(self) -> tuple[QualityGate, ...]:
        """Get all quality gates."""
        pass

    @abstractmethod
    def save_evaluation_result(self, result: GateEvaluationResult) -> None:
        """Persist a gate evaluation result."""
        pass

    @abstractmethod
    def get_evaluation_result(self, gate_id: str) -> GateEvaluationResult | None:
        """Get the latest evaluation result for a gate."""
        pass
