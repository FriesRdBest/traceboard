from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ...domain.token_trace import TokenTrace, TraceReport


class TokenScanner(ABC):
    """Port for scanning source files for token references."""

    @abstractmethod
    def scan_file(self, file_path: str, content: str) -> tuple[TokenTrace, ...]:
        """Scan a single file and return token traces found."""
        pass

    @abstractmethod
    def scan_files(self, file_paths: list[str], read_file: Callable[[str], str]) -> TraceReport:
        """Scan multiple files and return a complete trace report."""
        pass
