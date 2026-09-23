from __future__ import annotations

from datetime import UTC, datetime


def today_label() -> str:
    """Return today's date as an ISO string."""
    return datetime.now(tz=UTC).date().isoformat()


def format_percentage(value: float) -> str:
    """Format a 0-1 value as a percentage string."""
    return f"{value:.1%}"
