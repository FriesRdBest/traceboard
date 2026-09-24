from __future__ import annotations

from traceboard.domain.token_trace import (
    FileLanguage,
    TokenTrace,
    TokenUsage,
    TraceReport,
    UsageType,
)


def test_token_usage_creation() -> None:
    usage = TokenUsage(
        token_name="--color-primary",
        file_path="src/button.css",
        line_number=10,
        column=5,
        usage_type=UsageType.DIRECT,
        context="color: var(--color-primary)",
        language=FileLanguage.CSS,
    )

    assert usage.token_name == "--color-primary"
    assert usage.file_path == "src/button.css"
    assert usage.line_number == 10
    assert usage.location == "src/button.css:10:5"


def test_token_trace_creation() -> None:
    trace = TokenTrace(token_name="--color-primary")

    assert trace.token_name == "--color-primary"
    assert trace.usage_count == 0
    assert trace.file_count == 0


def test_token_trace_add_usage() -> None:
    trace = TokenTrace(token_name="--color-primary")

    usage = TokenUsage(
        token_name="--color-primary",
        file_path="src/button.css",
        line_number=10,
        column=5,
        usage_type=UsageType.DIRECT,
        context="color: var(--color-primary)",
        language=FileLanguage.CSS,
    )

    updated = trace.add_usage(usage)

    assert updated.usage_count == 1
    assert updated.file_count == 1


def test_token_trace_add_usage_wrong_token() -> None:
    trace = TokenTrace(token_name="--color-primary")

    usage = TokenUsage(
        token_name="--color-secondary",
        file_path="src/button.css",
        line_number=10,
        column=5,
        usage_type=UsageType.DIRECT,
        context="color: var(--color-secondary)",
        language=FileLanguage.CSS,
    )

    try:
        trace.add_usage(usage)
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "Cannot add usage for token" in str(e)


def test_token_trace_summary() -> None:
    usage1 = TokenUsage(
        token_name="--color-primary",
        file_path="src/button.css",
        line_number=10,
        column=5,
        usage_type=UsageType.DIRECT,
        context="color: var(--color-primary)",
        language=FileLanguage.CSS,
    )

    usage2 = TokenUsage(
        token_name="--color-primary",
        file_path="src/card.css",
        line_number=20,
        column=3,
        usage_type=UsageType.DIRECT,
        context="background: var(--color-primary)",
        language=FileLanguage.CSS,
    )

    trace = TokenTrace(token_name="--color-primary", usages=(usage1, usage2))
    summary = trace.summary()

    assert summary["token_name"] == "--color-primary"
    assert summary["usage_count"] == 2
    assert summary["file_count"] == 2
    files = summary["files"]
    assert isinstance(files, list) and "src/button.css" in files
    assert isinstance(files, list) and "src/card.css" in files


def test_trace_report_creation() -> None:
    report = TraceReport(
        scanned_files=("src/button.css", "src/card.css"),
        token_traces=(),
    )

    assert report.total_tokens == 0
    assert report.total_usages == 0
    assert len(report.unused_tokens) == 0


def test_trace_report_with_traces() -> None:
    trace = TokenTrace(token_name="--color-primary")

    report = TraceReport(
        scanned_files=("src/button.css",),
        token_traces=(trace,),
    )

    assert report.total_tokens == 1
    assert report.total_usages == 0
    assert len(report.unused_tokens) == 1


def test_trace_report_get_trace() -> None:
    trace = TokenTrace(token_name="--color-primary")

    report = TraceReport(
        scanned_files=("src/button.css",),
        token_traces=(trace,),
    )

    found = report.get_trace("--color-primary")
    assert found is not None
    assert found.token_name == "--color-primary"

    not_found = report.get_trace("--color-secondary")
    assert not_found is None


def test_trace_report_summary() -> None:
    trace = TokenTrace(token_name="--color-primary")

    report = TraceReport(
        scanned_files=("src/button.css", "src/card.css"),
        token_traces=(trace,),
        scan_errors=("error1",),
    )

    summary = report.summary()

    assert summary["scanned_files_count"] == 2
    assert summary["total_tokens"] == 1
    assert summary["total_usages"] == 0
    assert summary["unused_tokens_count"] == 1
    assert summary["errors_count"] == 1
