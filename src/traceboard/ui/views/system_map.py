from __future__ import annotations

import streamlit as st


def render_system_map() -> None:
    st.header("System Map")
    st.write(
        "Architecture surface for domain, application services, repositories, and UI boundaries."
    )
    st.caption(
        "Boundary: UI composition only. This view documents, but does not implement, architecture."
    )
