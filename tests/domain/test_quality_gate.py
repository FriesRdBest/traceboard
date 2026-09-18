from __future__ import annotations

import pytest

from traceboard.domain.quality_gate import (
    GateEvaluationResult,
    GateResultStatus,
    QualityGate,
    QualityGateResult,
    QualityGateRule,
    RuleType,
)


def test_create_quality_gate() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Component Quality Gate",
        description="Main quality gate for components",
    )

    assert gate.id == "gate-1"
    assert gate.name == "Component Quality Gate"
    assert gate.description == "Main quality gate for components"
    assert len(gate.rules) == 0


def test_add_rule() -> None:
    gate = QualityGate(id="gate-1", name="Test Gate")

    rule = QualityGateRule(
        id="rule-1",
        rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
        description="Must have no blocker divergences",
    )

    updated = gate.add_rule(rule)

    assert len(updated.rules) == 1
    assert updated.rules[0].id == "rule-1"
    assert updated.rules[0].rule_type == RuleType.NO_BLOCKER_DIVERGENCES


def test_add_rule_duplicate_id_raises() -> None:
    gate = QualityGate(id="gate-1", name="Test Gate")

    rule1 = QualityGateRule(
        id="rule-1",
        rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
        description="First rule",
    )

    rule2 = QualityGateRule(
        id="rule-1",
        rule_type=RuleType.NO_MAJOR_DIVERGENCES,
        description="Duplicate rule",
    )

    updated = gate.add_rule(rule1)

    with pytest.raises(ValueError, match="Rule 'rule-1' already exists"):
        updated.add_rule(rule2)


def test_gate_evaluation_result_passed() -> None:
    result = QualityGateResult(
        rule_id="rule-1",
        status=GateResultStatus.PASS,
        message="All checks passed",
    )

    eval_result = GateEvaluationResult(
        gate_id="gate-1",
        gate_name="Test Gate",
        rule_results=(result,),
        overall_status=GateResultStatus.PASS,
    )

    assert eval_result.passed is True
    assert eval_result.failed_rule_count == 0


def test_gate_evaluation_result_failed() -> None:
    result1 = QualityGateResult(
        rule_id="rule-1",
        status=GateResultStatus.PASS,
        message="Passed",
    )

    result2 = QualityGateResult(
        rule_id="rule-2",
        status=GateResultStatus.FAIL,
        message="Failed",
    )

    eval_result = GateEvaluationResult(
        gate_id="gate-1",
        gate_name="Test Gate",
        rule_results=(result1, result2),
        overall_status=GateResultStatus.FAIL,
    )

    assert eval_result.passed is False
    assert eval_result.failed_rule_count == 1


def test_gate_evaluation_result_summary() -> None:
    result = QualityGateResult(
        rule_id="rule-1",
        status=GateResultStatus.PASS,
        message="Passed",
    )

    eval_result = GateEvaluationResult(
        gate_id="gate-1",
        gate_name="Test Gate",
        rule_results=(result,),
        overall_status=GateResultStatus.PASS,
    )

    summary = eval_result.summary()

    assert summary["gate_id"] == "gate-1"
    assert summary["gate_name"] == "Test Gate"
    assert summary["passed"] is True
    assert summary["total_rules"] == 1
    assert summary["failed_rules"] == 0
