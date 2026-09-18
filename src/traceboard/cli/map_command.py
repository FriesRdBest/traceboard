"""CLI command for generating system map."""

from __future__ import annotations

import argparse
import json

from ..domain.system_map import ComponentNode, SystemMap, TokenDependency


def map_command(args: argparse.Namespace) -> int:
    """Generate system map."""
    system_map = SystemMap()

    system_map = system_map.add_dependency(
        TokenDependency(
            source_token="--color-primary",
            target_token="--color-brand",
            dependency_type="alias",
        )
    )
    system_map = system_map.add_dependency(
        TokenDependency(
            source_token="--color-brand",
            target_token="--color-blue-500",
            dependency_type="reference",
        )
    )

    system_map = system_map.add_component(
        ComponentNode(
            component_name="Button",
            contract_id="button-contract",
            token_names=("--color-primary", "--spacing-sm"),
        )
    )

    if args.mermaid:
        print(system_map.to_mermaid())
    elif args.json:
        print(json.dumps(system_map.summary(), indent=2))
    else:
        print(f"\n{'=' * 60}")
        print("SYSTEM MAP")
        print(f"{'=' * 60}\n")
        print(f"Tokens: {system_map.token_count}")
        print(f"Dependencies: {system_map.dependency_count}")
        print(f"Components: {system_map.component_count}")

        if system_map.token_dependencies:
            print(f"\n{'=' * 60}")
            print("TOKEN DEPENDENCIES")
            print(f"{'=' * 60}")
            for dep in system_map.token_dependencies:
                print(f"  {dep.source_token} --[{dep.dependency_type}]--> {dep.target_token}")

        if system_map.component_nodes:
            print(f"\n{'=' * 60}")
            print("COMPONENTS")
            print(f"{'=' * 60}")
            for comp in system_map.component_nodes:
                print(f"  {comp.component_name} ({comp.contract_id})")
                for token in comp.token_names:
                    print(f"    - {token}")

    return 0
