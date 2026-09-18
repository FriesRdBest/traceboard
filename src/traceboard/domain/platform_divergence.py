from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class DivergenceType(Enum):
    MISSING_TOKEN = auto()
    UNEXPECTED_TOKEN = auto()
    TOKEN_VALUE_MISMATCH = auto()
    BEHAVIOR_MISMATCH = auto()
    OTHER = auto()


class DivergenceSeverity(Enum):
    BLOCKER = auto()
    MAJOR = auto()
    MINOR = auto()
    INFO = auto()


def _empty_details() -> dict[str, str]:
    return {}


@dataclass(frozen=True)
class PlatformDivergence:
    """Records a divergence between a platform and the component contract."""

    id: str
    component_contract_id: str
    platform_name: str
    requirement_id: str | None
    divergence_type: DivergenceType
    severity: DivergenceSeverity
    description: str
    details: dict[str, str] = field(default_factory=_empty_details)


@dataclass(frozen=True)
class DivergenceReport:
    """Aggregates divergences for a component across platforms."""

    component_contract_id: str
    platform_name: str
    divergences: tuple[PlatformDivergence, ...] = field(default_factory=tuple)

    @property
    def has_divergences(self) -> bool:
        return len(self.divergences) > 0

    @property
    def blocker_count(self) -> int:
        return sum(1 for d in self.divergences if d.severity == DivergenceSeverity.BLOCKER)

    @property
    def major_count(self) -> int:
        return sum(1 for d in self.divergences if d.severity == DivergenceSeverity.MAJOR)

    def add_divergence(self, divergence: PlatformDivergence) -> DivergenceReport:
        return DivergenceReport(
            component_contract_id=self.component_contract_id,
            platform_name=self.platform_name,
            divergences=(*self.divergences, divergence),
        )

    def summary(self) -> dict[str, int | str]:
        return {
            "component_contract_id": self.component_contract_id,
            "platform_name": self.platform_name,
            "total_divergences": len(self.divergences),
            "blocker_count": self.blocker_count,
            "major_count": self.major_count,
        }
