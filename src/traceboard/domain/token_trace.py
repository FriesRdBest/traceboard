from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class UsageType(Enum):
    """How a token is referenced in code."""

    DIRECT = auto()
    ALIAS = auto()
    COMPUTED = auto()
    IMPORT = auto()
    UNKNOWN = auto()


class FileLanguage(Enum):
    """Source file language for token usage."""

    CSS = auto()
    SCSS = auto()
    TYPESCRIPT = auto()
    JAVASCRIPT = auto()
    JSON = auto()
    YAML = auto()
    OTHER = auto()


@dataclass(frozen=True)
class TokenUsage:
    """A single reference to a design token in source code."""

    token_name: str
    file_path: str
    line_number: int
    column: int
    usage_type: UsageType
    context: str
    language: FileLanguage = FileLanguage.CSS

    @property
    def location(self) -> str:
        return f"{self.file_path}:{self.line_number}:{self.column}"


@dataclass(frozen=True)
class TokenTrace:
    """Aggregates all usages of a single token."""

    token_name: str
    usages: tuple[TokenUsage, ...] = field(default_factory=tuple)

    @property
    def usage_count(self) -> int:
        return len(self.usages)

    @property
    def file_count(self) -> int:
        return len(set(u.file_path for u in self.usages))

    @property
    def languages(self) -> tuple[FileLanguage, ...]:
        return tuple(sorted(set(u.language for u in self.usages), key=lambda x: x.name))

    def add_usage(self, usage: TokenUsage) -> TokenTrace:
        if usage.token_name != self.token_name:
            raise ValueError(
                f"Cannot add usage for token '{usage.token_name}' to trace for '{self.token_name}'"
            )
        return TokenTrace(
            token_name=self.token_name,
            usages=(*self.usages, usage),
        )

    def summary(self) -> dict[str, str | int | list[str]]:
        return {
            "token_name": self.token_name,
            "usage_count": self.usage_count,
            "file_count": self.file_count,
            "languages": [lang.name for lang in self.languages],
            "files": sorted(set(u.file_path for u in self.usages)),
        }


@dataclass(frozen=True)
class TraceReport:
    """Complete report of all token traces from a scan."""

    scanned_files: tuple[str, ...]
    token_traces: tuple[TokenTrace, ...]
    scan_errors: tuple[str, ...] = field(default_factory=tuple)

    @property
    def total_tokens(self) -> int:
        return len(self.token_traces)

    @property
    def total_usages(self) -> int:
        return sum(t.usage_count for t in self.token_traces)

    @property
    def unused_tokens(self) -> tuple[TokenTrace, ...]:
        return tuple(t for t in self.token_traces if t.usage_count == 0)

    @property
    def high_usage_tokens(self) -> tuple[TokenTrace, ...]:
        """Tokens used more than 10 times."""
        return tuple(t for t in self.token_traces if t.usage_count > 10)

    def get_trace(self, token_name: str) -> TokenTrace | None:
        for trace in self.token_traces:
            if trace.token_name == token_name:
                return trace
        return None

    def summary(self) -> dict[str, int | list[str]]:
        return {
            "scanned_files_count": len(self.scanned_files),
            "total_tokens": self.total_tokens,
            "total_usages": self.total_usages,
            "unused_tokens_count": len(self.unused_tokens),
            "high_usage_tokens_count": len(self.high_usage_tokens),
            "errors_count": len(self.scan_errors),
            "tokens": [t.token_name for t in self.token_traces],
        }
