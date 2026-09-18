from __future__ import annotations

from traceboard.domain.component_contract import (
    ComponentContract,
    ContractRequirement,
    RequirementSeverity,
)
from traceboard.domain.divergence_evaluator import DivergenceEvaluator, PlatformState
from traceboard.domain.platform_divergence import DivergenceSeverity, DivergenceType


def test_evaluate_no_divergences() -> None:
    contract = ComponentContract(
        id="button-1",
        component_name="Button",
        requirements=(
            ContractRequirement(
                id="req-1",
                description="Must use primary color",
                token_names=("--color-primary", "--color-text"),
                severity=RequirementSeverity.MUST,
            ),
        ),
    )

    platform_state = PlatformState(
        component_name="Button",
        platform_name="web",
        token_names=("--color-primary", "--color-text"),
        token_values={"--color-primary": "#0066cc", "--color-text": "#1a1a1a"},
        behaviors={},
    )

    evaluator = DivergenceEvaluator(contract)
    report = evaluator.evaluate(platform_state)

    # Only unexpected token checks might add INFO divergences; here none
    assert report.blocker_count == 0
    assert report.major_count == 0


def test_evaluate_missing_token_blocker() -> None:
    contract = ComponentContract(
        id="button-1",
        component_name="Button",
        requirements=(
            ContractRequirement(
                id="req-1",
                description="Must use primary color",
                token_names=("--color-primary", "--color-text"),
                severity=RequirementSeverity.MUST,
            ),
        ),
    )

    platform_state = PlatformState(
        component_name="Button",
        platform_name="web",
        token_names=("--color-primary",),  # Missing --color-text
        token_values={"--color-primary": "#0066cc"},
        behaviors={},
    )

    evaluator = DivergenceEvaluator(contract)
    report = evaluator.evaluate(platform_state)

    assert report.has_divergences
    assert report.blocker_count == 1

    divergence = report.divergences[0]
    assert divergence.divergence_type == DivergenceType.MISSING_TOKEN
    assert divergence.severity == DivergenceSeverity.BLOCKER
    assert divergence.details["token_name"] == "--color-text"


def test_evaluate_missing_token_should_is_major() -> None:
    contract = ComponentContract(
        id="button-1",
        component_name="Button",
        requirements=(
            ContractRequirement(
                id="req-1",
                description="Should use secondary color",
                token_names=("--color-secondary",),
                severity=RequirementSeverity.SHOULD,
            ),
        ),
    )

    platform_state = PlatformState(
        component_name="Button",
        platform_name="web",
        token_names=(),  # Missing --color-secondary
        token_values={},
        behaviors={},
    )

    evaluator = DivergenceEvaluator(contract)
    report = evaluator.evaluate(platform_state)

    assert report.has_divergences
    assert report.major_count == 1
    assert report.blocker_count == 0

    divergence = report.divergences[0]
    assert divergence.severity == DivergenceSeverity.MAJOR


def test_evaluate_unexpected_token_info() -> None:
    contract = ComponentContract(
        id="button-1",
        component_name="Button",
        requirements=(
            ContractRequirement(
                id="req-1",
                description="Must use primary color",
                token_names=("--color-primary",),
                severity=RequirementSeverity.MUST,
            ),
        ),
    )

    platform_state = PlatformState(
        component_name="Button",
        platform_name="web",
        token_names=("--color-primary", "--color-legacy"),  # --color-legacy is unexpected
        token_values={"--color-primary": "#0066cc", "--color-legacy": "#aaa"},
        behaviors={},
    )

    evaluator = DivergenceEvaluator(contract)
    report = evaluator.evaluate(platform_state)

    unexpected = [
        d for d in report.divergences if d.divergence_type == DivergenceType.UNEXPECTED_TOKEN
    ]
    assert len(unexpected) == 1
    assert unexpected[0].severity == DivergenceSeverity.INFO
    assert unexpected[0].details["token_name"] == "--color-legacy"
