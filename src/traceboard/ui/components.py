from __future__ import annotations

from typing import Any

import streamlit as st


def render_theme_toggle() -> None:
    """Compatibility hook retained for host integration."""
    return


def close_panel() -> None:
    """Compatibility no-op for legacy views."""
    return


def render_header(title: str, subtitle: str | None = None) -> None:
    """Render a standard header block."""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(subtitle)


def render_metric_card(label: str, value: Any, delta: str | None = None) -> None:
    """Render a simple metric card."""
    if delta:
        st.metric(label=label, value=value, delta=delta)
    else:
        st.metric(label=label, value=value)
