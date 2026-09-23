from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScanResult:
    """Result of scanning a single file."""

    file_path: str
    traces: tuple[TokenTrace, ...]


@dataclass(frozen=True)
class TokenTrace:
    """Traced usages of a single token."""

    token_name: str
    usages: list[dict[str, str]]


@dataclass(frozen=True)
class TraceReport:
    """Aggregated report over many files."""

    scan_results: list[ScanResult]
    scan_errors: list[str]
