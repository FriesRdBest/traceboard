from __future__ import annotations

from pathlib import Path
from traceboard.application.trace_service import ScanDirectoryCommand, TraceService
from traceboard.infrastructure.scanners.json_token_scanner import JsonTokenScanner


def test_scan_directory_command_creation() -> None:
    cmd = ScanDirectoryCommand(directory="src/tokens")

    assert cmd.directory == "src/tokens"
    assert "*.json" in cmd.patterns
    assert "node_modules" in cmd.exclude_patterns


def test_trace_service_initialization() -> None:
    scanners = [JsonTokenScanner()]
    service = TraceService(scanners)

    assert len(service.scanners) == 1


def test_trace_service_scan_nonexistent_directory() -> None:
    scanners = [JsonTokenScanner()]
    service = TraceService(scanners)

    cmd = ScanDirectoryCommand(directory="/nonexistent/path")

    try:
        service.scan_directory(cmd)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "does not exist" in str(e)


def test_trace_service_get_token_trace() -> None:
    from traceboard.domain.token_trace import TokenTrace, TraceReport

    scanners = [JsonTokenScanner()]
    service = TraceService(scanners)

    trace = TokenTrace(token_name="--color-primary")
    report = TraceReport(
        scanned_files=("test.json",),
        token_traces=(trace,),
    )

    found = service.get_token_trace(report, "--color-primary")
    assert found is not None
    assert found.token_name == "--color-primary"

    not_found = service.get_token_trace(report, "--color-secondary")
    assert not_found is None


def test_trace_service_list_unused_tokens() -> None:
    from traceboard.domain.token_trace import TokenTrace, TraceReport

    scanners = [JsonTokenScanner()]
    service = TraceService(scanners)

    trace = TokenTrace(token_name="--color-primary")
    report = TraceReport(
        scanned_files=("test.json",),
        token_traces=(trace,),
    )

    unused = service.list_unused_tokens(report)
    assert len(unused) == 1
    assert unused[0].token_name == "--color-primary"


def test_trace_service_list_high_usage_tokens() -> None:
    from traceboard.domain.token_trace import TokenTrace, TokenUsage, TraceReport, UsageType, FileLanguage

    scanners = [JsonTokenScanner()]
    service = TraceService(scanners)

    # Create a trace with 15 usages
    usages = tuple(
        TokenUsage(
            token_name="--color-primary",
            file_path=f"file{i}.css",
            line_number=i,
            column=1,
            usage_type=UsageType.DIRECT,
            context="test",
            language=FileLanguage.CSS,
        )
        for i in range(15)
    )
    trace = TokenTrace(token_name="--color-primary", usages=usages)

    report = TraceReport(
        scanned_files=("test.json",),
        token_traces=(trace,),
    )

    high_usage = service.list_high_usage_tokens(report)
    assert len(high_usage) == 1
    assert high_usage[0].usage_count == 15
