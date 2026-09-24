from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..domain.token_trace import TokenTrace, TokenUsage, TraceReport

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .ports.token_scanner import TokenScanner


@dataclass(frozen=True)
class ScanDirectoryCommand:
    """Command to scan a directory for token usage."""

    directory: str
    patterns: tuple[str, ...] = ("*.json", "*.css", "*.scss")
    exclude_patterns: tuple[str, ...] = ("node_modules", "dist", "build", ".git")


class TraceService:
    """Application service for token trace operations."""

    def __init__(self, scanners: list[TokenScanner]) -> None:
        self.scanners = scanners

    def scan_directory(self, command: ScanDirectoryCommand) -> TraceReport:
        """Scan a directory and return trace report."""
        from pathlib import Path

        dir_path = Path(command.directory)
        if not dir_path.exists():
            raise ValueError(f"Directory '{command.directory}' does not exist")

        all_files: list[str] = []
        for pattern in command.patterns:
            all_files.extend(str(p) for p in dir_path.rglob(pattern))

        filtered_files: list[str] = []
        for file_path in all_files:
            excluded = False
            for exclude in command.exclude_patterns:
                if exclude in file_path:
                    excluded = True
                    break
            if not excluded:
                filtered_files.append(file_path)

        all_traces: dict[str, list[TokenUsage]] = {}
        all_errors: list[str] = []

        for scanner in self.scanners:
            json_files = [f for f in filtered_files if f.endswith(".json")]
            if json_files:
                try:
                    report = scanner.scan_files(json_files, lambda p: Path(p).read_text())
                    for trace in report.token_traces:
                        if trace.token_name not in all_traces:
                            all_traces[trace.token_name] = []
                        all_traces[trace.token_name].extend(trace.usages)
                    all_errors.extend(report.scan_errors)
                except (OSError, ValueError) as error:
                    all_errors.append(f"Scanner error: {error!s}")

        token_traces = tuple(
            TokenTrace(token_name=name, usages=tuple(usages)) for name, usages in all_traces.items()
        )

        return TraceReport(
            scanned_files=tuple(filtered_files),
            token_traces=token_traces,
            scan_errors=tuple(all_errors),
        )

    def get_token_trace(self, report: TraceReport, token_name: str) -> TokenTrace | None:
        """Get trace for a specific token from a report."""
        return report.get_trace(token_name)

    def list_unused_tokens(self, report: TraceReport) -> Sequence[TokenTrace]:
        """List tokens with no usages."""
        return report.unused_tokens

    def list_high_usage_tokens(self, report: TraceReport) -> Sequence[TokenTrace]:
        """List tokens used more than 10 times."""
        return report.high_usage_tokens
