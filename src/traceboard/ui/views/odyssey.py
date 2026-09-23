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
            "System Story",
            "A narrative record of how governance becomes a product capability.",
            elevation="raised",
        )
        st.markdown("### The system under pressure")
        st.write(
            "Traceboard turns design-system work into an observable chain "
            "of decisions: contribution, contract, quality, and release."
        )
        st.markdown("### Operating principles")
        st.write(
            "Prefer evidence over preference. Prefer shared primitives "
            "over local fixes. Prefer a visible blocked state over a "
            "silent compromise."
        )
        st.markdown(
            render_trace_row(
                "Contribution",
                "Governance",
                "Product capability",
                "Recorded",
                tone="info",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_evidence_list(
                [
                    {
                        "type": "PRINCIPLE",
                        "status": "Canonical",
                        "title": "Evidence over preference",
                        "excerpt": (
                            "System decisions should remain explainable "
                            "through their supporting record."
                        ),
                        "tone": "success",
                    }
                ]
            ),
            unsafe_allow_html=True,
        )
        close_panel()
