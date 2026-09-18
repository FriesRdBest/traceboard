"""Navigation model for Traceboard's seven workflow surfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NavItem:
    key: str
    label: str
    eyebrow: str
    description: str


NAV_ITEMS = (
    NavItem("workspace", "Workspace", "CONTROL ROOM", "System-wide governance posture and active work."),
    NavItem("contribution_intake", "Contribution Intake", "INTAKE", "Capture a proposed contribution with its evidence."),
    NavItem("token_lab", "Token Lab", "TOKENS", "Inspect the shared decision primitives."),
    NavItem("component_contract", "Component Contract", "CONTRACT", "Define behavior, anatomy, and required states."),
    NavItem("quality_gate", "Quality Gate", "QUALITY", "Review implementation readiness and blocking conditions."),
    NavItem("odyssey", "The Odyssey 2026", "NARRATIVE", "Trace the design-system operating story."),
    NavItem("release_trace", "Release Trace", "RELEASE", "Follow changes from decision through release."),
)


def get_active_key(default: str = "workspace") -> str:
    import streamlit as st

    current = st.session_state.get("traceboard_view", default)
    keys = {item.key for item in NAV_ITEMS}
    return current if current in keys else default


def render_navigation() -> str:
    import streamlit as st

    active = get_active_key()
    cols = st.columns(len(NAV_ITEMS), gap="small")
    for col, item in zip(cols, NAV_ITEMS):
        with col:
            if st.button(
                item.label,
                key=f"nav_{item.key}",
                use_container_width=True,
                type="primary" if item.key == active else "secondary",
            ):
                st.session_state.traceboard_view = item.key
                st.rerun()
    return active
