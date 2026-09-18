"""Traceboard application entry point."""

from __future__ import annotations

from traceboard.ui.shell import configure_page, render_shell
from traceboard.ui.views.registry import VIEWS

configure_page()
item = render_shell()
VIEWS[item.key]()
