# Contributing to Traceboard

## Scope

Traceboard is a design-system governance control room with a pure Python domain core and separately layered application and UI surfaces. Contributions must preserve separation of concerns and must not introduce UI, persistence, framework, or environment dependencies into `src/traceboard/domain`.

## Before changing code

1. Read the relevant domain model, service, repository, and test files.
2. Identify the smallest coherent change that solves the stated problem.
3. Confirm the change respects the repository architecture.
4. Keep unrelated refactoring, formatting, or dependency changes out of the same pull request.
5. Add or update tests before requesting review.

## Development setup

Create and activate a virtual environment, then install the project and development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pre-commit install
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Required verification

Run every command from the repository root before opening a pull request:

```bash
ruff check src tests
ruff format --check src tests
pyright src/traceboard
pytest
pre-commit run --all-files
```

A pull request is not ready when any required check fails.

## Architecture rules

- Domain models remain independent of Streamlit, web frameworks, file systems, databases, environment variables, and external service adapters.
- Application services coordinate use cases without owning presentation behavior.
- Repository interfaces define persistence boundaries; persistence implementations belong outside the domain package.
- UI code consumes application interfaces and does not encode domain business rules.
- Design tokens must use primitive, semantic, and component tiers.
- New color, spacing, typography, radius, elevation, or motion values require a named token.
- Accessibility requirements must be represented in tests or explicit Quality Gate rules.
- Platform divergence must be intentional, documented, and represented in a component contract.
- Commits must not contain credentials, secrets, local data, generated caches, or personal information.

## Commit conventions

Use short, imperative commit subjects. Include a scope when it clarifies the affected layer:

```text
feat(domain): add contribution lifecycle transition
fix(tokens): reject invalid semantic references
test(domain): cover contribution validation
docs: define release trace workflow
chore(ci): enforce strict type verification
```

## Pull requests

Each pull request must identify:

- What changed.
- Why the change is needed.
- Which architectural boundary is affected.
- How the change was verified.
- Any intentional platform divergence.
- Any migration, compatibility, or rollback implication.

Keep the pull request narrow enough that a reviewer can validate the complete behavior without reconstructing unrelated context.

## Review standard

Approval requires:

- Passing automated checks.
- Clear domain, application, repository, and UI boundaries.
- No untracked magic values in governed design-system code.
- Tests for new behavior and regressions.
- Documentation for public contracts, workflow changes, and migration paths.
