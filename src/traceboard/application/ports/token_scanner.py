from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from traceboard.domain.token_trace import TokenTrace, TraceReport


class TokenScanner(ABC):
    """Scans source files for design token usages."""

    @abstractmethod
    def scan_file(self, file_path: str, content: str) -> tuple[TokenTrace, ...]:
        """Scan a single file and return token traces found."""

    @abstractmethod
    def scan_files(
        self, file_paths: list[str], read_file: Callable[[str], str]
    ) -> TraceReport:
        """Scan multiple files and return a complete trace report."""
