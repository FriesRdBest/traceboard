from __future__ import annotations

from abc import ABC, abstractmethod

from traceboard.domain.component_contract import ComponentContract
from traceboard.domain.divergence_report import DivergenceReport


class ComponentContractRepository(ABC):
    """Repository for component contracts and divergence reports."""

    @abstractmethod
    def add(self, contract: ComponentContract) -> None:
        """Add or update a component contract."""

    @abstractmethod
    def get(self, contract_id: str) -> ComponentContract | None:
        """Get a component contract by ID."""

    @abstractmethod
    def get_all(self) -> tuple[ComponentContract, ...]:
        """Get all component contracts."""

    @abstractmethod
    def save_divergence_report(self, report: DivergenceReport) -> None:
        """Persist a divergence report."""

    @abstractmethod
    def get_divergence_report(
        self, contract_id: str, platform: str
    ) -> DivergenceReport | None:
        """Get a divergence report for a contract and platform."""
