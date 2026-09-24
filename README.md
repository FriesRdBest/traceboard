# Traceboard

Traceboard is a governance workspace for design systems and front‑end platforms. It makes the link between product decisions, design tokens, component contracts, and quality gates explicit and reviewable, so teams can see how a change flows from intake to release.

**Live app:** <https://traceboard.streamlit.app/>

## Problem

Front‑end platforms drift: tokens diverge across themes, component contracts loosen, and quality rules are applied inconsistently. Reviews happen in scattered tools, and the rationale for decisions is lost. The result is slower releases, fragile components, and unclear ownership.

## What Traceboard provides today

Traceboard implements a lightweight governance workflow on top of a design system codebase:

- **Workspace intake:** register contributions and link them to epics, components, and tokens.
- **Token trace:** follow a token from definition through theme aliases to concrete values.
- **Component contracts:** capture expected props, variants, and token bindings per component.
- **Quality gates:** define and evaluate rules for tokens, contrast, and divergence.
- **System map:** visualise the current component/token landscape.
- **Release trace:** track what changed, why, and which gates passed before release.

The UI is a Streamlit app backed by a layered Python codebase (domain, application, infrastructure, UI). There is no database yet; state is file‑based and intended for local/CI review workflows.

## Architecture at a glance

```text
src/traceboard/
  domain/           # core models: Token, DesignToken, ThemeAlias, TokenTrace,
                    # ComponentContract, QualityGate, PolicyEngine, SystemMap, etc.
  application/      # services: trace, token_lab, component_contract,
                    # quality_gate, contribution
  infrastructure/   # repositories and scanners (file-based for now)
  ui/
    views/          # Streamlit pages:
                    # workspace, contribution_intake, token_lab, system_map,
                    # component_contract, quality_gate, release_trace, etc.
    shell, layout, navigation, components, design_system
  cli/              # command-line entrypoints (future)
```

This structure keeps domain rules independent from UI and storage, making it easier to swap in a database or CI integration later without rewriting the core logic.

## Getting started (local)

Traceboard uses Poetry for dependency management. A lock file is committed and must be kept in sync with `pyproject.toml`.

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

### Install and run

```bash
# Clone
git clone [https://github.com/FriesRdBest/traceboard.git](https://github.com/FriesRdBest/traceboard.git)
cd traceboard

# Install dependencies (creates/updates venv and installs from poetry.lock)
poetry sync

# Run the Streamlit app
poetry run streamlit run app.py
```

Then open the URL printed by Streamlit (or use the live app above).

### Reproducibility policy

- `pyproject.toml` and `poetry.lock` are the source of truth for dependencies.
- Do not edit `poetry.lock` by hand.
- After changing dependencies, run `poetry sync` and commit both files together.
- Streamlit Cloud and CI must install via Poetry using the committed lock file.

## Verification

Run the quality suite before merging:

```bash
# Lint
poetry run ruff check .

# Format check
poetry run ruff format --check .

# Type check
poetry run pyright .

# Tests
poetry run pytest
```

Current baseline (as of Batch 1):

- Ruff: no errors
- Ruff format: clean
- Pyright: 0 errors
- Pytest: 92 passed

## Roadmap (future work)

Planned improvements, in rough priority order:

1. **Persistent storage:** replace file-based state with a database (e.g. SQLite/Postgres) and a migration strategy.
2. **CI integration:** run quality gates and token/contract checks in CI, posting results back to PRs.
3. **Token pipeline import:** ingest tokens from Style Dictionary / Figma Tokens and generate reports on divergence and contrast.
4. **Component contract enforcement:** integrate with component libraries to validate contracts in tests or build.
5. **Multi-project workspaces:** support multiple design systems or product areas in one Traceboard instance.
6. **Access control and audit log:** track who changed what and why, with role-based views.

These are explicit future items; the current README describes only what exists today.

## License

MIT
