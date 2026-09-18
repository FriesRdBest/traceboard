"""Traceboard application shell."""

from __future__ import annotations

import streamlit as st

from traceboard.ui.design_system import get_css
from traceboard.ui.navigation import NAV_ITEMS, render_navigation


def configure_page() -> None:
    st.set_page_config(
        page_title="Traceboard",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.session_state.traceboard_theme = "dark"
    st.markdown('<div data-theme="dark"></div>', unsafe_allow_html=True)
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)


def render_shell():
    st.markdown(
        """
        <header class="tb-masthead">
            <div class="tb-masthead-brand">
                <span class="tb-mark">◈</span>
                <span class="tb-kicker">DESIGN-SYSTEM GOVERNANCE</span>
            </div>
            <div class="tb-masthead-row">
                <div>
                    <h1 class="tb-app-title">Traceboard</h1>
                    <p class="tb-app-subtitle">
                        Evidence, contracts, and releases in one decision field.
                    </p>
                </div>
                <div class="tb-masthead-status">
                    <span class="tb-status-dot"></span>
                    <span>CONTROL ROOM</span>
                </div>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )

    active = render_navigation()

    return next(item for item in NAV_ITEMS if item.key == active)
