"""Traceboard visual system."""

from __future__ import annotations

CSS_TOKENS = r"""
:root {
  color-scheme: dark;

  --tb-canvas: #1A6872;
  --tb-sidebar: #12525B;
  --tb-surface: #1F717A;
  --tb-surface-raised: #287D85;

  --tb-text: #F2FCFC;
  --tb-text-2: rgba(242, 252, 252, .76);
  --tb-text-3: rgba(242, 252, 252, .56);

  --tb-accent: #B8F0F0;
  --tb-accent-soft: rgba(184, 240, 240, .12);
  --tb-accent-line: rgba(184, 240, 240, .36);

  --tb-success: #A9E2B8;
  --tb-warning: #F2D38C;
  --tb-danger: #F2A8A8;

  --tb-line: rgba(184, 240, 240, .20);
  --tb-line-soft: rgba(184, 240, 240, .11);

  --tb-radius: 8px;
  --tb-radius-small: 5px;
  --tb-ui: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;

  --workspace-gutter: clamp(20px, 4vw, 64px);
  --canvas-bg: var(--tb-canvas);
  --space-4: 16px;
  --radius-panel: var(--tb-radius);
  --border-focus: var(--tb-accent);
  --elevation-panel: 0 1px 0 rgba(255, 255, 255, .06) inset;
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
[data-testid="stStatusWidget"] {
  display: none;
}

[data-testid="stAppViewContainer"] > .main {
  padding-top: 0;
}

[data-testid="stAppViewContainer"] > .main > .block-container {
  max-width: 1320px;
  padding: 30px var(--workspace-gutter) 72px;
}

[data-testid="stSidebar"] {
  display: block;
  background: var(--tb-sidebar);
  border-right: 1px solid var(--tb-line-soft);
}

[data-testid="stSidebar"] > div:first-child {
  padding: 28px 18px;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
  padding-top: 8px;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
  border-radius: var(--tb-radius-small);
  color: var(--tb-text-2);
  font: 600 12px/1.2 var(--tb-ui);
  letter-spacing: .01em;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
  background: var(--tb-accent-soft);
  color: var(--tb-text);
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
  background: var(--tb-accent-soft);
  box-shadow: inset 3px 0 0 var(--tb-accent);
  color: var(--tb-text);
}

.tb-masthead {
  margin: 0 0 34px;
  padding: 0 0 22px;
  border-bottom: 1px solid var(--tb-line-soft);
}

.tb-masthead-brand {
  display: flex;
  align-items: center;
  gap: 9px;
  color: var(--tb-text-3);
  font: 700 11px/1 var(--tb-ui);
  letter-spacing: .09em;
}

.tb-masthead-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
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

.tb-kicker {
  color: var(--tb-text);
}

.tb-brand-divider {
  color: var(--tb-text-3);
}

.tb-brand-context {
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .08em;
}

.tb-masthead-row {
  margin-top: 18px;
}

.tb-app-title {
  margin: 0;
  color: var(--tb-text);
  font: 650 clamp(34px, 4vw, 48px)/1 var(--tb-ui);
  letter-spacing: -.06em;
}

.tb-app-subtitle {
  max-width: 620px;
  margin: 9px 0 0;
  color: var(--tb-text-2);
  font: 400 14px/1.45 var(--tb-ui);
}

.tb-masthead-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--tb-text-3);
  font: 700 10px/1 var(--tb-ui);
  letter-spacing: .1em;
}

.tb-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--tb-success);
  box-shadow: 0 0 0 4px rgba(169, 226, 184, .11);
}

.tb-status-value {
  color: var(--tb-text-2);
  font-variant-numeric: tabular-nums;
}

.tb-view-head {
  padding: 0 0 18px;
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
  font: 650 clamp(30px, 3vw, 42px)/1.05 var(--tb-ui);
  letter-spacing: -.05em;
}

.tb-view-description {
  max-width: 700px;
  margin: 10px 0 0;
  color: var(--tb-text-2);
  font: 400 14px/1.5 var(--tb-ui);
}

.tb-workspace {
  display: grid;
  gap: 20px;
  margin-top: 4px;
}

.tb-signal-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.tb-decision-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(300px, .7fr);
  gap: 16px;
}

.tb-signal-grid,
.tb-decision-grid {
  width: 100%;
  box-sizing: border-box;
}

.tb-signal,
.tb-panel {
  box-sizing: border-box;
  width: 100%;
}


.tb-signal,
.tb-panel {
  border: 1px solid var(--tb-line-soft);
  border-radius: var(--tb-radius);
  background: var(--tb-surface);
  box-shadow: var(--elevation-panel);
}

.tb-signal {
  display: grid;
  min-height: 118px;
  align-content: start;
  gap: 9px;
  padding: 20px;
}

.tb-signal[data-tone="accent"] {
  border-color: var(--tb-accent-line);
  background: var(--tb-surface-raised);
}

.tb-signal-value {
  color: var(--tb-text);
  font: 650 31px/1 var(--tb-ui);
  letter-spacing: -.05em;
}

.tb-signal-detail {
  color: var(--tb-text-2);
  font: 400 13px/1.45 var(--tb-ui);
}

.tb-panel {
  min-height: 0;
  padding: 22px;
}

.tb-panel[data-tone="feature"] {
  border-color: var(--tb-accent-line);
  background: var(--tb-surface-raised);
}

.tb-panel-head {
  margin-bottom: 20px;
}

.tb-panel-title {
  margin: 9px 0 0;
  color: var(--tb-text);
  font: 650 24px/1.1 var(--tb-ui);
  letter-spacing: -.04em;
}

.tb-panel-description {
  max-width: 660px;
  margin: 10px 0 0;
  color: var(--tb-text-2);
  font: 400 13px/1.5 var(--tb-ui);
}

.tb-table-wrap {
  overflow-x: auto;
}

.tb-table {
  width: 100%;
  border-collapse: collapse;
  font: 400 12px/1.45 var(--tb-ui);
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
  gap: 14px;
}

.tb-source {
  display: grid;
  gap: 7px;
  padding-top: 14px;
  border-top: 1px solid var(--tb-line-soft);
}

.tb-source:first-child {
  padding-top: 0;
  border-top: 0;
}

.tb-source-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
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
  border-color: rgba(169, 226, 184, .45);
  background: rgba(169, 226, 184, .12);
  color: var(--tb-success);
}

.tb-badge[data-tone="warning"] {
  border-color: rgba(242, 211, 140, .45);
  background: rgba(242, 211, 140, .12);
  color: var(--tb-warning);
}

.tb-badge[data-tone="danger"] {
  border-color: rgba(242, 168, 168, .45);
  background: rgba(242, 168, 168, .12);
  color: var(--tb-danger);
}

.stButton > button,
.stTextInput input,
.stTextArea textarea,
.stSelectbox [data-baseweb="select"] > div {
  border-radius: var(--tb-radius-small);
}

.stButton > button {
  border-color: var(--tb-line-soft);
  color: var(--tb-text-2);
}

.stButton > button:hover {
  border-color: var(--tb-accent-line);
  background: var(--tb-accent-soft);
  color: var(--tb-text);
}

@media (max-width: 1000px) {
  .tb-masthead-top {
    align-items: flex-start;
    flex-direction: column;
  }

  .tb-signal-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .tb-decision-grid {
    grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
  }
}

@media (max-width: 620px) {
  [data-testid="stAppViewContainer"] > .main > .block-container {
    padding: 20px 16px 48px;
  }

  .tb-masthead {
    margin-bottom: 24px;
  }

  .tb-panel,
  .tb-signal {
    padding: 16px;
  }

  .tb-view-title {
    font-size: 32px;
  }
}


/* Sidebar rhythm and navigation spacing. */

[data-testid="stSidebar"] {
  min-width: 248px;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 34px 20px 28px;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
  margin-top: 18px;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {
  display: grid;
  gap: 7px;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
  margin: 0;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
  min-height: 38px;
  padding: 9px 12px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  border-left: 3px solid transparent;
  font-size: 13px;
  line-height: 1.2;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
  border-left-color: var(--tb-accent);
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a p {
  margin: 0;
}

@media (max-width: 850px) {
  [data-testid="stSidebar"] {
    min-width: 220px;
  }

  [data-testid="stSidebar"] > div:first-child {
    padding: 28px 16px 24px;
  }
}



/* Shared content geometry. */

[data-testid="stAppViewContainer"] > .main > .block-container {
  width: min(100% - 2 * var(--workspace-gutter), 1240px);
  max-width: 1240px;
  margin: 0 auto;
  box-sizing: border-box;
}

.tb-view-head {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 0 20px;
  box-sizing: border-box;
}

.tb-workspace {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  gap: 24px;
  box-sizing: border-box;
}

.tb-signal-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: stretch;
  gap: 16px;
  width: 100%;
}

.tb-decision-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
  align-items: start;
  gap: 16px;
  width: 100%;
}

.tb-signal,
.tb-panel {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.tb-signal {
  min-height: 132px;
}

.tb-panel {
  padding: 20px;
}

.tb-panel-head {
  min-height: 84px;
  margin-bottom: 18px;
}

.tb-panel-title {
  line-height: 1.12;
}

.tb-panel-description {
  max-width: 58ch;
}

.tb-table-wrap {
  width: 100%;
  overflow-x: auto;
}

.tb-table {
  min-width: 520px;
}

.tb-source-excerpt {
  max-width: 42ch;
}

@media (max-width: 1000px) {
  [data-testid="stAppViewContainer"] > .main > .block-container {
    width: min(100% - 40px, 900px);
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
    width: 100%;
    padding: 22px 16px 48px;
  }

  .tb-view-head,
  .tb-workspace {
    width: 100%;
  }

  .tb-signal-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .tb-decision-grid {
    gap: 12px;
  }

  .tb-signal {
    min-height: 112px;
  }

  .tb-panel {
    padding: 16px;
  }

  .tb-panel-head {
    min-height: 0;
    margin-bottom: 16px;
  }

  .tb-panel-title {
    font-size: 22px;
  }

  .tb-panel-description {
    max-width: none;
  }
}



.tb-legacy-context {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto 24px;
  padding: 0 0 20px;
  border-bottom: 1px solid var(--tb-line-soft);
  box-sizing: border-box;
}

.tb-legacy-context .tb-view-title {
  margin-top: 9px;
}

.tb-legacy-context .tb-panel-description {
  margin-top: 9px;
}

"""


def get_css() -> str:
    return CSS_TOKENS
