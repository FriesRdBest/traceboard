from __future__ import annotations

import streamlit as st


def render_token_lab() -> None:
    st.header("Token Lab")
    st.write(
        "Three-tier inspection surface for primitive, semantic, and component design-token decisions."
    )
    st.caption(
        "Boundary: UI composition only. Token validation remains a domain and Quality Gate concern."
    )
