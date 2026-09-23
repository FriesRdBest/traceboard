from __future__ import annotations

import streamlit as st

from traceboard.ui.components import (
    badge,
    close_panel,
    panel,
    render_evidence_list,
    render_trace_row,
    table,
)


def render() -> None:
    with st.container(border=False):
        panel(
            "Component contract",
            "A component is not approved until its behavior is explicit.",
            elevation="raised",
        )
        component = st.selectbox(
            "Component", ("Citation card", "Button", "Status badge", "Data table")
        )
        table(
            ("Contract area", "Requirement", "State"),
            (
                ("Anatomy", "Identity, evidence, metadata", "Defined"),
                ("Interaction", "Keyboard and pointer parity", "Defined"),
                ("Content", "Long titles wrap without clipping", "Required"),
                ("Accessibility", "Visible focus and semantic labels", "Required"),
            ),
        )
        st.markdown(f"Current contract: {badge(component, 'accent')}", unsafe_allow_html=True)
        st.markdown(
            render_trace_row(
                "Component anatomy",
                "Contract review",
                "Implementation approval",
                "Defined",
                tone="success",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_evidence_list(
                [
                    {
                        "type": "CONTRACT",
                        "status": "Defined",
                        "title": f"{component} behavior contract",
                        "excerpt": (
                            "Anatomy, interaction, content resilience, "
                            "and accessibility expectations are explicit."
                        ),
                        "tone": "success",
                    }
                ]
            ),
            unsafe_allow_html=True,
        )
        close_panel()
