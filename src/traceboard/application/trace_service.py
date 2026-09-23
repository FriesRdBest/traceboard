from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from traceboard.application.ports.token_scanner import TokenScanner
    from traceboard.domain.token_trace import TokenTrace

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScanDirectoryCommand:
    """Command to scan a directory for token traces."""

    directory: str
    patterns: tuple[str, ...] = ("*.json",)


@dataclass(frozen=True)
class TraceResult:
    all_traces: dict[str, list[TokenTrace]]
    errors: list[str]


class TraceService:
    """Application service for running token traces."""

    def __init__(self, scanner: TokenScanner) -> None:
        self._scanner = scanner

    def run_trace(self, file_paths: list[str], read_file: Callable[[str], str]) -> TraceResult:
        """Run a token trace over the given files."""
        all_traces: dict[str, list[TokenTrace]] = {}
        errors: list[str] = []

        report = self._scanner.scan_files(file_paths, read_file)
        for scan_result in report.scan_results:
            try:
                for trace in scan_result.traces:
                    all_traces.setdefault(trace.token_name, []).append(trace)
                errors.extend(report.scan_errors)
            except ValueError as e:
                errors.append(f"Scanner error for {scan_result.file_path}: {e}")
            except Exception as e:
                logger.exception("Unexpected error during trace")
                errors.append(f"Unexpected scanner error: {e!s}")

        return TraceResult(all_traces=all_traces, errors=errors)
