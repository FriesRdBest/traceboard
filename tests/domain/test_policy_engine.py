from __future__ import annotations

from traceboard.domain.component_contract import ComponentContract
from traceboard.domain.platform_divergence import (
    DivergenceReport,
    DivergenceSeverity,
    DivergenceType,
    PlatformDivergence,
)
from traceboard.domain.policy_engine import PolicyContext, PolicyEngine
from traceboard.domain.quality_gate import (
    GateResultStatus,
    QualityGate,
    QualityGateRule,
    RuleType,
)
from traceboard.domain.token_value import TokenCategory, TokenValue


def test_policy_engine_no_blocker_divergences_pass() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Test Gate",
        rules=(
            QualityGateRule(
                id="rule-1",
                rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
                description="No blockers",
            ),
        ),
    )

    report = DivergenceReport(
        component_contract_id="contract-1",
        platform_name="web",
    )

    context = PolicyContext(
        component_contract=None,
        divergence_report=report,
        platform_state=None,
        foreground=None,
        background=None,
    )

    engine = PolicyEngine()
    result = engine.evaluate(gate, context)

    assert result.passed is True
    assert result.rule_results[0].status == GateResultStatus.PASS


def test_policy_engine_no_blocker_divergences_fail() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Test Gate",
        rules=(
            QualityGateRule(
                id="rule-1",
                rule_type=RuleType.NO_BLOCKER_DIVERGENCES,
                description="No blockers",
            ),
        ),
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

    context = PolicyContext(
        component_contract=None,
        divergence_report=report,
        platform_state=None,
        foreground=None,
        background=None,
    )

    engine = PolicyEngine()
    result = engine.evaluate(gate, context)

    assert result.passed is False
    assert result.rule_results[0].status == GateResultStatus.FAIL
    assert result.rule_results[0].actual_value == 1


def test_policy_engine_no_major_divergences_pass() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Test Gate",
        rules=(
            QualityGateRule(
                id="rule-1",
                rule_type=RuleType.NO_MAJOR_DIVERGENCES,
                description="No majors",
            ),
        ),
    )

    report = DivergenceReport(
        component_contract_id="contract-1",
        platform_name="web",
    )

    context = PolicyContext(
        component_contract=None,
        divergence_report=report,
        platform_state=None,
        foreground=None,
        background=None,
    )

    engine = PolicyEngine()
    result = engine.evaluate(gate, context)

    assert result.passed is True


def test_policy_engine_min_contrast_pass() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Test Gate",
        rules=(
            QualityGateRule(
                id="rule-1",
                rule_type=RuleType.MIN_CONTRAST_RATIO,
                description="Min contrast 4.5",
                threshold=4.5,
            ),
        ),
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

    context = PolicyContext(
        component_contract=None,
        divergence_report=None,
        platform_state=None,
        foreground=foreground,
        background=background,
    )

    engine = PolicyEngine()
    result = engine.evaluate(gate, context)

    assert result.passed is True
    assert result.rule_results[0].status == GateResultStatus.PASS


def test_policy_engine_min_contrast_fail() -> None:
    gate = QualityGate(
        id="gate-1",
        name="Test Gate",
        rules=(
            QualityGateRule(
                id="rule-1",
                rule_type=RuleType.MIN_CONTRAST_RATIO,
                description="Min contrast 4.5",
                threshold=4.5,
            ),
        ),
    )

    foreground = TokenValue(
        category=TokenCategory.COLOR,
        raw="#999999",
        description="Gray text",
    )

    background = TokenValue(
        category=TokenCategory.COLOR,
        raw="#ffffff",
        description="White background",
    )

    context = PolicyContext(
        component_contract=None,
        divergence_report=None,
        platform_state=None,
        foreground=foreground,
        background=background,
    )

    engine = PolicyEngine()
    result = engine.evaluate(gate, context)

    assert result.passed is False
    assert result.rule_results[0].status == GateResultStatus.FAIL
