from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from ...application.ports.token_scanner import TokenScanner
from ...domain.token_trace import (
    FileLanguage,
    TokenTrace,
    TokenUsage,
    TraceReport,
    UsageType,
)

if TYPE_CHECKING:
    from collections.abc import Callable


TOKEN_PATTERN = re.compile(r'["\']?(--[a-zA-Z0-9_-]+)["\']?')


class JsonTokenScanner(TokenScanner):
    """Scans JSON files for design token references."""

    def scan_file(self, file_path: str, content: str) -> tuple[TokenTrace, ...]:
        traces: dict[str, list[TokenUsage]] = {}

        try:
            data = json.loads(content)
            lines = content.split("\n")

            self._scan_value(data, file_path, lines, traces, path="")
        except json.JSONDecodeError:
            pass

        return tuple(
            TokenTrace(token_name=name, usages=tuple(usages)) for name, usages in traces.items()
        )

    def _scan_value(
        self,
        value: Any,
        file_path: str,
        lines: list[str],
        traces: dict[str, list[TokenUsage]],
        path: str,
    ) -> None:
        if isinstance(value, str):
            self._scan_string(value, file_path, lines, traces, path)
        elif isinstance(value, dict):
            for key, val in value.items():  # type: ignore
                new_path = f"{path}.{key}" if path else f"{key}"
                self._scan_value(val, file_path, lines, traces, new_path)
        elif isinstance(value, list):
            for i, item in enumerate(value):  # type: ignore
                new_path = f"{path}[{i}]"
                self._scan_value(item, file_path, lines, traces, new_path)

    def _scan_string(
        self,
        value: str,
        file_path: str,
        lines: list[str],
        traces: dict[str, list[TokenUsage]],
        path: str,
    ) -> None:
        for match in TOKEN_PATTERN.finditer(value):
            token_name = match.group(1)

            actual_line = 1
            actual_column = 1
            for i, line in enumerate(lines, 1):
                if token_name in line:
                    actual_line = i
                    actual_column = line.find(token_name) + 1
                    break

            usage = TokenUsage(
                token_name=token_name,
                file_path=file_path,
                line_number=actual_line,
                column=actual_column,
                usage_type=UsageType.DIRECT,
                context=value[:50] + "..." if len(value) > 50 else value,
                language=FileLanguage.JSON,
            )

            if token_name not in traces:
                traces[token_name] = []
            traces[token_name].append(usage)

    def scan_files(self, file_paths: list[str], read_file: Callable[[str], str]) -> TraceReport:
        all_traces: dict[str, list[TokenUsage]] = {}
        errors: list[str] = []
        scanned: list[str] = []

        for file_path in file_paths:
            try:
                content = read_file(file_path)
                scanned.append(file_path)

                file_traces = self.scan_file(file_path, content)
                for trace in file_traces:
                    if trace.token_name not in all_traces:
                        all_traces[trace.token_name] = []
                    all_traces[trace.token_name].extend(trace.usages)

            except Exception as e:
                errors.append(f"{file_path}: {e!s}")

        token_traces = tuple(
            TokenTrace(token_name=name, usages=tuple(usages)) for name, usages in all_traces.items()
        )

        return TraceReport(
            scanned_files=tuple(scanned),
            token_traces=token_traces,
            scan_errors=tuple(errors),
        )
