from __future__ import annotations

import pytest

from traceboard.domain.contribution import Contribution, Platform, Surface
from traceboard.infrastructure.repositories.in_memory_contribution_repository import (
    InMemoryContributionRepository,
)


def build_contribution(contribution_id: str = "contribution-001") -> Contribution:
    return Contribution(
        id=contribution_id,
        title="Citation treatment refinement",
        problem_statement="Citation affordances need consistent answer-surface treatment.",
        user_context="Readers need to assess source credibility without losing answer context.",
        surface=Surface.ANSWER,
        platforms=(Platform.WEB,),
    )


def test_add_and_get_by_id_returns_stored_contribution() -> None:
    repository = InMemoryContributionRepository()
    contribution = build_contribution()

    repository.add(contribution)

    assert repository.get_by_id(contribution.id) == contribution


def test_get_by_id_returns_none_when_contribution_does_not_exist() -> None:
    repository = InMemoryContributionRepository()

    assert repository.get_by_id("missing-contribution") is None


def test_list_all_preserves_explicit_insertion_order() -> None:
    repository = InMemoryContributionRepository()
    first = build_contribution("contribution-001")
    second = build_contribution("contribution-002")

    repository.add(first)
    repository.add(second)

    assert repository.list_all() == (first, second)


def test_add_rejects_duplicate_contribution_id() -> None:
    repository = InMemoryContributionRepository()
    repository.add(build_contribution())

    with pytest.raises(ValueError, match="already exists"):
        repository.add(build_contribution())
