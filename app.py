from __future__ import annotations

import streamlit as st

from traceboard.application.contribution_service import (
    ContributionService,
    CreateContributionCommand,
)
from traceboard.domain.contribution import Platform, Surface
from traceboard.infrastructure.repositories.in_memory_contribution_repository import (
    InMemoryContributionRepository,
)
from traceboard.ui.views.component_contract import render_component_contract
from traceboard.ui.views.quality_gate import render_quality_gate
from traceboard.ui.views.release_trace import render_release_trace
from traceboard.ui.views.system_map import render_system_map
from traceboard.ui.views.token_lab import render_token_lab
from traceboard.ui.views.workspace import render_workspace


@st.cache_resource
def get_service() -> ContributionService:
    repository = InMemoryContributionRepository()
    return ContributionService(repository)


def render_contribution_intake(service: ContributionService) -> None:
    st.header("Contribution Intake")
    st.write("Record a proposed feature, fix, or improvement for Traceboard.")

    with st.form("create_contribution", clear_on_submit=True):
        title = st.text_input(
            "Title",
            placeholder="Example: Add CSV export for contribution records",
        )
        problem_statement = st.text_area(
            "Problem statement",
            placeholder="What problem does this contribution solve?",
        )
        user_context = st.text_area(
            "User context",
            placeholder="Who experiences this problem, and when?",
        )

        surface_options = [surface.value for surface in Surface]
        surface_value = st.selectbox("Surface", options=surface_options)

        platform_options = [platform.value for platform in Platform]
        platform_values = st.multiselect(
            "Platforms",
            options=platform_options,
            default=[platform_options[0]] if platform_options else [],
        )

        submitted_by = st.text_input(
            "Submitted by (optional)",
            placeholder="Your name or username",
        )

        submitted = st.form_submit_button("Create contribution", type="primary")

        if submitted:
            if not title.strip() or not problem_statement.strip() or not user_context.strip():
                st.error("Title, problem statement, and user context are required.")
            elif not platform_values:
                st.error("Select at least one platform.")
            else:
                command = CreateContributionCommand(
                    title=title.strip(),
                    problem_statement=problem_statement.strip(),
                    user_context=user_context.strip(),
                    surface=Surface(surface_value),
                    platforms=tuple(Platform(platform) for platform in platform_values),
                    submitted_by=submitted_by.strip() or None,
                )
                contribution = service.create(command)
                st.success(f"Contribution created: {contribution.id}")

    st.subheader("Contributions")

    contributions = service.list_contributions()
    if not contributions:
        st.info("No contributions yet. Use the form above to add the first one.")
    else:
        for contribution in contributions:
            with st.expander(f"{contribution.id} — {contribution.title}"):
                st.write(f"**Surface:** {contribution.surface.value}")
                st.write(
                    f"**Platforms:** {', '.join(platform.value for platform in contribution.platforms)}"
                )
                st.write(f"**Status:** {contribution.status.value}")
                if contribution.submitted_by:
                    st.write(f"**Submitted by:** {contribution.submitted_by}")
                st.write("**Problem statement:**")
                st.write(contribution.problem_statement)
                st.write("**User context:**")
                st.write(contribution.user_context)


def main() -> None:
    st.set_page_config(
        page_title="Traceboard",
        page_icon="🔎",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("Traceboard")
    st.sidebar.caption("A workspace for contribution and governance tracking.")

    page = st.sidebar.radio(
        "Navigation",
        options=[
            "Workspace",
            "Contribution Intake",
            "Component Contract",
            "Quality Gate",
            "System Map",
            "Release Trace",
            "Token Lab",
        ],
    )

    st.title("Traceboard")

    if page == "Workspace":
        render_workspace()
    elif page == "Contribution Intake":
        render_contribution_intake(get_service())
    elif page == "Component Contract":
        render_component_contract()
    elif page == "Quality Gate":
        render_quality_gate()
    elif page == "System Map":
        render_system_map()
    elif page == "Release Trace":
        render_release_trace()
    else:
        render_token_lab()


if __name__ == "__main__":
    main()
