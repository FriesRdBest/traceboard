from __future__ import annotations

from ...application.ports.component_contract_repository import ComponentContractRepository
from ...domain.component_contract import ComponentContract
from ...domain.platform_divergence import DivergenceReport


class InMemoryComponentContractRepository(ComponentContractRepository):
    """In-memory adapter for ComponentContractRepository."""

    def __init__(self) -> None:
        self._contracts: dict[str, ComponentContract] = {}
        self._divergence_reports: dict[tuple[str, str], DivergenceReport] = {}

    def add(self, contract: ComponentContract) -> None:
        # Upsert semantics
        self._contracts[contract.id] = contract

    def get(self, contract_id: str) -> ComponentContract | None:
        return self._contracts.get(contract_id)

    def get_all(self) -> tuple[ComponentContract, ...]:
        return tuple(self._contracts.values())

    def save_divergence_report(self, report: DivergenceReport) -> None:
        key = (report.component_contract_id, report.platform_name)
        self._divergence_reports[key] = report

    def get_divergence_report(
        self, contract_id: str, platform_name: str
    ) -> DivergenceReport | None:
        key = (contract_id, platform_name)
        return self._divergence_reports.get(key)
