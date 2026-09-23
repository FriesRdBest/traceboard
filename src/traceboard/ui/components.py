from __future__ import annotations

from collections.abc import Iterable
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


def render_evidence_list(items: Iterable[dict[str, Any]]) -> None:
    """Render a simple list of evidence items."""
    for item in items:
        label = item.get("label", "Evidence")
        value = item.get("value", "")
        st.markdown(f"**{label}:** {value}")


def render_trace_row(token_name: str, usages: list[dict[str, Any]]) -> None:
    """Render a single token trace row in a table-like layout."""
    with st.expander(token_name, expanded=False):
        for usage in usages:
            file_path = usage.get("file_path", usage.get("path", ""))
            line = usage.get("line", "")
            value = usage.get("value", "")
            parts = [p for p in [file_path, line, value] if p]
            st.markdown(" • ".join(str(p) for p in parts))
