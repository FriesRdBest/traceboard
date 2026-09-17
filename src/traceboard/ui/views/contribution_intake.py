from __future__ import annotations

import streamlit as st


def render_contribution_intake() -> None:
    st.header("Contribution Intake")
    st.write(
        "Technical intake surface for platform scope, problem definition, and preview evidence."
    )
    st.caption(
        "Boundary: UI composition only. Submission behavior will be delegated to an application service."
    )
