"""Reusable Streamlit-rendered Traceboard components."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from traceboard.ui.navigation import NavItem


def _esc(value: object) -> str:
    return html.escape(str(value))


def panel(title: str, description: str | None = None, *, elevation: str = "panel") -> None:
    st.markdown(
        f'<section class="traceboard-panel" data-elevation="{_esc(elevation)}">'
        '<div class="traceboard-panel__header">'
        '<div><h2 class="traceboard-panel__title">'
        f"{_esc(title)}</h2>"
        + (f'<p class="traceboard-panel__description">{_esc(description)}</p>' if description else "")
        + "</div></div>",
        unsafe_allow_html=True,
    )


def close_panel() -> None:
    st.markdown("</section>", unsafe_allow_html=True)


def badge(label: str, tone: str = "neutral") -> str:
    return f'<span class="traceboard-badge" data-tone="{_esc(tone)}">{_esc(label)}</span>'


def stat(label: str, value: str, detail: str = "") -> None:
    st.markdown(
        '<div class="traceboard-stat">'
        f'<div class="traceboard-stat__label">{_esc(label)}</div>'
        f'<div class="traceboard-stat__value">{_esc(value)}</div>'
        f'<div class="traceboard-stat__detail">{_esc(detail)}</div>'
        "</div>",
        unsafe_allow_html=True,
    )


def table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> None:
    head = "".join(f"<th>{_esc(item)}</th>" for item in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{_esc(cell)}</td>" for cell in row) + "</tr>" for row in rows
    )
    st.markdown(
        f'<div style="overflow-x:auto"><table class="traceboard-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def citation_card(source: Mapping[str, str]) -> None:
    st.markdown(
        '<article class="citation-card">'
        f'<div class="citation-card__meta">{_esc(source.get("type", "SOURCE"))} · {_esc(source.get("status", "UNVERIFIED"))}</div>'
        f'<div class="citation-card__title">{_esc(source.get("title", "Untitled source"))}</div>'
        f'<div class="citation-card__excerpt">{_esc(source.get("excerpt", "No evidence excerpt supplied."))}</div>'
        "</article>",
        unsafe_allow_html=True,
    )


def view_header(item: NavItem) -> None:
    st.markdown(
        '<header class="traceboard-header">'
        '<div>'
        f'<div class="traceboard-kicker">{_esc(item.eyebrow)}</div>'
        f'<h1 class="traceboard-title">{_esc(item.label)}</h1>'
        f'<p class="traceboard-subtitle">{_esc(item.description)}</p>'
        "</div></header>",
        unsafe_allow_html=True,
    )
