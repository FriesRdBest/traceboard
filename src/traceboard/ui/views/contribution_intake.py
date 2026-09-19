from __future__ import annotations

import streamlit as st

from traceboard.ui.components import (
    close_panel,
    panel,
    render_evidence_list,
    render_trace_row,
)


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
        st.markdown(
            """
            <style>
            .st-key-stage-contribution button {
                background: #d6e8e5 !important;
                color: #092326 !important;
                border: 1px solid #d6e8e5 !important;
                font-weight: 700 !important;
            }

            .st-key-stage-contribution button:hover {
                background: #ffffff !important;
                color: #092326 !important;
                border-color: #ffffff !important;
            }

            .st-key-stage-contribution button:focus-visible {
                outline: 3px solid #00e5ff !important;
                outline-offset: 3px !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Stage contribution",
            type="primary",
            key="stage-contribution",
        ):
            st.session_state.last_contribution = {
                "title": title,
                "contributor": contributor,
                "category": category,
                "rationale": rationale,
                "evidence": evidence,
                "blocking": blocking,
            }
            st.success("Contribution staged in the local review queue.")

        st.markdown(
            render_trace_row(
                "Contribution brief",
                "Evidence review",
                "Implementation queue",
                "Ready" if evidence else "Needs evidence",
                tone="success" if evidence else "warning",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_evidence_list(
                [
                    {
                        "type": "REFERENCE",
                        "status": "Attached" if evidence else "Missing",
                        "title": evidence or "Evidence reference pending",
                        "excerpt": (
                            "This reference will support the contribution decision."
                            if evidence
                            else "Add a URL, ticket, or decision record before staging."
                        ),
                        "tone": "success" if evidence else "warning",
                    }
                ]
            ),
            unsafe_allow_html=True,
        )
        close_panel()
