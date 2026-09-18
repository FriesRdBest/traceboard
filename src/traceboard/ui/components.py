"""Shared Traceboard UI components."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from traceboard.ui.navigation import NavItem


def esc(value: object) -> str:
    return html.escape(str(value))


def markup(value: str) -> None:
    st.markdown(value, unsafe_allow_html=True)


def badge(label: str, tone: str = "neutral") -> str:
    return f'<span class="tb-badge" data-tone="{esc(tone)}">{esc(label)}</span>'


def render_status(label: str, tone: str = "neutral") -> None:
    markup(badge(label, tone))


def render_view_header(item: NavItem) -> None:
    markup(
        '<header class="tb-view-head">'
        f'<div class="tb-eyebrow">{esc(item.eyebrow)}</div>'
        f'<h1 class="tb-view-title">{esc(item.label)}</h1>'
        f'<p class="tb-view-description">{esc(item.description)}</p>'
        "</header>"
    )


def render_signal(
    label: str,
    value: str,
    detail: str,
    tone: str = "neutral",
) -> None:
    markup(
        f'<article class="tb-signal" data-tone="{esc(tone)}">'
        f'<div class="tb-label">{esc(label)}</div>'
        f'<div class="tb-signal-value">{esc(value)}</div>'
        f'<div class="tb-signal-detail">{esc(detail)}</div>'
        "</article>"
    )


def render_panel(
    label: str,
    title: str,
    description: str,
    body: str,
    *,
    tone: str = "neutral",
) -> None:
    markup(
        f'<article class="tb-panel" data-tone="{esc(tone)}">'
        '<header class="tb-panel-head">'
        f'<div class="tb-label">{esc(label)}</div>'
        f'<h2 class="tb-panel-title">{esc(title)}</h2>'
        f'<p class="tb-panel-description">{esc(description)}</p>'
        "</header>"
        f'<div class="tb-panel-body">{body}</div>'
        "</article>"
    )


def render_decision_row(
    evidence: str,
    decision: str,
    contract: str,
    state: str,
    tone: str = "neutral",
) -> str:
    return (
        '<div class="tb-decision-row">'
        f'<div class="tb-decision-evidence">{esc(evidence)}</div>'
        f'<div class="tb-decision-main">{esc(decision)}</div>'
        f'<div class="tb-decision-contract">{esc(contract)}</div>'
        f'<div class="tb-decision-state">{badge(state, tone)}</div>'
        "</div>"
    )


def table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    header_markup = "".join(f"<th>{esc(item)}</th>" for item in headers)
    row_markup = "".join(
        "<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        '<div class="tb-table-wrap"><table class="tb-table">'
        f"<thead><tr>{header_markup}</tr></thead>"
        f"<tbody>{row_markup}</tbody></table></div>"
    )


def sources(sources_data: Iterable[Mapping[str, str]]) -> str:
    items: list[str] = []
    for source in sources_data:
        items.append(
            '<div class="tb-source">'
            '<div class="tb-source-meta">'
            f"{esc(source.get('type', 'SOURCE'))}"
            f"{badge(source.get('status', 'UNVERIFIED'), 'success')}"
            "</div>"
            f'<div class="tb-source-title">{esc(source.get("title", "Untitled source"))}</div>'
            f'<div class="tb-source-excerpt">{esc(source.get("excerpt", ""))}</div>'
            "</div>"
        )
    return f'<div class="tb-sources">{"".join(items)}</div>'


def render_theme_toggle() -> None:
    """Compatibility hook retained for host integration."""
    return None


def close_panel() -> None:
    """Compatibility no-op for legacy views."""
    return None


def panel(
    title: str,
    description: str | None = None,
    *,
    elevation: str = "panel",
) -> None:
    """Compatibility opener for legacy views.

    The legacy API remains available, but page context is intentionally
    quieter than a data panel.
    """
    description_markup = (
        f'<p class="tb-panel-description">{esc(description)}</p>' if description else ""
    )
    markup(
        f'<section class="tb-legacy-context" data-tone="{esc(elevation)}">'
        '<div class="tb-label">TRACEBOARD</div>'
        f'<h1 class="tb-view-title">{esc(title)}</h1>'
        f"{description_markup}"
        "</section>"
    )
