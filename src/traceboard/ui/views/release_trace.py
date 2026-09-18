from __future__ import annotations

import streamlit as st

from traceboard.ui.components import close_panel, panel, table
from traceboard.ui.views.common import RELEASES


def render() -> None:
    with st.container(border=False):
        panel(
            "Release trace",
            "Follow every change from decision to shipped surface.",
            elevation="raised",
        )
        table(("Version", "Scope", "State", "Released"), RELEASES)
        st.divider()
        st.caption(
            "Local demo data is deterministic. Persistence is intentionally deferred until the integration contract is approved."
        )
        close_panel()
