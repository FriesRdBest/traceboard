from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class GateResultStatus(StrEnum):
    """Status of a quality gate evaluation."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass(frozen=True)
class QualityGateResult:
    """Result of evaluating a quality gate in a context."""

    gate_id: str
    context_id: str
    status: GateResultStatus
    score: float
    details: str | None = None


@dataclass(frozen=True)
class QualityGateRule:
    """A single rule within a quality gate."""

    id: str
    name: str
    threshold: float | None = None
    description: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class QualityGate:
    """A quality gate definition."""

    id: str
    name: str
    threshold: float | None = None
    description: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class GateEvaluationResult:
    """Result of evaluating a quality gate in a context."""

    gate_id: str
    context_id: str
    passed: bool
    score: float
    details: str | None = None
