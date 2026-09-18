from __future__ import annotations

from traceboard.ui.views import (
    component_contract,
    contribution_intake,
    odyssey,
    quality_gate,
    release_trace,
    token_lab,
    workspace,
)

VIEWS = {
    "workspace": workspace.render,
    "contribution_intake": contribution_intake.render,
    "token_lab": token_lab.render,
    "component_contract": component_contract.render,
    "quality_gate": quality_gate.render,
    "odyssey": odyssey.render,
    "release_trace": release_trace.render,
}
