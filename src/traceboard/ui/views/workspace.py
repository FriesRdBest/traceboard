from __future__ import annotations

import streamlit as st

from traceboard.ui.components import badge, close_panel, panel, stat, table
from traceboard.ui.views.common import RELEASES, SOURCES


def render() -> None:
    st.markdown('<div class="traceboard-grid traceboard-grid--3">', unsafe_allow_html=True)
    for label, value, detail in (("Governance health", "92%", "Stable across active surfaces"), ("Open contributions", "07", "Two require review"), ("Release readiness", "Ready", "No blocking gate failures")):
        with st.container(border=False):
            panel(label)
            stat(label, value, detail)
            close_panel()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="traceboard-grid traceboard-grid--2" style="margin-top:16px">', unsafe_allow_html=True)
    with st.container(border=False):
        panel("Active work", "The decisions currently consuming review capacity.", elevation="raised")
        table(("Work item", "Owner", "State"), (("Citation source badge", "A. Chen", "Review"), ("Token naming audit", "M. Singh", "Ready"), ("Button contract", "J. Rivera", "Blocked")))
        close_panel()
    with st.container(border=False):
        panel("Evidence pulse", "Recent evidence attached to governance decisions.")
        for source in SOURCES:
            st.markdown(f"- {source['title']} · {badge(source['status'], 'success')}", unsafe_allow_html=True)
        close_panel()
    st.markdown('</div>', unsafe_allow_html=True)
    with st.container(border=False):
        panel("Release trace", "Recent releases and the decisions behind them.")
        table(("Version", "Scope", "State", "Date"), RELEASES)
        close_panel()
