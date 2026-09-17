from __future__ import annotations

import streamlit as st

from traceboard.ui.layout import configure_page, render_app_shell
from traceboard.ui.views.component_contract import render_component_contract
from traceboard.ui.views.contribution_intake import render_contribution_intake
from traceboard.ui.views.quality_gate import render_quality_gate
from traceboard.ui.views.release_trace import render_release_trace
from traceboard.ui.views.system_map import render_system_map
from traceboard.ui.views.token_lab import render_token_lab
from traceboard.ui.views.workspace import render_workspace

configure_page()

navigation = st.navigation(
    [
        st.Page(render_workspace, title="Workspace", icon=":material/dashboard:"),
        st.Page(
            render_contribution_intake,
            title="Contribution Intake",
            icon=":material/assignment:",
        ),
        st.Page(render_token_lab, title="Token Lab", icon=":material/palette:"),
        st.Page(
            render_component_contract,
            title="Component Contract",
            icon=":material/account_tree:",
        ),
        st.Page(render_quality_gate, title="Quality Gate", icon=":material/verified:"),
        st.Page(render_release_trace, title="Release Trace", icon=":material/history:"),
        st.Page(render_system_map, title="System Map", icon=":material/schema:"),
    ]
)

render_app_shell()
navigation.run()
