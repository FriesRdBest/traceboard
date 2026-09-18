"""CLI command for running token traces."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from ..application.trace_service import ScanDirectoryCommand, TraceService
from ..infrastructure.scanners.json_token_scanner import JsonTokenScanner

if TYPE_CHECKING:
    import argparse

    from ..application.ports.token_scanner import TokenScanner


def trace_command(args: argparse.Namespace) -> int:
    """Run token trace on a directory."""
    scanners: list[TokenScanner] = [JsonTokenScanner()]
    service = TraceService(scanners)

    cmd = ScanDirectoryCommand(
        directory=args.directory,
        patterns=args.patterns.split(",") if args.patterns else ("*.json",),
        exclude_patterns=args.exclude.split(",") if args.exclude else ("node_modules", "dist"),
    )

    try:
        report = service.scan_directory(cmd)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if args.json:
        print(json.dumps(report.summary(), indent=2))
    else:
        print(f"\n{'=' * 60}")
        print("TOKEN TRACE REPORT")
        print(f"{'=' * 60}\n")
        print(f"Scanned files: {len(report.scanned_files)}")
        print(f"Total tokens: {report.total_tokens}")
        print(f"Total usages: {report.total_usages}")
        print(f"Unused tokens: {len(report.unused_tokens)}")
        print(f"High usage tokens: {len(report.high_usage_tokens)}")

        if report.unused_tokens:
            print(f"\n{'=' * 60}")
            print("UNUSED TOKENS")
            print(f"{'=' * 60}")
            for trace in report.unused_tokens:
                print(f"  - {trace.token_name}")

        if args.verbose and report.token_traces:
            print(f"\n{'=' * 60}")
            print("TOKEN DETAILS")
            print(f"{'=' * 60}")
            for trace in report.token_traces[:10]:
                print(f"\n{trace.token_name}:")
                print(f"  Usage count: {trace.usage_count}")
                print(f"  Files: {trace.file_count}")

    if report.scan_errors:
        print(f"\n{'=' * 60}")
        print("ERRORS")
        print(f"{'=' * 60}")
        for error in report.scan_errors:
            print(f"  - {error}")

    return 0
