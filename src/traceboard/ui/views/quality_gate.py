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
            "Quality gate",
            "Blocking conditions remain visible until evidence closes them.",
            elevation="raised",
        )
        table(
            ("Gate", "Owner", "Result", "Evidence"),
            (
                ("Token compliance", "Design systems", "Pass", "Token inventory"),
                ("Responsive behavior", "Frontend", "Review", "Viewport matrix"),
                ("Keyboard access", "Accessibility", "Pass", "Focus audit"),
                ("Content resilience", "Product", "Blocked", "Long-source fixture"),
            ),
        )
        st.markdown(
            f"Overall status: {badge('Review required', 'warning')}", unsafe_allow_html=True
        )
        st.markdown(
            render_trace_row(
                "Quality checks",
                "Gate decision",
                "Release readiness",
                "Review required",
                tone="warning",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_evidence_list(
                [
                    {
                        "type": "AUDIT",
                        "status": "Open",
                        "title": "Content resilience fixture",
                        "excerpt": (
                            "The blocked fixture must pass before release readiness can advance."
                        ),
                        "tone": "warning",
                    },
                    {
                        "type": "AUDIT",
                        "status": "Passed",
                        "title": "Keyboard focus audit",
                        "excerpt": (
                            "Visible focus behavior has been recorded for the current surface."
                        ),
                        "tone": "success",
                    },
                ]
            ),
            unsafe_allow_html=True,
        )
        close_panel()
