from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class RequirementSeverity(Enum):
    MUST = auto()
    SHOULD = auto()
    MAY = auto()


@dataclass(frozen=True)
class ContractRequirement:
    """Individual requirement within a component contract."""

    id: str
    description: str
    token_names: tuple[str, ...] = field(default_factory=tuple)
    severity: RequirementSeverity = RequirementSeverity.MUST
    notes: str | None = None


@dataclass(frozen=True)
class ComponentContract:
    """Contract defining required tokens and behaviors for a component."""

    id: str
    component_name: str
    requirements: tuple[ContractRequirement, ...] = field(default_factory=tuple)
    version: str = "1.0.0"
    description: str | None = None

    def add_requirement(self, requirement: ContractRequirement) -> ComponentContract:
        if any(r.id == requirement.id for r in self.requirements):
            raise ValueError(
                f"Requirement '{requirement.id}' already exists in contract '{self.id}'"
            )

        return ComponentContract(
            id=self.id,
            component_name=self.component_name,
            requirements=(*self.requirements, requirement),
            version=self.version,
            description=self.description,
        )

    def get_requirement(self, requirement_id: str) -> ContractRequirement | None:
        for req in self.requirements:
            if req.id == requirement_id:
                return req
        return None
