from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from traceboard.domain.quality_gate import GateEvaluationResult, QualityGate


class QualityGateRepository(ABC):
    """Repository for quality gates and evaluation results."""

    @abstractmethod
    def add(self, gate: QualityGate) -> None:
        """Add or update a quality gate."""

    @abstractmethod
    def get(self, gate_id: str) -> QualityGate | None:
        """Get a quality gate by ID."""

    @abstractmethod
    def get_all(self) -> tuple[QualityGate, ...]:
        """Get all quality gates."""

    @abstractmethod
    def save_evaluation_result(self, result: GateEvaluationResult) -> None:
        """Persist a gate evaluation result."""

    @abstractmethod
    def get_evaluation_result(self, gate_id: str, context_id: str) -> GateEvaluationResult | None:
        """Get an evaluation result for a gate and context."""
