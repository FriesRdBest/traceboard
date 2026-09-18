"""Shared deterministic demo data for the initial Traceboard build."""

from __future__ import annotations

from datetime import date

SOURCES = [
    {
        "type": "PRIMARY",
        "status": "VERIFIED",
        "title": "Perplexity Design System",
        "excerpt": "Canonical guidance for interface structure, typography, and product behavior.",
    },
    {
        "type": "RECORD",
        "status": "REVIEWED",
        "title": "Traceboard decision log",
        "excerpt": "The current governance record for token and component changes.",
    },
]

RELEASES = [
    ("v0.4.0", "Design-system shell", "Approved", "2026-09-18"),
    ("v0.3.0", "Quality gate model", "Approved", "2026-09-16"),
    ("v0.2.0", "Contribution intake", "Released", "2026-09-12"),
]


def today_label() -> str:
    return date.today().isoformat()
