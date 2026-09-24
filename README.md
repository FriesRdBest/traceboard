# Traceboard

A governance dashboard for Perplexity that traces assets from design file to live code
across product surfaces. Built with Python and Streamlit.

## Features

- **Design token governance** — Track and validate tokens across components and surfaces.
- **Component standards** — Enforce consistent patterns and accessibility rules.
- **Asset tracing** — Link design artifacts to implementation and deployment.
- **Quality checks** — Run automated checks across multiple product surfaces.

## Local development

### Requirements

- Python 3.10 or later
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup

```bash
git clone https://github.com/FriesRdBest/traceboard.git
cd traceboard
poetry sync
poetry run streamlit run app.py
```

Streamlit will print a local URL, typically `http://localhost:8501`.

## Verification

Run the complete local quality suite before opening a pull request:

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run pyright
poetry run pytest -q
```

Expected baseline:

- Ruff reports no findings.
- Ruff formatting reports no files requiring formatting.
- Pyright reports 0 errors.
- Pytest reports all tests passing.

## Dependency and deployment policy

Traceboard uses Poetry with both `pyproject.toml` and a committed `poetry.lock`.

- Use `poetry sync` to install the locked dependency set.
- When dependency constraints change in `pyproject.toml`, regenerate the lock file with
  `poetry lock` and commit the resulting `poetry.lock` in the same pull request.
- Do not use `poetry update` for routine setup; it can resolve newer versions than the
  committed baseline.
- Streamlit Cloud installs the project from this same Poetry configuration. Keeping the
  lock file in sync makes local development, CI, and deployment reproducible.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
