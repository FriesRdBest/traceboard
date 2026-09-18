from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class GateResultStatus(Enum):
    PASS = auto()
    FAIL = auto()
    SKIP = auto()


class RuleType(Enum):
    NO_BLOCKER_DIVERGENCES = auto()
    NO_MAJOR_DIVERGENCES = auto()
    MIN_CONTRAST_RATIO = auto()
    CUSTOM = auto()


@dataclass(frozen=True)
class QualityGateRule:
    """Individual rule within a quality gate."""

    id: str
    rule_type: RuleType
    description: str
    threshold: float | None = None  # e.g., min contrast ratio
    component_contract_id: str | None = None
    platform_name: str | None = None


@dataclass(frozen=True)
class QualityGateResult:
    """Outcome of evaluating a single rule."""

    rule_id: str
    status: GateResultStatus
    message: str
    actual_value: float | int | str | None = None
    expected_value: float | int | str | None = None


@dataclass(frozen=True)
class QualityGate:
    """Quality gate defining pass/fail criteria."""

    id: str
    name: str
    rules: tuple[QualityGateRule, ...] = field(default_factory=tuple)
    description: str | None = None

    def add_rule(self, rule: QualityGateRule) -> QualityGate:
        if any(r.id == rule.id for r in self.rules):
            raise ValueError(f"Rule '{rule.id}' already exists in gate '{self.id}'")

        return QualityGate(
            id=self.id,
            name=self.name,
            rules=self.rules + (rule,),
            description=self.description,
        )

    def get_rule(self, rule_id: str) -> QualityGateRule | None:
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None


@dataclass(frozen=True)
class GateEvaluationResult:
    """Aggregate result of evaluating all rules in a gate."""

    gate_id: str
    gate_name: str
    rule_results: tuple[QualityGateResult, ...]
    overall_status: GateResultStatus

    @property
    def passed(self) -> bool:
        return self.overall_status == GateResultStatus.PASS

    @property
    def failed_rule_count(self) -> int:
        return sum(1 for r in self.rule_results if r.status == GateResultStatus.FAIL)

    def summary(self) -> dict[str, str | int | bool]:
        return {
            "gate_id": self.gate_id,
            "gate_name": self.gate_name,
            "passed": self.passed,
            "total_rules": len(self.rule_results),
            "failed_rules": self.failed_rule_count,
        }
