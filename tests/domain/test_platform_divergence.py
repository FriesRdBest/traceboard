from __future__ import annotations

from traceboard.domain.platform_divergence import (
    DivergenceReport,
    DivergenceSeverity,
    DivergenceType,
    PlatformDivergence,
)


def test_divergence_report_initial_state() -> None:
    report = DivergenceReport(
        component_contract_id="button-1",
        platform_name="web",
    )

    assert not report.has_divergences
    assert report.blocker_count == 0
    assert report.major_count == 0


def test_add_divergence() -> None:
    report = DivergenceReport(
        component_contract_id="button-1",
        platform_name="web",
    )

    divergence = PlatformDivergence(
        id="missing-token-1",
        component_contract_id="button-1",
        platform_name="web",
        requirement_id="req-1",
        divergence_type=DivergenceType.MISSING_TOKEN,
        severity=DivergenceSeverity.BLOCKER,
        description="Required token '--color-primary' is missing",
        details={"token_name": "--color-primary"},
    )

    updated = report.add_divergence(divergence)

    assert updated.has_divergences
    assert len(updated.divergences) == 1
    assert updated.blocker_count == 1
    assert updated.major_count == 0


def test_divergence_report_summary() -> None:
    report = DivergenceReport(
        component_contract_id="button-1",
        platform_name="web",
    )

    divergence1 = PlatformDivergence(
        id="missing-token-1",
        component_contract_id="button-1",
        platform_name="web",
        requirement_id="req-1",
        divergence_type=DivergenceType.MISSING_TOKEN,
        severity=DivergenceSeverity.BLOCKER,
        description="Missing token",
    )

    divergence2 = PlatformDivergence(
        id="missing-token-2",
        component_contract_id="button-1",
        platform_name="web",
        requirement_id="req-2",
        divergence_type=DivergenceType.MISSING_TOKEN,
        severity=DivergenceSeverity.MAJOR,
        description="Missing token",
    )

    updated = report.add_divergence(divergence1).add_divergence(divergence2)

    summary = updated.summary()

    assert summary["component_contract_id"] == "button-1"
    assert summary["platform_name"] == "web"
    assert summary["total_divergences"] == 2
    assert summary["blocker_count"] == 1
    assert summary["major_count"] == 1
