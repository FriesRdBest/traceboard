# traceboard

A governance dashboard for Perplexity that traces assets from design file to live code across product surfaces. Built with Python and Streamlit.

## Why this exists

At scale, design systems drift: tokens diverge, components are implemented inconsistently, and the link between design files and production code becomes implicit. Traceboard makes that link explicit and auditable.

It answers questions like:

- Which surfaces are using which token versions?
- Where have components diverged from the canonical pattern?
- What is the compliance posture of each product surface?
- How do we trace a design decision from Figma to deployment?

The goal is not just visibility, but **governance**: enabling design and engineering leaders to enforce standards, prioritize remediation, and measure improvement over time.

## Features

- **Design token governance** — Track and validate tokens across components and surfaces.
- **Component standards** — Enforce consistent patterns and accessibility rules.
- **Asset tracing** — Link design artifacts to implementation and deployment.
- **Quality checks** — Run automated checks across multiple product surfaces.
- **Compliance posture** — Summarize governance status per surface and globally.

## Architecture overview

```
src/traceboard/
├── domain/          # Core concepts: tokens, components, surfaces, checks
├── application/     # Use cases: run checks, compute posture, orchestrate flows
├── infrastructure/  # Adapters: file I/O, external APIs, data persistence
├── ui/              # Streamlit pages and visual components
└── cli/             # Command-line entrypoints (optional automation)
```

Data flow:

1. **Ingest** design tokens, component definitions, and surface manifests (from files or APIs).
2. **Normalize** into domain models (`Token`, `Component`, `Surface`, `Check`).
3. **Execute checks** (token version, component usage, accessibility rules).
4. **Aggregate results** into compliance scores and governance reports.
5. **Visualize** in Streamlit dashboards for design, eng, and leadership.

```
[Design tokens] ─┐
[Components]  ───┼→ domain models → checks → results → dashboards
[Surfaces]    ───┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a deeper dive.

## How to run checks

### Local development

```bash
git clone https://github.com/FriesRdBest/traceboard.git
cd traceboard
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Run the dashboard

```bash
python -m streamlit run app.py
```

### Run checks programmatically

```bash
python -m traceboard.cli.run_checks --config config/example.yml
```

(Adjust the command to match your actual CLI once implemented; the key is to show there is a non-UI entrypoint for automation.)

### Run tests and lint

```bash
python -m pytest
python -m ruff check .
python -m black --check .
```

These same commands are executed in CI on every push and pull request.

## Repository structure

```text
.
├── app.py                 # Streamlit entrypoint
├── src/traceboard/        # Core package
│   ├── domain/            # Domain models and rules
│   ├── application/       # Use cases and orchestration
│   ├── infrastructure/    # I/O and external integrations
│   ├── ui/                # Streamlit UI components
│   └── cli/               # CLI tools
├── tests/                 # Test suite (domain, application, infrastructure)
├── docs/                  # Architecture and design notes
├── .github/workflows/     # CI workflows (test + lint)
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── LICENSE                # Apache License 2.0
```

## CI and quality gates

Traceboard uses GitHub Actions to enforce quality:

- **Tests** – `pytest` runs on every push and PR.
- **Lint** – `ruff` and `black --check` run as separate steps.
- **Dependabot** – weekly dependency updates with limited PRs.

Passing CI is required before merging. This ensures that governance logic itself is governed.

## Contributing

Contributions and focused feedback are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow the [Code of Conduct](CODE_OF_CONDUCT.md) before opening an issue or pull request.

For security concerns, do not open a public issue; follow [SECURITY.md](SECURITY.md).

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
