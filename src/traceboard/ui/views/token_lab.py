from __future__ import annotations

import streamlit as st

from traceboard.ui.components import close_panel, panel, table


def render() -> None:
    with st.container(border=False):
        panel(
            "Token inventory",
            "Inspect the primitives that prevent local visual improvisation.",
            elevation="raised",
        )
        table(
            ("Token", "Value", "Role"),
            (
                ("--canvas-bg", "#0A2528", "Primary canvas"),
                ("--accent-cyan", "#00E5FF", "Interaction and focus"),
                ("--space-4", "16px", "Base content gap"),
                ("--radius-panel", "12px", "Evidence surface"),
                ("--border-subtle", "10% white", "Quiet boundary"),
            ),
        )
        st.markdown("### Token preview")
        st.caption("A controlled preview of surface and elevation relationships.")

        a, b, c = st.columns(3)
        for col, name, color in (
            (a, "Canvas", "#0A2528"),
            (b, "Panel", "#103438"),
            (c, "Raised", "#143D40"),
        ):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        height:96px;
                        border-radius:8px;
                        border:1px solid rgba(214,232,229,.16);
                        background:{color};
                        display:flex;
                        align-items:flex-end;
                        padding:12px;
                        font-size:12px;
                    ">{name}</div>
                    """,
                    unsafe_allow_html=True,
                )
        close_panel()
