"""Traceboard Streamlit application entry point."""

from __future__ import annotations

import streamlit as st

from traceboard.ui.components import view_header
from traceboard.ui.navigation import NAV_ITEMS
from traceboard.ui.shell import configure_page, render_shell
from traceboard.ui.views.registry import VIEWS


configure_page()
item = render_shell()
view_header(item)
VIEWS[item.key]()
