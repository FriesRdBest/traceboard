from __future__ import annotations

import pytest

from traceboard.application.quality_gate_service import (
    AddRuleCommand,
    CreateQualityGateCommand,
    EvaluateGateCommand,
    QualityGateService,
)
from traceboard.domain.platform_divergence import (
    DivergenceReport,
    DivergenceSeverity,
    DivergenceType,
    PlatformDivergence,
)
from traceboard.domain.quality_gate import GateResultStatus, RuleType
from traceboard.domain.token_value import TokenCategory, TokenValue
from traceboard.infrastructure.repositories.in_memory_quality_gate_repository import (
    InMemoryQualityGateRepository,
)


def build_service() -> QualityGateService:
    return QualityGateService(InMemoryQualityGateRepository())


def test_create_gate() -> None:
    service = build_service()

    command = CreateQualityGateCommand(
        id="gate-1",
        name="Component Quality Gate",
        description="Main quality gate",
    )

    gate = service.create_gate(command)

    assert gate.id == "gate-1"
    assert gate.name == "Component Quality Gate"
    assert service.get_gate("gate-1") == gate


def test_add_rule() -> None:
    service = build_service()

    service.create_gate(CreateQualityGateCommand(id="gate-1", name="Test Gate"))

    command = AddRuleCommand(
        gate_id="gate-1",
        rule_id="rule-1",
        rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
        description="No blocker divergences",
    )

    updated = service.add_rule(command)

    assert len(updated.rules) == 1
    assert updated.rules[0].rule_type == RuleType.NO_BLOCKER_DIVERGENCES


def test_add_rule_gate_not_found() -> None:
    service = build_service()

    command = AddRuleCommand(
        gate_id="nonexistent",
        rule_id="rule-1",
        rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
        description="Rule",
    )

    with pytest.raises(ValueError, match="QualityGate 'nonexistent' not found"):
        service.add_rule(command)


def test_evaluate_gate_no_blocker_pass() -> None:
    service = build_service()

    service.create_gate(CreateQualityGateCommand(id="gate-1", name="Test Gate"))
    service.add_rule(
        AddRuleCommand(
            gate_id="gate-1",
            rule_id="rule-1",
            rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
            description="No blockers",
        )
    )

    report = DivergenceReport(
        component_contract_id="contract-1",
        platform_name="web",
    )

    command = EvaluateGateCommand(
        gate_id="gate-1",
        divergence_report=report,
    )

    result = service.evaluate_gate(command)

    assert result.passed is True
    assert result.rule_results[0].status == GateResultStatus.PASS


def test_evaluate_gate_no_blocker_fail() -> None:
    service = build_service()

    service.create_gate(CreateQualityGateCommand(id="gate-1", name="Test Gate"))
    service.add_rule(
        AddRuleCommand(
            gate_id="gate-1",
            rule_id="rule-1",
            rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
            description="No blockers",
        )
    )

    divergence = PlatformDivergence(
        id="div-1",
        component_contract_id="contract-1",
        platform_name="web",
        requirement_id="req-1",
        divergence_type=DivergenceType.MISSING_TOKEN,
        severity=DivergenceSeverity.BLOCKER,
        description="Missing token",
    )

    report = DivergenceReport(
        component_contract_id="contract-1",
        platform_name="web",
        divergences=(divergence,),
    )

    command = EvaluateGateCommand(
        gate_id="gate-1",
        divergence_report=report,
    )

    result = service.evaluate_gate(command)

    assert result.passed is False
    assert result.rule_results[0].status == GateResultStatus.FAIL


def test_evaluate_gate_contrast_pass() -> None:
    service = build_service()

    service.create_gate(CreateQualityGateCommand(id="gate-1", name="Test Gate"))
    service.add_rule(
        AddRuleCommand(
            gate_id="gate-1",
            rule_id="rule-1",
            rule_type=RuleType.MIN_CONTRAST_RATIO,
            description="Min contrast 4.5",
            threshold=4.5,
        )
    )

    foreground = TokenValue(
        category=TokenCategory.COLOR,
        raw="#1a1a1a",
        description="Dark text",
    )

    background = TokenValue(
        category=TokenCategory.COLOR,
        raw="#ffffff",
        description="White background",
    )

    command = EvaluateGateCommand(
        gate_id="gate-1",
        foreground=foreground,
        background=background,
    )

    result = service.evaluate_gate(command)

    assert result.passed is True


def test_list_gates() -> None:
    service = build_service()

    gate1 = service.create_gate(CreateQualityGateCommand(id="gate-1", name="First Gate"))
    gate2 = service.create_gate(CreateQualityGateCommand(id="gate-2", name="Second Gate"))

    assert service.list_gates() == (gate1, gate2)
