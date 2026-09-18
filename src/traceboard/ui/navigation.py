"""Traceboard application navigation."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class NavItem:
    key: str
    label: str
    eyebrow: str
    description: str


NAV_ITEMS = (
    NavItem("workspace", "Workspace", "CONTROL ROOM", "System posture and active decisions."),
    NavItem(
        "contribution_intake", "Contribution Intake", "INTAKE", "Open a new door with evidence."
    ),
    NavItem("token_lab", "Token Lab", "TOKENS", "Inspect the primitives behind decisions."),
    NavItem(
        "component_contract",
        "Component Contract",
        "CONTRACT",
        "Define behavior before implementation.",
    ),
    NavItem("quality_gate", "Quality Gate", "QUALITY", "Make readiness and blockers explicit."),
    NavItem(
        "odyssey", "The Odyssey 2026", "SYSTEM STORY", "Follow the ideas that changed the system."
    ),
    NavItem("release_trace", "Release Trace", "RELEASE", "Connect decisions to shipped surfaces."),
)


DISPLAY_LABELS = {
    "workspace": "Workspace",
    "contribution_intake": "Intake",
    "token_lab": "Tokens",
    "component_contract": "Contracts",
    "quality_gate": "Quality",
    "odyssey": "Story",
    "release_trace": "Release",
}


def get_active_key(default: str = "workspace") -> str:
    active = st.session_state.get("traceboard_view", default)
    keys = {item.key for item in NAV_ITEMS}
    return active if active in keys else default


def render_navigation() -> str:
    active = get_active_key()

    with st.sidebar:
        st.markdown(
            """
            <div class="tb-sidebar-brand">
              <span class="tb-mark">◈</span>
              <div>
                <div class="tb-sidebar-name">TRACEBOARD</div>
                <div class="tb-sidebar-context">Governance console</div>
              </div>
            </div>
            <div class="tb-sidebar-heading">
              <span>Governance surfaces</span>
              <span>07</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for item in NAV_ITEMS:
            display_label = DISPLAY_LABELS[item.key]
            is_active = item.key == active

            if st.button(
                display_label,
                key=f"nav_{item.key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=f"{item.label}: {item.description}",
            ):
                st.session_state.traceboard_view = item.key
                st.rerun()

    return active
