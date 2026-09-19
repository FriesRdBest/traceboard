"""Traceboard Streamlit entry point."""

from __future__ import annotations

import streamlit as st

from traceboard.ui.design_system import get_css
from traceboard.ui.views import (
    component_contract,
    contribution_intake,
    odyssey,
    quality_gate,
    release_trace,
    token_lab,
    workspace,
)


def configure_page() -> None:
    st.set_page_config(
        page_title="Traceboard",
        page_icon="https://www.perplexity.ai/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)


def build_pages():
    return [
        st.Page(
            workspace.render,
            title="Workspace",
            url_path="workspace",
            default=True,
        ),
        st.Page(
            contribution_intake.render,
            title="Intake",
            url_path="intake",
        ),
        st.Page(
            token_lab.render,
            title="Tokens",
            url_path="tokens",
        ),
        st.Page(
            component_contract.render,
            title="Contracts",
            url_path="contracts",
        ),
        st.Page(
            quality_gate.render,
            title="Quality",
            url_path="quality",
        ),
        st.Page(
            odyssey.render,
            title="Story",
            url_path="story",
        ),
        st.Page(
            release_trace.render,
            title="Release",
            url_path="release",
        ),
    ]


configure_page()
navigation = st.navigation(build_pages(), position="sidebar")
navigation.run()
