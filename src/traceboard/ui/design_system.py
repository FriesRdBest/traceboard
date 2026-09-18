"""Traceboard design-system tokens and CSS generation."""

from __future__ import annotations

CSS_TOKENS = r"""
:root {
  --canvas-bg: #0a2528;
  --canvas-bg-raised: #0d2d30;
  --surface-1: #103438;
  --surface-2: #143d40;
  --surface-inset: #082023;
  --accent-cyan: #00e5ff;
  --accent-cyan-soft: rgba(0, 229, 255, 0.14);
  --text-primary: #f3f7f5;
  --text-secondary: rgba(243, 247, 245, 0.72);
  --text-tertiary: rgba(243, 247, 245, 0.50);
  --text-disabled: rgba(243, 247, 245, 0.32);
  --success: #8ee6b2;
  --warning: #f5c77a;
  --danger: #ff8d8d;
  --workspace-max: 1600px;
  --workspace-gutter: clamp(16px, 2.4vw, 40px);
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 32px;
  --space-8: 40px;
  --space-9: 48px;
  --space-10: 64px;
  --panel-padding: clamp(16px, 1.8vw, 28px);
  --radius-control: 8px;
  --radius-panel: 12px;
  --radius-emphasis: 16px;
  --radius-pill: 999px;
  --border-subtle: rgba(214, 232, 229, 0.10);
  --border-default: rgba(214, 232, 229, 0.16);
  --border-strong: rgba(214, 232, 229, 0.28);
  --border-focus: #00e5ff;
  --elevation-panel: 0 1px 0 rgba(255,255,255,.035) inset, 0 8px 24px rgba(0,0,0,.12);
  --elevation-raised: 0 1px 0 rgba(255,255,255,.05) inset, 0 12px 32px rgba(0,0,0,.18);
  --elevation-floating: 0 1px 0 rgba(255,255,255,.07) inset, 0 20px 48px rgba(0,0,0,.26);
  --font-ui: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-answer: Georgia, "Times New Roman", serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --text-xs: 11px;
  --text-sm: 12px;
  --text-md: 14px;
  --text-lg: 16px;
  --text-xl: 20px;
  --text-display: clamp(24px, 2.2vw, 36px);
  --leading-tight: 1.15;
  --leading-body: 1.5;
  --leading-dense: 1.35;
  --tracking-label: .04em;
}

html, body, [data-testid="stAppViewContainer"] { background: var(--canvas-bg); color: var(--text-primary); }
[data-testid="stAppViewContainer"] > .main { background: var(--canvas-bg); }
.block-container { max-width: var(--workspace-max); padding: 24px var(--workspace-gutter) 48px; }
.traceboard-shell { min-height: 100dvh; }
.traceboard-workspace { width: min(100%, var(--workspace-max)); margin: 0 auto; }
.traceboard-header { display:flex; justify-content:space-between; align-items:flex-end; gap:24px; margin-bottom:24px; }
.traceboard-kicker { color:var(--text-tertiary); font:600 var(--text-xs)/var(--leading-tight) var(--font-ui); letter-spacing:var(--tracking-label); text-transform:uppercase; }
.traceboard-title { margin:4px 0 0; color:var(--text-primary); font:500 var(--text-display)/var(--leading-tight) var(--font-ui); letter-spacing:-.025em; }
.traceboard-subtitle { max-width:720px; margin:8px 0 0; color:var(--text-secondary); font:400 var(--text-md)/var(--leading-body) var(--font-ui); }
.traceboard-tabs { display:flex; gap:4px; overflow-x:auto; scrollbar-width:none; padding:4px; margin-bottom:24px; border:1px solid var(--border-subtle); border-radius:var(--radius-panel); background:var(--surface-inset); }
.traceboard-tabs::-webkit-scrollbar { display:none; }
.traceboard-tab { flex:0 0 auto; min-height:44px; padding:0 12px; border:0; border-radius:var(--radius-control); background:transparent; color:var(--text-tertiary); font:500 var(--text-sm)/var(--leading-tight) var(--font-ui); letter-spacing:var(--tracking-label); }
.traceboard-tab:hover { color:var(--text-primary); background:rgba(255,255,255,.035); }
.traceboard-tab[aria-selected="true"] { color:var(--text-primary); background:var(--surface-2); box-shadow:0 1px 0 rgba(255,255,255,.06) inset, 0 2px 8px rgba(0,0,0,.14); }
.traceboard-tab:focus-visible, button:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible { outline:2px solid var(--border-focus); outline-offset:2px; }
.traceboard-grid { display:grid; gap:var(--space-4); }
.traceboard-grid--2 { grid-template-columns:repeat(2,minmax(0,1fr)); }
.traceboard-grid--3 { grid-template-columns:repeat(3,minmax(0,1fr)); }
.traceboard-panel { padding:var(--panel-padding); border:1px solid var(--border-subtle); border-radius:var(--radius-panel); background:var(--surface-1); box-shadow:var(--elevation-panel); }
.traceboard-panel[data-elevation="raised"] { border-color:var(--border-default); box-shadow:var(--elevation-raised); }
.traceboard-panel[data-elevation="floating"] { border-color:var(--border-strong); box-shadow:var(--elevation-floating); }
.traceboard-panel__header { display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:var(--space-5); }
.traceboard-panel__title { margin:0; color:var(--text-primary); font:600 var(--text-lg)/var(--leading-tight) var(--font-ui); }
.traceboard-panel__description { margin:6px 0 0; color:var(--text-tertiary); font:400 var(--text-sm)/var(--leading-body) var(--font-ui); }
.traceboard-stat { display:grid; gap:8px; min-width:0; }
.traceboard-stat__label { color:var(--text-tertiary); font:600 var(--text-xs)/var(--leading-tight) var(--font-ui); letter-spacing:var(--tracking-label); text-transform:uppercase; }
.traceboard-stat__value { color:var(--text-primary); font:500 28px/1 var(--font-ui); letter-spacing:-.025em; }
.traceboard-stat__detail { color:var(--text-secondary); font:400 var(--text-sm)/var(--leading-body) var(--font-ui); }
.traceboard-badge { display:inline-flex; align-items:center; min-height:24px; padding:0 8px; border:1px solid var(--border-default); border-radius:var(--radius-pill); color:var(--text-secondary); font:600 var(--text-xs)/1 var(--font-ui); letter-spacing:.02em; }
.traceboard-badge[data-tone="success"] { color:var(--success); border-color:rgba(142,230,178,.28); background:rgba(142,230,178,.08); }
.traceboard-badge[data-tone="warning"] { color:var(--warning); border-color:rgba(245,199,122,.28); background:rgba(245,199,122,.08); }
.traceboard-badge[data-tone="danger"] { color:var(--danger); border-color:rgba(255,141,141,.28); background:rgba(255,141,141,.08); }
.traceboard-badge[data-tone="accent"] { color:var(--accent-cyan); border-color:rgba(0,229,255,.28); background:var(--accent-cyan-soft); }
.traceboard-table { width:100%; border-collapse:collapse; font:400 var(--text-sm)/var(--leading-dense) var(--font-ui); }
.traceboard-table th { padding:0 12px 10px 0; color:var(--text-tertiary); font-size:var(--text-xs); letter-spacing:var(--tracking-label); text-align:left; text-transform:uppercase; }
.traceboard-table td { padding:12px 12px 12px 0; border-top:1px solid var(--border-subtle); color:var(--text-secondary); vertical-align:top; }
.traceboard-table td:first-child { color:var(--text-primary); }
.citation-card { display:grid; gap:8px; padding:16px; border:1px solid var(--border-subtle); border-radius:var(--radius-control); background:var(--surface-inset); }
.citation-card__meta { display:flex; flex-wrap:wrap; align-items:center; gap:8px; color:var(--text-tertiary); font:600 var(--text-xs)/var(--leading-tight) var(--font-ui); letter-spacing:var(--tracking-label); text-transform:uppercase; }
.citation-card__title { color:var(--text-primary); font:400 var(--text-lg)/var(--leading-body) var(--font-answer); }
.citation-card__excerpt { color:var(--text-secondary); font:400 var(--text-sm)/var(--leading-body) var(--font-ui); }
.traceboard-code { color:var(--accent-cyan); font:400 var(--text-sm)/var(--leading-dense) var(--font-mono); }
.traceboard-muted { color:var(--text-tertiary); }
@media (max-width:900px) { .traceboard-header { align-items:flex-start; flex-direction:column; } .traceboard-grid--3 { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:640px) { .block-container { padding-inline:16px; } .traceboard-grid--2, .traceboard-grid--3 { grid-template-columns:1fr; } .traceboard-panel { padding:16px; } }
@media (prefers-reduced-motion:reduce) { *, *::before, *::after { scroll-behavior:auto !important; transition-duration:.01ms !important; animation-duration:.01ms !important; } }
"""


def get_css() -> str:
    return CSS_TOKENS
