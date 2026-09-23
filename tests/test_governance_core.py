"""Core governance tests: checks, posture, and aggregation.

These tests demonstrate disciplined testing of traceboard's domain and application logic.
They are intentionally small but serious: focused on invariants, edge cases, and clarity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterable

# In a real repo these would import from src/traceboard/domain & application.
# For this example we define minimal stand-ins to keep the file self-contained.


@dataclass(frozen=True)
class Token:
    name: str
    version: str
    value: str


@dataclass(frozen=True)
class Component:
    name: str
    token_versions: dict[str, str]  # token_name -> required version


@dataclass(frozen=True)
class Surface:
    name: str
    tokens: dict[str, str]  # token_name -> used version
    components: dict[str, dict[str, str]]  # component_name -> {token_name: used_version}


@dataclass(frozen=True)
class CheckResult:
    surface: str
    check: str
    passed: bool
    details: str


def token_version_check(surface: Surface, token_name: str, required_version: str) -> CheckResult:
    """Check that a surface uses the required version of a token."""
    used_version = surface.tokens.get(token_name)
    if used_version is None:
        return CheckResult(
            surface=surface.name,
            check=f"token_version[{token_name}]",
            passed=False,
            details=f"Token {token_name} not used on surface {surface.name}",
        )
    passed = used_version == required_version
    return CheckResult(
        surface=surface.name,
        check=f"token_version[{token_name}]",
        passed=passed,
        details=(
            f"Expected {required_version}, got {used_version}"
            if not passed
            else f"Token {token_name} at required version {required_version}"
        ),
    )


def component_token_alignment_check(surface: Surface, component: Component) -> CheckResult:
    """Check that a component's tokens on a surface match the canonical versions."""
    comp_tokens = surface.components.get(component.name)
    if comp_tokens is None:
        return CheckResult(
            surface=surface.name,
            check=f"component_alignment[{component.name}]",
            passed=False,
            details=f"Component {component.name} not used on surface {surface.name}",
        )

    violations = []
    for token_name, required_version in component.token_versions.items():
        used_version = comp_tokens.get(token_name)
        if used_version != required_version:
            violations.append(
                f"{token_name}: expected {required_version}, got {used_version or 'missing'}"
            )

    if not violations:
        return CheckResult(
            surface=surface.name,
            check=f"component_alignment[{component.name}]",
            passed=True,
            details=f"Component {component.name} tokens align with canonical versions",
        )

    return CheckResult(
        surface=surface.name,
        check=f"component_alignment[{component.name}]",
        passed=False,
        details="; ".join(violations),
    )


def compute_posture(results: Iterable[CheckResult]) -> dict[str, float]:
    """Compute pass-rate posture per surface."""
    surface_totals: dict[str, int] = {}
    surface_passes: dict[str, int] = {}

    for r in results:
        surface_totals[r.surface] = surface_totals.get(r.surface, 0) + 1
        if r.passed:
            surface_passes[r.surface] = surface_passes.get(r.surface, 0) + 1

    posture = {}
    for s, total in surface_totals.items():
        passes = surface_passes.get(s, 0)
        posture[s] = passes / total if total > 0 else 0.0

    return posture


class TestTokenVersionCheck:
    def test_pass_when_version_matches(self) -> None:
        surface = Surface(
            name="web-app",
            tokens={"color-primary": "v2.1.0"},
            components={},
        )
        result = token_version_check(surface, "color-primary", "v2.1.0")
        assert result.passed is True
        assert "at required version" in result.details

    def test_fail_when_version_mismatches(self) -> None:
        surface = Surface(
            name="marketing-site",
            tokens={"color-primary": "v1.3.0"},
            components={},
        )
        result = token_version_check(surface, "color-primary", "v2.1.0")
        assert result.passed is False
        assert "Expected v2.1.0, got v1.3.0" in result.details

    def test_fail_when_token_missing(self) -> None:
        surface = Surface(
            name="internal-tool",
            tokens={},
            components={},
        )
        result = token_version_check(surface, "color-primary", "v2.1.0")
        assert result.passed is False
        assert "not used" in result.details


class TestComponentTokenAlignment:
    def test_pass_when_all_tokens_align(self) -> None:
        surface = Surface(
            name="web-app",
            tokens={},
            components={
                "Button": {"color-primary": "v2.1.0", "spacing-md": "v1.0.0"},
            },
        )
        component = Component(
            name="Button",
            token_versions={"color-primary": "v2.1.0", "spacing-md": "v1.0.0"},
        )
        result = component_token_alignment_check(surface, component)
        assert result.passed is True
        assert "align" in result.details

    def test_fail_when_any_token_mismatches(self) -> None:
        surface = Surface(
            name="marketing-site",
            tokens={},
            components={
                "Button": {"color-primary": "v1.3.0", "spacing-md": "v1.0.0"},
            },
        )
        component = Component(
            name="Button",
            token_versions={"color-primary": "v2.1.0", "spacing-md": "v1.0.0"},
        )
        result = component_token_alignment_check(surface, component)
        assert result.passed is False
        assert "color-primary" in result.details
        assert "v2.1.0" in result.details
        assert "v1.3.0" in result.details

    def test_fail_when_component_missing_on_surface(self) -> None:
        surface = Surface(
            name="internal-tool",
            tokens={},
            components={},
        )
        component = Component(
            name="Button",
            token_versions={"color-primary": "v2.1.0"},
        )
        result = component_token_alignment_check(surface, component)
        assert result.passed is False
        assert "not used" in result.details


class TestComputePosture:
    def test_posture_with_mixed_results(self) -> None:
        results = [
            CheckResult("web-app", "token_version[color-primary]", True, ""),
            CheckResult("web-app", "component_alignment[Button]", False, ""),
            CheckResult("marketing-site", "token_version[color-primary]", False, ""),
            CheckResult("marketing-site", "component_alignment[Button]", False, ""),
        ]
        posture = compute_posture(results)
        assert posture["web-app"] == pytest.approx(0.5)
        assert posture["marketing-site"] == pytest.approx(0.0)

    def test_posture_with_all_pass(self) -> None:
        results = [
            CheckResult("web-app", "check1", True, ""),
            CheckResult("web-app", "check2", True, ""),
        ]
        posture = compute_posture(results)
        assert posture["web-app"] == pytest.approx(1.0)

    def test_posture_with_no_results_for_surface(self) -> None:
        results: list[CheckResult] = []
        posture = compute_posture(results)
        assert posture == {}
