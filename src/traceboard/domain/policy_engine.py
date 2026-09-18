from __future__ import annotations

from dataclasses import dataclass

from .component_contract import ComponentContract
from .contrast_evaluator import ContrastEvaluator
from .divergence_evaluator import PlatformState
from .platform_divergence import DivergenceReport
from .quality_gate import (
    GateEvaluationResult,
    GateResultStatus,
    QualityGate,
    QualityGateResult,
    QualityGateRule,
    RuleType,
)
from .token_value import TokenValue


@dataclass(frozen=True)
class PolicyContext:
    """Aggregates all data needed for policy evaluation."""

    component_contract: ComponentContract | None
    divergence_report: DivergenceReport | None
    platform_state: PlatformState | None
    foreground: TokenValue | None  # For contrast checks
    background: TokenValue | None


class PolicyEngine:
    """Pure-domain policy engine evaluating quality gates against context."""

    def evaluate(self, gate: QualityGate, context: PolicyContext) -> GateEvaluationResult:
        rule_results: list[QualityGateResult] = []
        has_failure = False

        for rule in gate.rules:
            result = self._evaluate_rule(rule, context)
            rule_results.append(result)
            if result.status == GateResultStatus.FAIL:
                has_failure = True

        overall_status = GateResultStatus.FAIL if has_failure else GateResultStatus.PASS

        return GateEvaluationResult(
            gate_id=gate.id,
            gate_name=gate.name,
            rule_results=tuple(rule_results),
            overall_status=overall_status,
        )

    def _evaluate_rule(self, rule: QualityGateRule, context: PolicyContext) -> QualityGateResult:
        if rule.rule_type == RuleType.NO_BLOCKER_DIVERGENCES:
            return self._check_no_blocker_divergences(rule, context)
        elif rule.rule_type == RuleType.NO_MAJOR_DIVERGENCES:
            return self._check_no_major_divergences(rule, context)
        elif rule.rule_type == RuleType.MIN_CONTRAST_RATIO:
            return self._check_min_contrast(rule, context)
        else:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.SKIP,
                message=f"Rule type {rule.rule_type} not implemented",
            )

    def _check_no_blocker_divergences(
        self, rule: QualityGateRule, context: PolicyContext
    ) -> QualityGateResult:
        report = context.divergence_report
        if report is None:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.SKIP,
                message="No divergence report available",
            )

        if report.blocker_count == 0:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.PASS,
                message="No blocker divergences found",
                actual_value=0,
                expected_value=0,
            )
        else:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.FAIL,
                message=f"Found {report.blocker_count} blocker divergence(s)",
                actual_value=report.blocker_count,
                expected_value=0,
            )

    def _check_no_major_divergences(
        self, rule: QualityGateRule, context: PolicyContext
    ) -> QualityGateResult:
        report = context.divergence_report
        if report is None:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.SKIP,
                message="No divergence report available",
            )

        if report.major_count == 0:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.PASS,
                message="No major divergences found",
                actual_value=0,
                expected_value=0,
            )
        else:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.FAIL,
                message=f"Found {report.major_count} major divergence(s)",
                actual_value=report.major_count,
                expected_value=0,
            )

    def _check_min_contrast(
        self, rule: QualityGateRule, context: PolicyContext
    ) -> QualityGateResult:
        if context.foreground is None or context.background is None:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.SKIP,
                message="Foreground or background token not available",
            )

        threshold = rule.threshold or 4.5  # WCAG AA normal text default

        result = ContrastEvaluator.evaluate(
            context.foreground.raw,
            context.background.raw,
        )

        if result.ratio >= threshold:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.PASS,
                message=f"Contrast ratio {result.ratio:.2f} meets threshold {threshold}",
                actual_value=result.ratio,
                expected_value=threshold,
            )
        else:
            return QualityGateResult(
                rule_id=rule.id,
                status=GateResultStatus.FAIL,
                message=f"Contrast ratio {result.ratio:.2f} below threshold {threshold}",
                actual_value=result.ratio,
                expected_value=threshold,
            )
