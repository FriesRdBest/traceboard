from traceboard.ui.design_system import get_css


def test_design_system_contains_required_primitives():
    css = get_css()
    for token in ("--canvas-bg", "--workspace-gutter", "--space-4", "--radius-panel", "--border-focus", "--elevation-panel"):
        assert token in css
