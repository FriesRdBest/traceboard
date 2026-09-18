from __future__ import annotations

import streamlit as st

from traceboard.ui.components import badge, close_panel, panel, table


def render() -> None:
    with st.container(border=False):
        panel(
            "Component contract",
            "A component is not approved until its behavior is explicit.",
            elevation="raised",
        )
        component = st.selectbox(
            "Component", ("Citation card", "Button", "Status badge", "Data table")
        )
        table(
            ("Contract area", "Requirement", "State"),
            (
                ("Anatomy", "Identity, evidence, metadata", "Defined"),
                ("Interaction", "Keyboard and pointer parity", "Defined"),
                ("Content", "Long titles wrap without clipping", "Required"),
                ("Accessibility", "Visible focus and semantic labels", "Required"),
            ),
        )
        st.markdown(f"Current contract: {badge(component, 'accent')}", unsafe_allow_html=True)
        close_panel()
