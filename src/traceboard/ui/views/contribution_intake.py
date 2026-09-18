from __future__ import annotations

import streamlit as st

from traceboard.ui.components import close_panel, panel


def render() -> None:
    with st.container(border=False):
        panel(
            "Contribution brief",
            "Capture the decision before implementation begins.",
            elevation="raised",
        )
        left, right = st.columns(2)
        with left:
            title = st.text_input("Contribution title", placeholder="e.g. Verified source badge")
            contributor = st.text_input("Contributor", placeholder="Name or team")
            category = st.selectbox(
                "Category", ("Token", "Component", "Pattern", "Content", "Motion")
            )
        with right:
            rationale = st.text_area(
                "Decision rationale", placeholder="What problem does this solve?"
            )
            evidence = st.text_input(
                "Evidence reference", placeholder="URL, ticket, or decision record"
            )
            blocking = st.checkbox("Potentially release-blocking")
        if st.button("Stage contribution", type="primary"):
            st.session_state.last_contribution = {
                "title": title,
                "contributor": contributor,
                "category": category,
                "rationale": rationale,
                "evidence": evidence,
                "blocking": blocking,
            }
            st.success("Contribution staged in the local review queue.")
        close_panel()
