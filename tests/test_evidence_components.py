from __future__ import annotations

from traceboard.ui.components import (
    render_citation_card,
    render_empty_state,
    render_evidence_list,
    render_trace_row,
)


def test_render_citation_card_contains_source_and_excerpt():
    html = render_citation_card(
        "Design guidance",
        "Canonical source excerpt.",
        source_type="GUIDANCE",
        credibility="Verified",
        tone="success",
    )

    assert "Design guidance" in html
    assert "Canonical source excerpt." in html
    assert "GUIDANCE" in html
    assert "Verified" in html
    assert "tb-badge--success" in html


def test_render_trace_row_contains_the_full_lineage():
    html = render_trace_row(
        "Source",
        "Decision",
        "Outcome",
        "Ready",
        tone="info",
    )

    assert "Source" in html
    assert "Decision" in html
    assert "Outcome" in html
    assert "Ready" in html
    assert "tb-tone-info" in html


def test_render_empty_state_is_accessible():
    html = render_empty_state("No evidence", "Attach a source.")

    assert 'role="status"' in html
    assert "No evidence" in html
    assert "Attach a source." in html


def test_render_evidence_list_handles_empty_and_populated_states():
    empty = render_evidence_list([])
    populated = render_evidence_list(
        [
            {
                "title": "Repository record",
                "excerpt": "Reviewed implementation record.",
                "type": "RECORD",
                "status": "Reviewed",
                "tone": "success",
            }
        ]
    )

    assert "No evidence attached" in empty
    assert "Repository record" in populated
    assert "Reviewed" in populated
