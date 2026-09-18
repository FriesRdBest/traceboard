# Traceboard

Design token traceability and quality gate system for design systems.

## Features

- Token Tracing: Scan codebases for design token usage
- Quality Gates: Define and enforce token quality rules
- Component Contracts: Define required tokens for components
- Divergence Detection: Find mismatches between platforms
- System Maps: Visualize token dependencies

## CLI Usage

### Token Trace

python -m traceboard.cli.main trace ./tokens --patterns "*.json,*.css" --verbose

### System Map

python -m traceboard.cli.main map --mermaid

## Architecture

src/traceboard/
  application/     # Application services
  domain/          # Core business logic
  infrastructure/  # External adapters
  cli/             # Command-line interface

## Development

pytest -v
pre-commit run --all-files

## License

MIT
