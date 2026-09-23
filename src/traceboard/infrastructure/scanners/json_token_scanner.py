from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from traceboard.application.ports.token_scanner import TokenScanner
from traceboard.domain.token_trace import ScanResult, TokenTrace, TraceReport

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class JsonTokenUsage:
    """A token usage found in JSON."""

    token_name: str
    path: str
    value: str


class JsonTokenScanner(TokenScanner):
    """Scans JSON files for design token usages."""

    def __init__(self, token_prefix: str = "--") -> None:
        self._token_prefix = token_prefix

    def scan_file(self, file_path: str, content: str) -> tuple[TokenTrace, ...]:
        """Scan a single JSON file and return token traces."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning("Invalid JSON in %s: %s", file_path, e)
            return ()

        usages = self._extract_usages(data, file_path)
        return self._group_usages_into_traces(usages)

    def scan_files(
        self, file_paths: list[str], read_file: Callable[[str], str]
    ) -> TraceReport:
        """Scan multiple JSON files and return a trace report."""
        scan_results: list[ScanResult] = []
        errors: list[str] = []

        for file_path in file_paths:
            try:
                content = read_file(file_path)
            except FileNotFoundError:
                errors.append(f"{file_path}: file not found")
                continue
            except OSError as e:
                errors.append(f"{file_path}: {e!s}")
                continue

            try:
                traces = self.scan_file(file_path, content)
                scan_results.append(ScanResult(file_path=file_path, traces=traces))
            except ValueError as e:
                errors.append(f"{file_path}: {e}")
            except Exception as e:
                logger.exception("Unexpected error scanning %s", file_path)
                errors.append(f"{file_path}: {e!s}")

        return TraceReport(scan_results=scan_results, scan_errors=errors)

    def _extract_usages(self, data: Any, file_path: str) -> list[JsonTokenUsage]:
        """Recursively extract token usages from a JSON structure."""
        usages: list[JsonTokenUsage] = []
        self._walk_json(data, [], usages, file_path)
        return usages

    def _walk_json(
        self,
        node: Any,
        path: list[str],
        usages: list[JsonTokenUsage],
        file_path: str,
    ) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                self._walk_json(value, [*path, key], usages, file_path)
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                self._walk_json(item, [*path, str(idx)], usages, file_path)
        elif isinstance(node, str):
            for token_name in self._extract_tokens_from_string(node):
                usages.append(
                    JsonTokenUsage(
                        token_name=token_name,
                        path=".".join(path),
                        value=node,
                    )
                )

    def _extract_tokens_from_string(self, value: str) -> list[str]:
        """Extract token names from a string value."""
        tokens: list[str] = []
        for part in value.split():
            if part.startswith(self._token_prefix):
                tokens.append(part)
        return tokens

    def _group_usages_into_traces(
        self, usages: list[JsonTokenUsage]
    ) -> tuple[TokenTrace, ...]:
        """Group raw usages into token traces."""
        by_token: dict[str, list[JsonTokenUsage]] = {}
        for u in usages:
            by_token.setdefault(u.token_name, []).append(u)

        traces: list[TokenTrace] = []
        for token_name, token_usages in by_token.items():
            traces.append(
                TokenTrace(
                    token_name=token_name,
                    usages=[
                        {
                            "path": u.path,
                            "value": u.value,
                        }
                        for u in token_usages
                    ],
                )
            )
        return tuple(traces)
