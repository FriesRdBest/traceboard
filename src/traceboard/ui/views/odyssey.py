from __future__ import annotations

import streamlit as st

from traceboard.ui.components import close_panel, panel


def render() -> None:
    with st.container(border=False):
        panel(
            "The Odyssey 2026",
            "A narrative record of how governance becomes a product capability.",
            elevation="raised",
        )
        st.markdown("### The system under pressure")
        st.write(
            "Traceboard turns design-system work into an observable chain of decisions: contribution, contract, quality, and release."
        )
        st.markdown("### Operating principles")
        st.write(
            "Prefer evidence over preference. Prefer shared primitives over local fixes. Prefer a visible blocked state over a silent compromise."
        )
        close_panel()
