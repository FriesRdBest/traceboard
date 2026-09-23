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


def render_citation_card(
    title: str,
    source: str,
    url: str | None = None,
    snippet: str | None = None,
) -> None:
    """Render a citation card for evidence-backed claims."""
    with st.expander(title, expanded=False):
        st.markdown(f"**Source:** {source}")
        if url:
            st.markdown(f"[Link]({url})")
        if snippet:
            st.markdown(f"> {snippet}")


def render_empty_state(title: str, message: str | None = None) -> None:
    """Render an empty state panel."""
    st.info(title)
    if message:
        st.markdown(message)
