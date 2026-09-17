from __future__ import annotations

import streamlit as st


def configure_page() -> None:
    st.set_page_config(
        page_title="Traceboard",
        page_icon=":material/account_tree:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": None,
            "Report a bug": None,
            "About": "Traceboard is a design-system governance control room.",
        },
    )


def render_app_shell() -> None:
    st.title("Traceboard")
    st.caption("Design-system governance control room")
    st.divider()
