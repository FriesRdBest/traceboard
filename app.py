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


@st.cache_resource
def get_service() -> ContributionService:
    repository = InMemoryContributionRepository()
    return ContributionService(repository)


def main() -> None:
    st.set_page_config(page_title="Traceboard", layout="wide")
    st.title("Traceboard")

    service = get_service()

    st.header("Create contribution")

    with st.form("create_contribution", clear_on_submit=True):
        title = st.text_input("Title")
        problem_statement = st.text_area("Problem statement")
        user_context = st.text_area("User context")

        surface_options = [s.value for s in Surface]
        surface_value = st.selectbox("Surface", options=surface_options)

        platform_options = [p.value for p in Platform]
        platform_values = st.multiselect(
            "Platforms",
            options=platform_options,
            default=[platform_options[0]] if platform_options else [],
        )

        submitted_by = st.text_input("Submitted by (optional)")

        submitted = st.form_submit_button("Create contribution")

        if submitted:
            if not title or not problem_statement or not user_context:
                st.error("Title, problem statement, and user context are required.")
            elif not platform_values:
                st.error("Select at least one platform.")
            else:
                command = CreateContributionCommand(
                    title=title,
                    problem_statement=problem_statement,
                    user_context=user_context,
                    surface=Surface(surface_value),
                    platforms=tuple(Platform(p) for p in platform_values),
                    submitted_by=submitted_by or None,
                )
                contribution = service.create(command)
                st.success(f"Created contribution: {contribution.id}")

    st.header("Contributions")

    contributions = service.list_contributions()
    if not contributions:
        st.info("No contributions yet.")
    else:
        for c in contributions:
            with st.expander(f"{c.id} — {c.title}"):
                st.write(f"**Surface:** {c.surface.value}")
                st.write(f"**Platforms:** {', '.join(p.value for p in c.platforms)}")
                st.write(f"**Status:** {c.status.value}")
                if c.submitted_by:
                    st.write(f"**Submitted by:** {c.submitted_by}")
                st.write("**Problem statement:**")
                st.write(c.problem_statement)
                st.write("**User context:**")
                st.write(c.user_context)


if __name__ == "__main__":
    main()
