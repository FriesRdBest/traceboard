"""Workspace composition rendered as one controlled HTML block."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping


from traceboard.ui.components import render_trace_row
from traceboard.ui.views.common import RELEASES, SOURCES


def _esc(value: object) -> str:
    return html.escape(str(value))


def _badge(label: str, tone: str = "success") -> str:
    label_html = _esc(label)
    tone_html = _esc(tone)
    return '<span class="tb-badge" data-tone="' + tone_html + '">' + label_html + "</span>"


def _table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    header_html = "".join("<th>" + _esc(item) + "</th>" for item in headers)
    row_html = "".join(
        "<tr>" + "".join("<td>" + _esc(cell) + "</td>" for cell in row) + "</tr>" for row in rows
    )
    return (
        '<div class="tb-table-wrap"><table class="tb-table">'
        + "<thead><tr>"
        + header_html
        + "</tr></thead><tbody>"
        + row_html
        + "</tbody></table></div>"
    )


def _sources(items: Iterable[Mapping[str, str]]) -> str:
    source_html: list[str] = []

    for item in items:
        source_type = _esc(item.get("type", "SOURCE"))
        status = _badge(item.get("status", "UNVERIFIED"))
        title = _esc(item.get("title", "Untitled source"))
        excerpt = _esc(item.get("excerpt", ""))

        source_html.append(
            '<article class="tb-source">'
            '<div class="tb-source-meta">' + source_type + status + "</div>"
            '<div class="tb-source-title">' + title + "</div>"
            '<div class="tb-source-excerpt">' + excerpt + "</div>"
            "</article>"
        )

    return '<div class="tb-sources">' + "".join(source_html) + "</div>"


def _signal(label: str, value: str, detail: str, tone: str = "neutral") -> str:
    return (
        '<article class="tb-signal" data-tone="' + _esc(tone) + '">'
        '<div class="tb-label">' + _esc(label) + "</div>"
        '<div class="tb-signal-value">' + _esc(value) + "</div>"
        '<div class="tb-signal-detail">' + _esc(detail) + "</div>"
        "</article>"
    )


def render() -> None:
    active_work = _table(
        ("Work item", "Owner", "State"),
        (
            ("Citation source badge", "A. Chen", "Review"),
            ("Token naming audit", "M. Singh", "Ready"),
            ("Button contract", "J. Rivera", "Blocked"),
        ),
    )

    release_trace = _table(
        ("Version", "Scope", "State", "Date"),
        RELEASES,
    )

    workspace_html = (
        '<main class="tb-workspace">'
        '<header class="tb-workspace-head">'
        '<div class="tb-eyebrow">CONTROL ROOM</div>'
        '<h1 class="tb-workspace-title">Workspace</h1>'
        '<p class="tb-workspace-description">'
        "System posture and active decisions."
        "</p>"
        "</header>"
        '<section class="tb-signal-grid" aria-label="System signals">'
        + _signal(
            "Governance health",
            "92%",
            "Stable across active surfaces",
            "accent",
        )
        + _signal("Open contributions", "07", "Two require review")
        + _signal(
            "Release readiness",
            "Ready",
            "No blocking gate failures",
            "success",
        )
        + "</section>"
        '<section class="tb-workspace-trace" aria-label="Evidence trace">'
        + render_trace_row(
            "Evidence pulse",
            "Governance decision",
            "Release trace",
            "Active",
            tone="success",
        )
        + "</section>"
        '<section class="tb-decision-grid">'
        '<article class="tb-panel tb-panel--feature">'
        '<header class="tb-panel-head">'
        '<div class="tb-label">NEXT DECISIONS</div>'
        '<h2 class="tb-panel-title">Active work</h2>'
        '<p class="tb-panel-description">'
        "The decisions currently consuming review capacity."
        "</p>"
        "</header>"
        '<div class="tb-panel-body">' + active_work + "</div></article>"
        '<article class="tb-panel tb-panel--quiet">'
        '<header class="tb-panel-head">'
        '<div class="tb-label">SOURCE FIELD</div>'
        '<h2 class="tb-panel-title">Evidence pulse</h2>'
        '<p class="tb-panel-description">'
        "Recent evidence attached to governance decisions."
        "</p>"
        "</header>"
        '<div class="tb-panel-body">' + _sources(SOURCES) + "</div></article>"
        "</section>"
        '<article class="tb-panel tb-panel--release">'
        '<header class="tb-panel-head">'
        '<div class="tb-label">RECENT MOVEMENT</div>'
        '<h2 class="tb-panel-title">Release trace</h2>'
        '<p class="tb-panel-description">'
        "A short record of decisions that reached a shipped surface."
        "</p>"
        "</header>"
        '<div class="tb-panel-body">' + release_trace + "</div></article>"
        "</main>"
    )

    st.markdown(workspace_html, unsafe_allow_html=True)
