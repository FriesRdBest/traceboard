from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FileLanguage(StrEnum):
    """Supported file languages for token tracing."""

    JSON = "json"
    TS = "ts"
    TSX = "tsx"
    CSS = "css"


@dataclass(frozen=True)
class ScanResult:
    """Result of scanning a single file."""

    file_path: str
    language: FileLanguage
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
