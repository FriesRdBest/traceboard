"""Global Traceboard shell."""

from __future__ import annotations

import streamlit as st

from traceboard.ui.design_system import get_css
from traceboard.ui.navigation import NAV_ITEMS, render_navigation


def configure_page() -> None:
    st.set_page_config(page_title="Traceboard", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)


def render_shell():
    st.markdown('<main class="traceboard-shell"><div class="traceboard-workspace">', unsafe_allow_html=True)
    st.markdown('<header class="traceboard-header"><div><div class="traceboard-kicker">DESIGN-SYSTEM GOVERNANCE</div><div class="traceboard-title">Traceboard</div><p class="traceboard-subtitle">A live control room for making, reviewing, and releasing design-system decisions under pressure.</p></div></header>', unsafe_allow_html=True)
    active = render_navigation()
    st.markdown("</div></main>", unsafe_allow_html=True)
    return next(item for item in NAV_ITEMS if item.key == active)
