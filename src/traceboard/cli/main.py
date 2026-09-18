"""Main CLI entry point."""
from __future__ import annotations

import argparse
import sys

from .trace_command import trace_command
from .map_command import map_command


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="traceboard",
        description="Design token trace and system map CLI",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    trace_parser = subparsers.add_parser("trace", help="Scan directory for token usage")
    trace_parser.add_argument("directory", help="Directory to scan")
    trace_parser.add_argument("-p", "--patterns", help="File patterns (comma-separated)")
    trace_parser.add_argument("-e", "--exclude", help="Exclude patterns (comma-separated)")
    trace_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    trace_parser.add_argument("--json", action="store_true", help="Output as JSON")
    trace_parser.set_defaults(func=trace_command)

    map_parser = subparsers.add_parser("map", help="Generate system map")
    map_parser.add_argument("--mermaid", action="store_true", help="Output as Mermaid diagram")
    map_parser.add_argument("--json", action="store_true", help="Output as JSON")
    map_parser.set_defaults(func=map_command)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
