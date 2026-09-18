from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .token_trace import TokenTrace


@dataclass(frozen=True)
class TokenDependency:
    """Represents a dependency between two tokens."""

    source_token: str
    target_token: str
    dependency_type: str


@dataclass(frozen=True)
class ComponentNode:
    """A component in the system map."""

    component_name: str
    contract_id: str
    token_names: tuple[str, ...]


@dataclass(frozen=True)
class SystemMap:
    """Complete system map of token relationships."""

    token_dependencies: tuple[TokenDependency, ...] = field(default_factory=tuple)
    component_nodes: tuple[ComponentNode, ...] = field(default_factory=tuple)
    token_traces: tuple[TokenTrace, ...] = field(default_factory=tuple)

    @property
    def dependency_count(self) -> int:
        return len(self.token_dependencies)

    @property
    def component_count(self) -> int:
        return len(self.component_nodes)

    @property
    def token_count(self) -> int:
        tokens: set[str] = set()
        for dep in self.token_dependencies:
            tokens.add(dep.source_token)
            tokens.add(dep.target_token)
        for node in self.component_nodes:
            tokens.update(node.token_names)
        return len(tokens)

    def add_dependency(self, dep: TokenDependency) -> SystemMap:
        return SystemMap(
            token_dependencies=(*self.token_dependencies, dep),
            component_nodes=self.component_nodes,
            token_traces=self.token_traces,
        )

    def add_component(self, component: ComponentNode) -> SystemMap:
        return SystemMap(
            token_dependencies=self.token_dependencies,
            component_nodes=(*self.component_nodes, component),
            token_traces=self.token_traces,
        )

    def get_token_dependencies(self, token_name: str) -> tuple[TokenDependency, ...]:
        return tuple(
            dep for dep in self.token_dependencies
            if dep.source_token == token_name or dep.target_token == token_name
        )

    def to_mermaid(self) -> str:
        """Generate Mermaid.js diagram syntax."""
        lines = ["graph TD"]

        tokens: set[str] = set()
        for dep in self.token_dependencies:
            tokens.add(dep.source_token)
            tokens.add(dep.target_token)

        for token in sorted(tokens):
            safe_name = token.replace("-", "_").replace(".", "_")
            lines.append(f"    {safe_name}[{token}]")

        for dep in self.token_dependencies:
            source = dep.source_token.replace("-", "_").replace(".", "_")
            target = dep.target_token.replace("-", "_").replace(".", "_")
            lines.append(f"    {source} -->|{dep.dependency_type}| {target}")

        for comp in self.component_nodes:
            safe_name = comp.component_name.replace("-", "_").replace(".", "_")
            lines.append(f"    {safe_name}({comp.component_name})")
            for token in comp.token_names:
                token_safe = token.replace("-", "_").replace(".", "_")
                lines.append(f"    {safe_name} --- {token_safe}")

        return "\n".join(lines)

    def summary(self) -> dict[str, int]:
        return {
            "token_count": self.token_count,
            "dependency_count": self.dependency_count,
            "component_count": self.component_count,
        }
