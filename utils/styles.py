"""Shared design system for RecruitLens — adapted from SentimentScope."""

# Primary colour palette
_P   = "#2563EB"   # blue-600
_PL  = "#3B82F6"   # blue-500  (lighter accent)
_PXL = "#DBEAFE"   # blue-100  (very light bg)
_D   = "#0F172A"   # slate-900 (dark text)
_M   = "#475569"   # slate-600 (muted text)
_MU  = "#94A3B8"   # slate-400 (ultra-muted)

CSS = f"""
<style>
/* ── Streamlit chrome ──────────────────────────────────────── */
#MainMenu {{ visibility: hidden; }}
footer    {{ visibility: hidden; }}
/* Keep header visible so the sidebar toggle button works */
[data-testid="stHeader"] {{ background: transparent !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
}}

/* ── Sidebar ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: #EFF6FF !important;
    border-right: 1px solid rgba(37,99,235,0.12) !important;
}}

[data-testid="stSidebarNav"] a {{
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    padding: 6px 12px !important;
    color: #1E3A5F !important;
    transition: background 0.15s ease !important;
}}

[data-testid="stSidebarNav"] a:hover {{
    background: rgba(37,99,235,0.08) !important;
    color: {_P} !important;
}}

[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: rgba(37,99,235,0.1) !important;
    border-left: 2px solid {_P} !important;
    color: {_P} !important;
    font-weight: 600 !important;
}}

/* ── Buttons ────────────────────────────────────────────────── */
[data-testid="baseButton-primary"] {{
    background: linear-gradient(135deg, {_P} 0%, #1D4ED8 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.30) !important;
    transition: box-shadow 0.2s ease, transform 0.15s ease !important;
}}

[data-testid="baseButton-primary"]:hover {{
    box-shadow: 0 6px 22px rgba(37,99,235,0.46) !important;
    transform: translateY(-1px) !important;
}}

[data-testid="baseButton-secondary"] {{
    background: #FFFFFF !important;
    border: 1px solid rgba(37,99,235,0.22) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: {_P} !important;
}}

[data-testid="baseButton-secondary"]:hover {{
    background: rgba(37,99,235,0.04) !important;
    border-color: rgba(37,99,235,0.38) !important;
}}

/* ── Metrics ────────────────────────────────────────────────── */
[data-testid="stMetric"] {{
    background: #FFFFFF !important;
    border: 1px solid rgba(37,99,235,0.1) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.05) !important;
}}

[data-testid="stMetricValue"] {{
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: {_D} !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 0.70rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: {_MU} !important;
}}

/* ── File uploader ──────────────────────────────────────────── */
[data-testid="stFileUploadDropzone"] {{
    background: rgba(37,99,235,0.02) !important;
    border: 1.5px dashed rgba(37,99,235,0.22) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}}

[data-testid="stFileUploadDropzone"]:hover {{
    background: rgba(37,99,235,0.05) !important;
    border-color: rgba(37,99,235,0.4) !important;
}}

/* ── Text inputs / textarea ─────────────────────────────────── */
[data-testid="stTextArea"] textarea {{
    background: #FFFFFF !important;
    border: 1px solid rgba(37,99,235,0.16) !important;
    border-radius: 12px !important;
    color: {_D} !important;
}}

[data-testid="stTextArea"] textarea:focus {{
    border-color: rgba(37,99,235,0.42) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}}

/* ── Expanders ──────────────────────────────────────────────── */
[data-testid="stExpander"] details {{
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(37,99,235,0.1) !important;
    border-radius: 10px !important;
}}

/* ── DataFrames ─────────────────────────────────────────────── */
[data-testid="stDataFrame"] > div {{
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(37,99,235,0.1) !important;
}}

/* ── Alerts ─────────────────────────────────────────────────── */
[data-testid="stAlert"] {{ border-radius: 10px !important; }}

/* ── Checkboxes ─────────────────────────────────────────────── */
[data-testid="stCheckbox"] {{
    background: rgba(37,99,235,0.03) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    border: 1px solid rgba(37,99,235,0.08) !important;
}}

/* ── RL custom components ───────────────────────────────────── */

.rl-skill-badge {{
    display: inline-block;
    background: {_P};
    color: #fff;
    padding: 3px 11px;
    border-radius: 999px;
    margin: 2px 3px;
    font-size: 0.79em;
    font-weight: 600;
    letter-spacing: 0.01em;
}}

.rl-skill-badge-green {{
    display: inline-block;
    background: #059669;
    color: #fff;
    padding: 3px 11px;
    border-radius: 999px;
    margin: 2px 3px;
    font-size: 0.79em;
    font-weight: 600;
}}

.rl-skill-badge-red {{
    display: inline-block;
    background: #DC2626;
    color: #fff;
    padding: 3px 11px;
    border-radius: 999px;
    margin: 2px 3px;
    font-size: 0.79em;
    font-weight: 600;
}}

.rl-info-card {{
    background: #F8FAFF;
    border: 1px solid rgba(37,99,235,0.10);
    border-left: 3px solid {_P};
    padding: 14px 16px;
    border-radius: 10px;
    margin-bottom: 10px;
}}

.rl-info-card strong {{ color: {_D}; }}
.rl-info-card em {{ color: {_M}; font-size: 0.85em; }}

.rl-bar-wrap {{
    background: #E2E8F0;
    border-radius: 8px;
    height: 16px;
    width: 100%;
    margin: 6px 0 14px;
    overflow: hidden;
}}

.rl-bar-fill {{
    height: 16px;
    border-radius: 8px;
    transition: width 0.4s ease;
}}

.rl-sec {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 36px 0 16px;
}}

.rl-sec h3 {{
    font-size: 1.0rem;
    font-weight: 700;
    color: {_D};
    margin: 0;
    white-space: nowrap;
}}

.rl-sec-line {{
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(37,99,235,0.22) 0%, transparent 100%);
}}

.rl-page-head {{
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(37,99,235,0.10);
}}

.rl-page-head h1 {{
    font-size: 2rem;
    font-weight: 800;
    color: {_D};
    margin: 0 0 5px;
    letter-spacing: -0.015em;
}}

.rl-page-head p {{
    font-size: 0.9rem;
    color: {_M};
    margin: 0;
}}

.rl-divider {{
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(37,99,235,0.14) 25%,
        rgba(37,99,235,0.14) 75%,
        transparent 100%);
    margin: 36px 0;
}}

/* ── Feature card grid ─────────────────────────────────────── */
.rl-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 36px;
}}

.rl-grid-3 {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-bottom: 36px;
}}

.rl-card {{
    background: #FFFFFF;
    border: 1px solid rgba(37,99,235,0.10);
    border-radius: 16px;
    padding: 22px 18px;
    box-shadow: 0 2px 10px rgba(37,99,235,0.06);
}}

.rl-card-icon {{ font-size: 1.7rem; display: block; margin-bottom: 12px; }}
.rl-card-title {{ font-size: 0.94rem; font-weight: 700; color: {_D}; margin: 0 0 6px; }}
.rl-card-body  {{ font-size: 0.81rem; color: {_M}; line-height: 1.65; margin: 0; }}

/* ── Steps grid ─────────────────────────────────────────────── */
.rl-steps {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 8px;
}}

.rl-step {{
    background: #FFFFFF;
    border: 1px solid rgba(37,99,235,0.09);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    box-shadow: 0 1px 4px rgba(37,99,235,0.05);
}}

.rl-step-num {{
    min-width: 26px; height: 26px;
    background: rgba(37,99,235,0.08);
    border: 1px solid rgba(37,99,235,0.2);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.76rem; font-weight: 800;
    color: {_P}; flex-shrink: 0;
}}

.rl-step h4 {{ font-size: 0.85rem; font-weight: 700; color: {_D}; margin: 0 0 4px; }}
.rl-step p  {{ font-size: 0.78rem; color: {_M}; line-height: 1.55; margin: 0; }}

/* ── Stat strip ─────────────────────────────────────────────── */
.rl-stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
    gap: 10px;
    margin-bottom: 28px;
}}

.rl-stat {{
    background: #FFFFFF;
    border: 1px solid rgba(37,99,235,0.10);
    border-radius: 12px;
    padding: 18px 10px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(37,99,235,0.05);
}}

.rl-stat-label {{
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: {_MU};
    margin: 0 0 8px;
}}

.rl-stat-value {{
    font-size: 1.55rem;
    font-weight: 900;
    line-height: 1;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
    color: {_D};
}}

.rl-stat-sub {{
    font-size: 0.72rem;
    font-weight: 600;
    color: {_MU};
}}
</style>
"""


def inject() -> str:
    return CSS


def hero(eyebrow: str, title: str, accent: str, subtitle: str) -> str:
    return f"""
<div style="position:relative;background:linear-gradient(160deg,#EFF6FF 0%,#FFFFFF 55%,#F0F9FF 100%);border:1px solid rgba(37,99,235,0.14);border-radius:22px;padding:clamp(28px,5vw,60px) clamp(20px,5vw,52px);text-align:center;overflow:hidden;margin-bottom:36px;box-shadow:0 4px 24px rgba(37,99,235,0.07),0 1px 4px rgba(37,99,235,0.04);">
  <div style="position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:620px;height:260px;background:radial-gradient(ellipse,rgba(37,99,235,0.12) 0%,transparent 70%);pointer-events:none;"></div>
  <div style="position:relative;z-index:1;">
    <div style="display:inline-block;background:rgba(37,99,235,0.07);border:1px solid rgba(37,99,235,0.2);border-radius:999px;padding:5px 18px;font-size:0.70rem;color:{_P};letter-spacing:0.14em;text-transform:uppercase;font-weight:700;margin-bottom:22px;">{eyebrow}</div>
    <h1 style="font-size:clamp(1.8rem,4vw,3.2rem);font-weight:900;color:{_D};margin:0 0 14px;line-height:1.1;letter-spacing:-0.02em;">{title} <span style="background:linear-gradient(130deg,{_P} 0%,{_PL} 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{accent}</span></h1>
    <div style="font-size:1.05rem;color:{_M};line-height:1.7;margin:0 auto;max-width:520px;text-align:center !important;">{subtitle}</div>
  </div>
</div>"""


def feature_cards(*cards) -> str:
    inner = "".join(
        f'<div class="rl-card"><span class="rl-card-icon">{icon}</span>'
        f'<p class="rl-card-title">{title}</p>'
        f'<p class="rl-card-body">{body}</p></div>'
        for icon, title, body in cards
    )
    return f'<div class="rl-grid">{inner}</div>'


def feature_cards_3(*cards) -> str:
    inner = "".join(
        f'<div class="rl-card"><span class="rl-card-icon">{icon}</span>'
        f'<p class="rl-card-title">{title}</p>'
        f'<p class="rl-card-body">{body}</p></div>'
        for icon, title, body in cards
    )
    return f'<div class="rl-grid-3">{inner}</div>'


def step_cards(*steps) -> str:
    inner = "".join(
        f'<div class="rl-step"><div class="rl-step-num">{i+1}</div>'
        f'<div><h4>{title}</h4><p>{desc}</p></div></div>'
        for i, (title, desc) in enumerate(steps)
    )
    return f'<div class="rl-steps">{inner}</div>'


def section(title: str) -> str:
    return f'<div class="rl-sec"><h3>{title}</h3><div class="rl-sec-line"></div></div>'


def divider() -> str:
    return '<div class="rl-divider"></div>'


def page_header(title: str, caption: str) -> str:
    return f'<div class="rl-page-head"><h1>{title}</h1><p>{caption}</p></div>'


def ats_stats(total: int, contact: int, skills: int, exp: int, edu: int, detail: int) -> str:
    color = "#059669" if total >= 70 else ("#D97706" if total >= 45 else "#DC2626")
    return f"""
<div class="rl-stats">
  <div class="rl-stat">
    <div class="rl-stat-label">Total</div>
    <div class="rl-stat-value" style="color:{color};">{total}</div>
    <div class="rl-stat-sub">/ 100</div>
  </div>
  <div class="rl-stat">
    <div class="rl-stat-label">Contact</div>
    <div class="rl-stat-value">{contact}</div>
    <div class="rl-stat-sub">/ 20</div>
  </div>
  <div class="rl-stat">
    <div class="rl-stat-label">Skills</div>
    <div class="rl-stat-value">{skills}</div>
    <div class="rl-stat-sub">/ 25</div>
  </div>
  <div class="rl-stat">
    <div class="rl-stat-label">Experience</div>
    <div class="rl-stat-value">{exp}</div>
    <div class="rl-stat-sub">/ 25</div>
  </div>
  <div class="rl-stat">
    <div class="rl-stat-label">Education</div>
    <div class="rl-stat-value">{edu}</div>
    <div class="rl-stat-sub">/ 15</div>
  </div>
  <div class="rl-stat">
    <div class="rl-stat-label">Detail</div>
    <div class="rl-stat-value">{detail}</div>
    <div class="rl-stat-sub">/ 15</div>
  </div>
</div>"""


def ats_bar(score: int) -> str:
    color = "#059669" if score >= 70 else ("#D97706" if score >= 45 else "#DC2626")
    return (
        f'<div class="rl-bar-wrap">'
        f'<div class="rl-bar-fill" style="width:{score}%;background:{color};"></div>'
        f'</div>'
    )


def skill_badges(skills: list, style: str = "default") -> str:
    cls = {"default": "rl-skill-badge", "green": "rl-skill-badge-green", "red": "rl-skill-badge-red"}.get(style, "rl-skill-badge")
    return " ".join(f'<span class="{cls}">{s}</span>' for s in skills)


def info_card(title: str, subtitle: str = "", meta: str = "") -> str:
    sub = f"<br><span style='font-size:0.85em;color:#475569;'>{subtitle}</span>" if subtitle else ""
    mt  = f"<br><em>{meta}</em>" if meta else ""
    return f'<div class="rl-info-card"><strong>{title}</strong>{sub}{mt}</div>'
