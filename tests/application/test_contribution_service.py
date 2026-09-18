from __future__ import annotations

from traceboard.application.contribution_service import (
    ContributionService,
    CreateContributionCommand,
)
from traceboard.domain.contribution import ContributionStatus, Platform, Surface
from traceboard.infrastructure.repositories.in_memory_contribution_repository import (
    InMemoryContributionRepository,
)


def build_service() -> ContributionService:
    return ContributionService(InMemoryContributionRepository())


def build_command() -> CreateContributionCommand:
    return CreateContributionCommand(
        title="Follow-up prompt control",
        problem_statement="Follow-up prompts need a governed density and interaction model.",
        user_context="Readers need relevant next actions without visual overload.",
        surface=Surface.FOLLOW_UP,
        platforms=(Platform.WEB, Platform.IOS),
        submitted_by="design-systems",
        related_token_ids=("token-space-400",),
        related_component_ids=("component-follow-up-prompt",),
    )


def test_create_stores_a_draft_contribution() -> None:
    service = build_service()

    contribution = service.create(build_command())

    assert contribution.status is ContributionStatus.DRAFT
    assert contribution.title == "Follow-up prompt control"
    assert contribution.platforms == (Platform.WEB, Platform.IOS)
    assert service.get_by_id(contribution.id) == contribution


def test_list_contributions_returns_created_contributions_in_creation_order() -> None:
    service = build_service()
    first = service.create(build_command())
    second = service.create(
        CreateContributionCommand(
            title="Answer citation treatment",
            problem_statement="Answer citations need consistent source visibility.",
            user_context="Readers need to distinguish answer claims from source evidence.",
            surface=Surface.ANSWER,
            platforms=(Platform.WEB,),
        )
    )

    assert service.list_contributions() == (first, second)
