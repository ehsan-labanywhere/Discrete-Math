"""
Cognitive Scaffolding System
============================
Central design-system module for the Discrete Math Learning System.

Everything visual lives here so the eight chapters and the home page share a
single, consistent language. Import it and call ``theme.setup_page(...)`` as the
first Streamlit command in every page:

    import theme
    theme.setup_page("Ch 1: Logic & Proofs", "🔣")

Design tokens are taken from DESIGN.md ("Cognitive Scaffolding System"):
  * Deep Slate  #1E293B — structure & primary text
  * Indigo      #4F46E5 — logic / active / focus
  * Teal        #0D9488 — interaction / success / "what-if"
  * Amber       #D97706 — Socratic hints / cautions
  * Slate 50-200 tonal layers for elevation (tonal, not heavy shadow)
  * Inter for instruction, JetBrains Mono for logic/proofs
"""

import streamlit as st

# --------------------------------------------------------------------------- #
#  Design tokens (single source of truth)
# --------------------------------------------------------------------------- #
COLORS = {
    "base": "#F7F9FB",          # Level 0 background (Slate 50)
    "surface": "#FFFFFF",        # Level 1 card
    "surface_low": "#F2F4F6",
    "surface_high": "#ECEEF1",
    "border": "#E2E8F0",         # Slate 200 hairline
    "border_strong": "#CBD5E1",
    "ink": "#1E293B",            # Deep Slate — primary text
    "ink_soft": "#475569",       # secondary text
    "ink_faint": "#64748B",
    "slate": "#1E293B",
    "indigo": "#4F46E5",         # logic / active
    "indigo_soft": "#EEF2FF",
    "indigo_ink": "#3730A3",
    "teal": "#0D9488",           # interaction / success
    "teal_soft": "#F0FDFA",
    "teal_ink": "#115E59",
    "amber": "#D97706",          # hints / caution
    "amber_soft": "#FFFBEB",
    "amber_ink": "#92400E",
    "red": "#BA1A1A",
    "red_soft": "#FEF2F2",
}

# Public constants other modules can reuse for e.g. graphviz node colors
INDIGO = COLORS["indigo"]
TEAL = COLORS["teal"]
AMBER = COLORS["amber"]
SLATE = COLORS["slate"]


# --------------------------------------------------------------------------- #
#  Global CSS
# --------------------------------------------------------------------------- #
def _css() -> str:
    c = COLORS
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;450;500;600&display=swap');

:root {{
  --cs-base:{c['base']}; --cs-surface:{c['surface']}; --cs-border:{c['border']};
  --cs-ink:{c['ink']}; --cs-ink-soft:{c['ink_soft']};
  --cs-indigo:{c['indigo']}; --cs-teal:{c['teal']}; --cs-amber:{c['amber']};
  --cs-r-sm:4px; --cs-r-lg:8px; --cs-r-xl:12px;
}}

/* ---- Base typography & canvas ---------------------------------------- */
html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {{
  font-family:'Inter', system-ui, -apple-system, sans-serif;
  color:var(--cs-ink);
}}
.stApp {{ background:var(--cs-base); }}
[data-testid="stAppViewContainer"] .main .block-container {{
  padding-top:2.2rem; max-width:1180px;
}}

h1, h2, h3, h4 {{ color:var(--cs-ink); font-weight:700; letter-spacing:-0.02em; }}
h1 {{ font-size:2rem; line-height:1.15; }}
h2 {{ font-size:1.5rem; }}
h3 {{ font-size:1.2rem; color:var(--cs-ink) !important; font-weight:600; }}
p, li, .stMarkdown {{ color:var(--cs-ink); line-height:1.6; }}

/* ---- Logic typeface: proofs, code, LaTeX ----------------------------- */
code, kbd, pre, .stCode, [data-testid="stCodeBlock"] {{
  font-family:'JetBrains Mono', ui-monospace, monospace !important;
}}
[data-testid="stCodeBlock"] {{
  border:1px solid var(--cs-border); border-radius:var(--cs-r-lg);
}}
.katex {{ font-size:1.08em; }}
[data-testid="stMarkdownContainer"] .katex-display {{
  overflow-x:auto; overflow-y:hidden; padding:6px 2px;
  background:var(--cs-surface); border:1px solid var(--cs-border);
  border-radius:var(--cs-r-lg);
  -webkit-mask-image:linear-gradient(90deg,#000 92%,transparent);
          mask-image:linear-gradient(90deg,#000 92%,transparent);
}}

/* ---- Sidebar (course structure) -------------------------------------- */
[data-testid="stSidebar"] {{
  background:var(--cs-surface); border-right:1px solid var(--cs-border);
}}
[data-testid="stSidebarNav"] a[aria-current="page"] {{
  background:{c['indigo_soft']} !important; font-weight:600;
}}

/* ---- Tabs: multi-pane workspace feel --------------------------------- */
[data-baseweb="tab-list"] {{
  gap:4px; background:var(--cs-surface); padding:5px;
  border:1px solid var(--cs-border); border-radius:var(--cs-r-xl);
}}
button[data-baseweb="tab"] {{
  border-radius:var(--cs-r-lg); padding:6px 14px; color:var(--cs-ink-soft);
  font-weight:500;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  background:var(--cs-indigo); color:#fff;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{ display:none; }}
button[data-baseweb="tab"][aria-selected="true"] * {{ color:#fff !important; }}

/* ---- Buttons: touch-friendly, rounded-xl ----------------------------- */
.stButton > button {{
  border-radius:var(--cs-r-xl); border:1px solid #38BDF8;
  background:#38BDF8; color:#fff; font-weight:600;
  transition:transform .05s ease, box-shadow .15s ease, background .15s ease;
}}
.stButton > button:hover {{
  background:#0284C7; border-color:#0284C7; color:#fff;
  box-shadow:0 4px 14px rgba(56,189,248,.35);
}}
.stButton > button:active {{ transform:translateY(1px); }}
.stDownloadButton > button {{ border-radius:var(--cs-r-xl); }}

/* ---- Expanders as tonal cards ---------------------------------------- */
[data-testid="stExpander"] {{
  border:1px solid var(--cs-border); border-radius:var(--cs-r-lg);
  background:var(--cs-surface); box-shadow:none;
}}
[data-testid="stExpander"] summary {{ font-weight:600; color:var(--cs-ink); }}
[data-testid="stExpander"] summary:hover {{ color:var(--cs-indigo); }}

/* ---- Inputs ---------------------------------------------------------- */
[data-baseweb="input"] input, [data-baseweb="select"] > div, .stTextInput input {{
  border-radius:var(--cs-r-lg) !important;
}}

/* ---- Dataframes / truth tables --------------------------------------- */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
  border:1px solid var(--cs-border); border-radius:var(--cs-r-lg);
  overflow:hidden;
}}

/* ---- Alerts as Socratic / status blocks ------------------------------ */
[data-testid="stAlert"] {{ border-radius:var(--cs-r-lg); border:1px solid transparent; }}

/* ---- Dividers -------------------------------------------------------- */
hr {{ border-color:var(--cs-border); }}

/* ===================================================================== */
/*  Design-system components (used via helper functions & inline HTML)   */
/* ===================================================================== */

/* Bridge tags: Math <-> CS translation */
.math-tag {{
  background:{c['indigo_soft']}; color:{c['indigo_ink']}; padding:3px 9px;
  border-radius:var(--cs-r-sm); font-weight:600; font-size:.85em;
  font-family:'JetBrains Mono', monospace;
}}
.db-tag {{
  background:{c['teal_soft']}; color:{c['teal_ink']}; padding:3px 9px;
  border-radius:var(--cs-r-sm); font-weight:600; font-size:.85em;
  font-family:'JetBrains Mono', monospace;
}}

/* Highlight / bridge box (Level 1 card with indigo accent) */
.highlight-box {{
  background:var(--cs-surface); border:1px solid var(--cs-border);
  border-left:4px solid var(--cs-indigo); padding:14px 16px; margin:12px 0;
  border-radius:var(--cs-r-lg);
}}

/* Hero header */
.cs-hero {{
  background:linear-gradient(135deg,#1E293B 0%,#312E81 100%);
  color:#fff; padding:34px 32px; border-radius:var(--cs-r-xl); margin-bottom:6px;
}}
.cs-hero .kicker {{
  text-transform:uppercase; letter-spacing:.14em; font-size:.72rem;
  font-weight:600; color:#C7D2FE;
}}
.cs-hero h1 {{ color:#fff !important; margin:.35rem 0 .5rem; font-size:2.15rem; }}
.cs-hero p {{ color:#CBD5E1; font-size:1.02rem; margin:0; max-width:70ch; }}

/* Chapter header band */
.cs-chip {{
  display:inline-block; padding:4px 11px; border-radius:999px;
  font-size:.74rem; font-weight:600; letter-spacing:.03em;
  background:{c['indigo_soft']}; color:{c['indigo_ink']};
}}

/* Content card */
.cs-card {{
  background:var(--cs-surface); border:1px solid var(--cs-border);
  border-radius:var(--cs-r-lg); padding:18px 20px; margin:10px 0;
}}
.cs-card h4 {{ margin-top:0; }}

/* Roadmap grid card */
.cs-course-card {{
  background:var(--cs-surface); border:1px solid var(--cs-border);
  border-top:3px solid var(--accent,#4F46E5);
  border-radius:var(--cs-r-lg); padding:16px 18px; height:100%;
}}
.cs-course-card .num {{
  font-family:'JetBrains Mono',monospace; font-size:.78rem; font-weight:600;
  color:var(--accent,#4F46E5);
}}
.cs-course-card h4 {{ margin:.15rem 0 .4rem; font-size:1.02rem; }}
.cs-course-card p {{ font-size:.86rem; color:var(--cs-ink-soft); margin:0; }}

/* Socratic hint (amber thought-bubble) */
.cs-hint {{
  background:{c['amber_soft']}; border:1px solid #FDE68A;
  border-left:4px solid var(--cs-amber); border-radius:var(--cs-r-lg);
  padding:12px 15px; margin:10px 0; color:{c['amber_ink']};
}}
.cs-hint b {{ color:{c['amber_ink']}; }}

/* Tutor bubble (Socratic dialogue) */
.cs-tutor {{
  background:var(--cs-surface-high,#ECEEF1); border-radius:14px 14px 14px 4px;
  padding:12px 16px; margin:8px 0; color:var(--cs-ink); max-width:88%;
  border:1px solid var(--cs-border);
}}

/* What-If playground band */
.cs-playground {{
  background:{c['teal_soft']}; border:1px solid #99F6E4;
  border-left:4px solid var(--cs-teal); border-radius:var(--cs-r-lg);
  padding:6px 16px 14px; margin:12px 0;
}}
.cs-playground .pg-label {{
  color:{c['teal_ink']}; font-weight:600; font-size:.8rem;
  text-transform:uppercase; letter-spacing:.06em;
}}

/* Stateful stepper */
.cs-stepper {{ display:flex; align-items:center; margin:6px 0 14px; flex-wrap:wrap; gap:2px; }}
.cs-step {{ display:flex; align-items:center; }}
.cs-node {{
  width:26px; height:26px; border-radius:999px; display:flex;
  align-items:center; justify-content:center; font-size:.78rem; font-weight:700;
  border:2px solid var(--cs-border); background:var(--cs-surface);
  color:var(--cs-ink-soft); font-family:'JetBrains Mono',monospace;
}}
.cs-step.done .cs-node {{ background:var(--cs-teal); border-color:var(--cs-teal); color:#fff; }}
.cs-step.active .cs-node {{
  background:var(--cs-indigo); border-color:var(--cs-indigo); color:#fff;
  box-shadow:0 0 0 4px {c['indigo_soft']};
}}
.cs-bar {{ width:34px; height:2px; background:var(--cs-border); }}
.cs-step.done + .cs-step .cs-bar, .cs-step.done .cs-bar {{ background:var(--cs-teal); }}
.cs-label {{ font-size:.74rem; color:var(--cs-ink-soft); margin-left:6px; margin-right:4px; }}
.cs-step.active .cs-label {{ color:var(--cs-indigo); font-weight:600; }}

/* ===================================================================== */
/*  v2.0 Premium Enhancements                                           */
/* ===================================================================== */

/* Smooth transitions on all interactive elements */
*, *::before, *::after {{ transition: color .15s ease, background .15s ease, border-color .15s ease, box-shadow .15s ease, transform .1s ease; }}

/* Subtle card hover lift */
.cs-course-card:hover, .cs-card:hover {{
  box-shadow: 0 8px 25px rgba(30,41,59,.08);
  border-color: #C7D2FE;
  transform: translateY(-2px);
}}

/* Hero shimmer animation */
@keyframes heroShimmer {{
  0%   {{ background-position: 0% 50%; }}
  50%  {{ background-position: 100% 50%; }}
  100% {{ background-position: 0% 50%; }}
}}
.cs-hero {{
  background: linear-gradient(135deg, #1E293B 0%, #312E81 40%, #4F46E5 70%, #312E81 100%);
  background-size: 200% 200%;
  animation: heroShimmer 8s ease infinite;
  box-shadow: 0 8px 32px rgba(49,46,129,.25);
}}

/* Glassmorphism metric cards */
[data-testid="stMetric"] {{
  background: rgba(255,255,255,.75);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(226,232,240,.6);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(30,41,59,.04);
}}
[data-testid="stMetric"]:hover {{
  box-shadow: 0 4px 20px rgba(79,70,229,.1);
  border-color: #C7D2FE;
}}
[data-testid="stMetricValue"] {{
  font-weight: 700 !important;
  font-size: 1.8rem !important;
  background: linear-gradient(135deg, #4F46E5, #0D9488);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

/* Enhanced tab hover */
button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
  background: rgba(79,70,229,.06);
  color: #4F46E5;
}}

/* Polished expander hover */
[data-testid="stExpander"]:hover {{
  border-color: #C7D2FE;
  box-shadow: 0 2px 12px rgba(79,70,229,.06);
}}

/* Input focus glow */
[data-baseweb="input"] input:focus, .stTextInput input:focus {{
  border-color: #4F46E5 !important;
  box-shadow: 0 0 0 3px rgba(79,70,229,.12) !important;
}}

/* Success/Error/Info alert polish */
[data-testid="stAlert"] {{
  box-shadow: 0 2px 8px rgba(30,41,59,.04);
}}

/* Smooth button press */
.stButton > button:active {{
  transform: translateY(1px) scale(.98);
}}

/* Animated hint box */
.cs-hint {{
  position: relative;
  overflow: hidden;
}}
.cs-hint::before {{
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(217,119,6,.06), transparent);
  animation: hintShine 4s ease infinite;
}}
@keyframes hintShine {{
  0%   {{ left: -100%; }}
  100% {{ left: 200%; }}
}}

/* Playground pulse border */
.cs-playground {{
  position: relative;
}}
@keyframes tealPulse {{
  0%, 100% {{ border-left-color: #0D9488; }}
  50%      {{ border-left-color: #5EEAD4; }}
}}
.cs-playground {{ animation: tealPulse 3s ease-in-out infinite; }}

/* Bridge box arrow animation */
.highlight-box:hover {{
  border-left-color: #4F46E5;
  box-shadow: 0 2px 12px rgba(79,70,229,.08);
}}

/* Scrollbar styling */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: #CBD5E1; border-radius: 99px; }}
::-webkit-scrollbar-thumb:hover {{ background: #94A3B8; }}

/* Sidebar polish */
[data-testid="stSidebar"] {{
  box-shadow: 2px 0 12px rgba(30,41,59,.04);
}}

/* Version badge */
.cs-version-badge {{
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: .7rem;
  font-weight: 600;
  letter-spacing: .04em;
  background: linear-gradient(135deg, #4F46E5, #0D9488);
  color: #fff;
  margin-left: 8px;
  vertical-align: middle;
}}

/* Chapter nav buttons — styled as course cards */
button[kind="tertiary"][data-testid="stBaseButton-tertiary"] {{
  border: 1px solid var(--cs-border) !important;
  border-top: 3px solid var(--cs-indigo) !important;
  border-radius: var(--cs-r-lg) !important;
  background: var(--cs-surface) !important;
  padding: 18px 20px !important;
  text-align: left !important;
  white-space: pre-wrap !important;
  line-height: 1.5 !important;
  color: var(--cs-ink) !important;
  font-weight: 500 !important;
  font-size: .9rem !important;
  min-height: 140px !important;
  cursor: pointer !important;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease !important;
}}
button[kind="tertiary"][data-testid="stBaseButton-tertiary"]:hover {{
  box-shadow: 0 8px 25px rgba(30,41,59,.08) !important;
  border-color: #C7D2FE !important;
  border-top-color: var(--cs-indigo) !important;
  transform: translateY(-2px) !important;
  background: var(--cs-surface) !important;
  color: var(--cs-ink) !important;
}}
</style>
"""


# --------------------------------------------------------------------------- #
#  Page setup
# --------------------------------------------------------------------------- #
def setup_page(title: str, icon: str = "📐", layout: str = "wide") -> None:
    """First Streamlit call on every page. Sets config + injects the theme.

    ``set_page_config`` may only run once per session; under ``st.navigation``
    the entry page already calls it, so we swallow the resulting exception.
    """
    try:
        st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    except Exception:
        pass
    st.markdown(_css(), unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
#  Component helpers  (return/emit design-system HTML)
# --------------------------------------------------------------------------- #
def hero(title: str, subtitle: str = "", kicker: str = "") -> None:
    """Gradient hero banner for landing / chapter intros."""
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    s = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="cs-hero">{k}<h1>{title}</h1>{s}</div>',
                unsafe_allow_html=True)


def chapter_header(chip: str, title: str, subtitle: str = "") -> None:
    """Compact chapter title band with a category chip."""
    s = f'<p style="color:#475569;margin:.35rem 0 0;">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<span class="cs-chip">{chip}</span>'
        f'<h1 style="margin:.5rem 0 .1rem;">{title}</h1>{s}',
        unsafe_allow_html=True,
    )


def bridge(math_label: str, cs_label: str, note: str = "") -> None:
    """Render a Math ↔ CS bridge box."""
    n = f'<div style="margin-top:6px;color:#475569;font-size:.9em;">{note}</div>' if note else ""
    st.markdown(
        f'<div class="highlight-box">'
        f'<span class="math-tag">{math_label}</span>'
        f'<span style="margin:0 8px;color:#94A3B8;">&rarr;</span>'
        f'<span class="db-tag">{cs_label}</span>{n}</div>',
        unsafe_allow_html=True,
    )


def hint(text: str) -> None:
    """Amber Socratic hint / thought bubble."""
    st.markdown(f'<div class="cs-hint">💡 <b>Hint:</b> {text}</div>',
                unsafe_allow_html=True)


def tutor(text: str) -> None:
    """Socratic tutor dialogue bubble."""
    st.markdown(f'<div class="cs-tutor">🧑‍🏫 {text}</div>',
                unsafe_allow_html=True)


def stepper(labels, current: int) -> None:
    """Stateful progress stepper. Steps before ``current`` are done (teal),
    ``current`` is active (indigo), the rest are pending.

    ``current`` is 1-indexed.
    """
    html = ['<div class="cs-stepper">']
    for i, lab in enumerate(labels, start=1):
        cls = "done" if i < current else "active" if i == current else ""
        bar = '<div class="cs-bar"></div>' if i > 1 else ""
        mark = "✓" if i < current else str(i)
        html.append(
            f'{bar}<div class="cs-step {cls}">'
            f'<div class="cs-node">{mark}</div>'
            f'<span class="cs-label">{lab}</span></div>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def playground_open(label: str = "What-If Playground") -> None:
    """Open a Teal 'what-if' band. Pair with ``playground_close()``.

    Note: Streamlit widgets rendered between open/close sit visually inside
    the band via a negative-margin wrapper.
    """
    st.markdown(f'<div class="cs-playground"><div class="pg-label">🧪 {label}</div>',
                unsafe_allow_html=True)


def playground_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def section(title: str, subtitle: str = "") -> None:
    """Lightweight section header used inside chapters."""
    s = f'<span style="color:#64748B;font-weight:400;font-size:.9rem;">&nbsp;— {subtitle}</span>' if subtitle else ""
    st.markdown(f"### {title}{s}", unsafe_allow_html=True)
