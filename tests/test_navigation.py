from traceboard.ui.navigation import NAV_ITEMS


def test_traceboard_has_seven_navigation_surfaces():
    assert len(NAV_ITEMS) == 7
    assert {item.key for item in NAV_ITEMS} == {
        "workspace", "contribution_intake", "token_lab", "component_contract",
        "quality_gate", "odyssey", "release_trace",
    }
