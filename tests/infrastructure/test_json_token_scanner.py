from __future__ import annotations

from traceboard.infrastructure.scanners.json_token_scanner import JsonTokenScanner


def test_scan_file_finds_token_references() -> None:
    scanner = JsonTokenScanner()

    content = """
    {
        "button": {
            "color": "--color-primary",
            "background": "--color-brand"
        }
    }
    """

    traces = scanner.scan_file("tokens.json", content)

    assert len(traces) == 2
    token_names = {t.token_name for t in traces}
    assert "--color-primary" in token_names
    assert "--color-brand" in token_names


def test_scan_file_empty_json() -> None:
    scanner = JsonTokenScanner()

    content = "{}"

    traces = scanner.scan_file("empty.json", content)

    assert len(traces) == 0


def test_scan_file_invalid_json() -> None:
    scanner = JsonTokenScanner()

    content = "{ invalid json }"

    traces = scanner.scan_file("invalid.json", content)

    assert len(traces) == 0


def test_scan_file_nested_tokens() -> None:
    scanner = JsonTokenScanner()

    content = """
    {
        "theme": {
            "colors": {
                "primary": "--color-primary",
                "secondary": "--color-secondary"
            }
        }
    }
    """

    traces = scanner.scan_file("nested.json", content)

    assert len(traces) == 2
    token_names = {t.token_name for t in traces}
    assert "--color-primary" in token_names
    assert "--color-secondary" in token_names


def test_scan_files_multiple_files() -> None:
    scanner = JsonTokenScanner()

    files = {
        "file1.json": '{"token": "--color-primary"}',
        "file2.json": '{"token": "--color-secondary"}',
    }

    report = scanner.scan_files(list(files.keys()), lambda p: files[p])

    assert len(report.scanned_files) == 2
    assert len(report.token_traces) == 2
    assert len(report.scan_errors) == 0


def test_scan_files_with_errors() -> None:
    scanner = JsonTokenScanner()

    def read_file(path: str) -> str:
        if path == "good.json":
            return '{"token": "--color-primary"}'
        else:
            raise FileNotFoundError("File not found")

    report = scanner.scan_files(["good.json", "bad.json"], read_file)

    assert len(report.scanned_files) == 1
    assert len(report.scan_errors) == 1
    assert "bad.json" in report.scan_errors[0]
