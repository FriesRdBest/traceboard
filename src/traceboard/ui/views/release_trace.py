from __future__ import annotations

import streamlit as st

from traceboard.ui.components import (
    close_panel,
    panel,
    render_evidence_list,
    render_trace_row,
    table,
)
from traceboard.ui.views.common import RELEASES


def render() -> None:
    with st.container(border=False):
        panel(
            "Release trace",
            "Follow every change from decision to shipped surface.",
            elevation="raised",
        )
        table(("Version", "Scope", "State", "Released"), RELEASES)
        st.markdown(
            render_trace_row(
                "Approved contribution",
                "Quality gate",
                "Release surface",
                "Traceable",
                tone="success",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            render_evidence_list(
                [
                    {
                        "type": "RECORD",
                        "status": "Reviewed",
                        "title": "Release decision record",
                        "excerpt": "The release surface is linked to an approved contribution and quality evaluation.",
                        "tone": "success",
                    },
                    {
                        "type": "GUIDANCE",
                        "status": "Verified",
                        "title": "System Story evidence",
                        "excerpt": "The visible narrative remains grounded in the same traceable system record.",
                        "tone": "info",
                    },
                ]
            ),
            unsafe_allow_html=True,
        )
        st.divider()
        st.caption(
            "Local demo data is deterministic. Persistence is intentionally deferred until the integration contract is approved."
        )
        close_panel()
