# Traceboard Architecture

This document describes the architecture of traceboard, the governance dashboard for Perplexity. It is intended for engineers and designers who want to understand how the system works and how to extend it.

## Goals

- Make the link between design assets (tokens, components) and live surfaces explicit and queryable.
- Provide automated checks that encode design-system rules and accessibility requirements.
- Summarize compliance posture in a way that is actionable for leadership.
- Remain simple enough to evolve as the design system and product surfaces change.

## High-level design

Traceboard follows a layered architecture:

```
UI (Streamlit)
    ↓
Application (use cases, orchestration)
    ↓
Domain (models, rules, checks)
    ↓
Infrastructure (I/O, adapters, persistence)
```

### Domain layer

The domain layer defines the core concepts:

- **Token** – a design token (color, spacing, typography, etc.) with version and value.
- **Component** – a UI component with a canonical definition and allowed variations.
- **Surface** – a product surface (e.g., web app, marketing site, internal tool) that consumes tokens and components.
- **Check** – a rule that validates tokens, components, or surfaces against standards.

Key responsibilities:

- Define data structures and invariants.
- Encode design-system rules as pure functions where possible.
- Remain independent of frameworks and I/O details.

### Application layer

The application layer implements use cases:

- **RunChecks** – load configuration, execute checks against a set of surfaces, and return results.
- **ComputePosture** – aggregate check results into per-surface and global compliance scores.
- **GenerateReport** – produce structured output (e.g., JSON, Markdown) for dashboards or export.

This layer coordinates domain objects but does not directly perform I/O. It depends on abstractions defined in infrastructure.

### Infrastructure layer

Infrastructure provides adapters for:

- Loading tokens, components, and surface manifests from files or APIs.
- Persisting check results (e.g., JSON files, database).
- Integrating with external systems (e.g., design tools, CI).

The infrastructure layer implements interfaces required by the application layer. Dependencies point inward: infrastructure depends on domain/application, not vice versa.

### UI layer

The UI is a Streamlit application that:

- Displays compliance dashboards per surface and globally.
- Allows filtering by token, component, check type, and surface.
- Surfaces detailed violation information and remediation guidance.

UI components call application use cases; they do not directly access domain models or infrastructure.

## Data flow

1. **Configuration** specifies which surfaces to analyze and where to load assets from.
2. **Infrastructure** loads tokens, components, and surfaces into domain models.
3. **Application** runs checks against these models.
4. **Results** are aggregated into posture scores and rendered in the UI.

```
config → load assets → domain models → run checks → results → posture → UI
```

## Extending traceboard

### Adding a new check

1. Define the check in `domain/checks.py` (or a dedicated module).
2. Implement the validation logic as a pure function where possible.
3. Wire the check into the `RunChecks` use case in the application layer.
4. Add tests in `tests/domain/` or `tests/application/`.

### Adding a new surface

1. Add a surface manifest (tokens/components used) in the configured location.
2. Ensure the manifest conforms to the expected schema.
3. Update configuration to include the new surface.
4. Run checks; the surface will appear in dashboards automatically.

### Adding a new data source

1. Implement a loader in `infrastructure/loaders.py` (or a new module).
2. Ensure it returns domain models consistent with existing loaders.
3. Update configuration to reference the new loader.

## Quality and governance

Traceboard itself is governed:

- All changes go through pull requests with passing CI.
- Tests cover domain rules and key use cases.
- Linting and formatting are enforced via pre-commit and CI.
- Dependabot keeps dependencies up to date.

This ensures that the tool used to enforce standards is itself held to high standards.

## Future directions

Possible evolutions (not exhaustive):

- Integration with design tools (e.g., Figma) for automatic asset ingestion.
- Trend analysis over time (com posture per week/month).
- Automated remediation suggestions or code-fix PRs for simple violations.
- More granular ownership (per-team or per-repo posture).

These should be added incrementally, preserving simplicity and clarity.
