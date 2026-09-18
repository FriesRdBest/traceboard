"""Traceboard visual system."""

from __future__ import annotations

CSS_TOKENS = r"""
:root {
  color-scheme: dark;
  --tb-canvas: #102f35;
  --tb-surface: #194950;
  --tb-surface-raised: #205860;
  --tb-text: #f4f8f7;
  --tb-text-2: rgba(244,248,247,.76);
  --tb-text-3: rgba(244,248,247,.54);
  --tb-accent: #b7edf0;
  --tb-accent-soft: rgba(183,237,240,.13);
  --tb-accent-line: rgba(183,237,240,.48);
  --tb-green: #9fe0b8;
  --tb-line: rgba(183,237,240,.18);
  --tb-line-soft: rgba(183,237,240,.10);
  --tb-radius: 8px;
  --tb-radius-small: 6px;
  --tb-ui: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --workspace-gutter: clamp(20px, 4vw, 64px);
  --canvas-bg: var(--tb-canvas);
  --space-4: 16px;
  --radius-panel: var(--tb-radius);
  --border-focus: var(--tb-accent);
  --elevation-panel: 0 1px 0 rgba(255,255,255,.05) inset;
  --st-gap: 0px;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  background: var(--tb-canvas);
  color: var(--tb-text);
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebar"] {
  display: none;
}

[data-testid="stAppViewContainer"] > .main {
  padding-top: 0;
}

[data-testid="stAppViewContainer"] > .main > .block-container {
  max-width: 1480px;
  padding: 28px var(--workspace-gutter) 72px;
}

[data-testid="stVerticalBlock"] {
  gap: var(--st-gap);
}

[data-testid="stHorizontalBlock"] {
  gap: 16px;
  align-items: stretch;
}

[data-testid="column"] {
  min-width: 0;
}

.tb-masthead {
  position: relative;
  margin: 4px 0 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid var(--tb-line-soft);
}

.tb-masthead-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--tb-text-3);
  font: 700 11px/1 var(--tb-ui);
  letter-spacing: .09em;
}

.tb-mark {
  display: grid;
  width: 25px;
  height: 25px;
  place-items: center;
  border: 1px solid var(--tb-line);
  border-radius: 50%;
  color: var(--tb-accent);
  font-size: 12px;
}

.tb-masthead-row {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  margin-top: 18px;
}

.tb-app-title {
  margin: 0;
  color: var(--tb-text);
  font: 620 clamp(38px, 5vw, 64px)/.95 var(--tb-ui);
  letter-spacing: -.065em;
}

.tb-app-subtitle {
  max-width: 650px;
  margin: 12px 0 0;
  color: var(--tb-text-2);
  font: 400 16px/1.45 var(--tb-ui);
}

.tb-masthead-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 4px;
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .1em;
}

.tb-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--tb-green);
  box-shadow: 0 0 0 4px rgba(159,224,184,.10);
}

.tb-nav-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 9px;
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .1em;
  text-transform: uppercase;
}

.tb-nav-rule {
  flex: 1;
  height: 1px;
  background: var(--tb-line-soft);
}

.tb-nav-count {
  color: rgba(244,248,247,.34);
}

.stButton > button {
  min-height: 42px;
  border: 1px solid var(--tb-line-soft);
  border-radius: var(--tb-radius-small);
  background: transparent;
  color: var(--tb-text-2);
  font: 650 12px/1.15 var(--tb-ui);
  transition: background .16s ease, border-color .16s ease,
    color .16s ease, transform .16s ease;
}

.stButton > button:hover {
  transform: translateY(-1px);
  border-color: var(--tb-accent-line);
  background: var(--tb-accent-soft);
  color: var(--tb-text);
}

.stButton > button[kind="primary"] {
  border-color: var(--tb-accent-line);
  background: var(--tb-accent-soft);
  color: var(--tb-text);
}

.tb-view-head {
  padding-top: 38px;
  padding-bottom: 8px;
}

.tb-eyebrow,
.tb-label {
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .1em;
  text-transform: uppercase;
}

.tb-view-title {
  margin: 10px 0 0;
  color: var(--tb-text);
  font: 620 clamp(30px, 3vw, 44px)/1.05 var(--tb-ui);
  letter-spacing: -.05em;
}

.tb-view-description {
  max-width: 700px;
  margin: 12px 0 0;
  color: var(--tb-text-2);
  font: 400 16px/1.45 var(--tb-ui);
}

.tb-signal,
.tb-panel {
  border: 1px solid var(--tb-line-soft);
  border-radius: var(--tb-radius);
  background: var(--tb-surface);
  box-shadow: 0 1px 0 rgba(255,255,255,.05) inset;
}

.tb-signal {
  display: grid;
  min-height: 118px;
  align-content: start;
  gap: 8px;
  padding: 18px;
}

.tb-signal[data-tone="accent"] {
  border-color: var(--tb-accent-line);
  background: var(--tb-surface-raised);
}

.tb-signal-value {
  color: var(--tb-text);
  font: 620 30px/1 var(--tb-ui);
  letter-spacing: -.05em;
}

.tb-signal-detail {
  color: var(--tb-text-2);
  font: 400 12px/1.4 var(--tb-ui);
}

.tb-panel {
  min-height: 0;
  padding: 20px;
}

.tb-panel[data-tone="feature"] {
  border-color: var(--tb-accent-line);
  background: var(--tb-surface-raised);
}

.tb-panel-head {
  margin-bottom: 18px;
}

.tb-panel-title {
  margin: 8px 0 0;
  color: var(--tb-text);
  font: 620 24px/1.08 var(--tb-ui);
  letter-spacing: -.04em;
}

.tb-panel-description {
  max-width: 640px;
  margin: 9px 0 0;
  color: var(--tb-text-2);
  font: 400 14px/1.45 var(--tb-ui);
}

.tb-table-wrap {
  overflow-x: auto;
}

.tb-table {
  width: 100%;
  border-collapse: collapse;
  font: 400 12px/1.4 var(--tb-ui);
}

.tb-table th {
  padding: 0 12px 10px 0;
  color: var(--tb-text-3);
  font-size: 10px;
  letter-spacing: .1em;
  text-align: left;
  text-transform: uppercase;
}

.tb-table td {
  padding: 12px 12px 12px 0;
  border-top: 1px solid var(--tb-line-soft);
  color: var(--tb-text-2);
}

.tb-table td:first-child {
  color: var(--tb-text);
}

.tb-sources {
  display: grid;
  gap: 12px;
}

.tb-source {
  display: grid;
  gap: 6px;
  padding-top: 12px;
  border-top: 1px solid var(--tb-line-soft);
}

.tb-source:first-child {
  padding-top: 0;
  border-top: 0;
}

.tb-source-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .06em;
  text-transform: uppercase;
}

.tb-source-title {
  color: var(--tb-text);
  font: 600 14px/1.35 var(--tb-ui);
}

.tb-source-excerpt {
  color: var(--tb-text-2);
  font: 400 12px/1.45 var(--tb-ui);
}

.tb-badge {
  display: inline-flex;
  align-items: center;
  min-height: 20px;
  padding: 0 8px;
  border: 1px solid var(--tb-line);
  border-radius: 999px;
  color: var(--tb-text-2);
  font: 700 10px/1 var(--tb-ui);
}

.tb-badge[data-tone="success"] {
  border-color: rgba(159,224,184,.40);
  background: rgba(159,224,184,.10);
  color: var(--tb-green);
}

.tb-workspace {
  display: grid;
  gap: 22px;
  margin-top: 24px;
}

.tb-workspace-head {
  display: grid;
  gap: 0;
  padding-bottom: 4px;
}

.tb-workspace-title {
  margin: 8px 0 0;
  color: var(--tb-text);
  font: 620 clamp(30px, 3vw, 44px)/1.05 var(--tb-ui);
  letter-spacing: -.05em;
}

.tb-workspace-description {
  margin: 12px 0 0;
  color: var(--tb-text-2);
  font: 400 16px/1.45 var(--tb-ui);
}

.tb-signal-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.tb-decision-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(320px, .7fr);
  gap: 16px;
}

.tb-panel--quiet,
.tb-panel--release {
  background: var(--tb-surface);
  box-shadow: none;
}

@media (max-width: 1000px) {
  .tb-masthead-row {
    align-items: start;
    flex-direction: column;
  }

  .tb-masthead-status {
    display: none;
  }

  .tb-signal-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .tb-decision-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  [data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 20px 16px 48px;
  }

  .tb-masthead {
    margin-bottom: 22px;
  }

  .tb-app-title {
    font-size: 42px;
  }

  .tb-signal-grid {
    grid-template-columns: 1fr;
  }
}
"""


def get_css() -> str:
    return CSS_TOKENS
