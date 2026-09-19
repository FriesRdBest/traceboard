from __future__ import annotations

import streamlit as st

from traceboard.ui.components import render_evidence_list, render_trace_row


def render_system_map() -> None:
    st.header("System Map")
    st.write(
        "Architecture surface for domain, application services, repositories, and UI boundaries."
    )
    st.caption(
        "Boundary: UI composition only. This view documents, but does not implement, architecture."
    )
    st.markdown(
        render_trace_row(
            "Domain model",
            "Application service",
            "UI surface",
            "Mapped",
            tone="info",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        render_evidence_list(
            [
                {
                    "type": "ARCHITECTURE",
                    "status": "Documented",
                    "title": "Layer boundary record",
                    "excerpt": "Domain rules remain separate from application orchestration and UI composition.",
                    "tone": "info",
                }
            ]
        ),
        unsafe_allow_html=True,
    )
