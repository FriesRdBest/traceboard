from __future__ import annotations

import streamlit as st

from traceboard.ui.components import badge, close_panel, panel, table


def render() -> None:
    with st.container(border=False):
        panel("Quality gate", "Blocking conditions remain visible until evidence closes them.", elevation="raised")
        table(("Gate", "Owner", "Result", "Evidence"), (("Token compliance", "Design systems", "Pass", "Token inventory"), ("Responsive behavior", "Frontend", "Review", "Viewport matrix"), ("Keyboard access", "Accessibility", "Pass", "Focus audit"), ("Content resilience", "Product", "Blocked", "Long-source fixture")))
        st.markdown(f"Overall status: {badge('Review required', 'warning')}", unsafe_allow_html=True)
        close_panel()
