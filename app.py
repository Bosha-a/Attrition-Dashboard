import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import base64, warnings
from PIL import Image
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kayfa HR — Attrition Intelligence",
    page_icon=Image.open("kayfa icon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# LOGO
# ──────────────────────────────────────────────────────────────────────────────
with open("kayfa.png", "rb") as _f:
    _LOGO_B64 = base64.b64encode(_f.read()).decode()

def logo(h=54):
    return f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:{h}px;width:auto;object-fit:contain;display:block;" />'

# ──────────────────────────────────────────────────────────────────────────────
# BRAND COLOURS  (sourced from kayfa.png blue)
# ──────────────────────────────────────────────────────────────────────────────
BRAND       = "#2D3BE0"
BRAND_DARK  = "#1A24A8"
BRAND_LIGHT = "#E8EAFD"
BRAND_MID   = "#4D5CE8"
RED         = "#E53E3E"
AMBER       = "#DD6B20"
GREEN       = "#276749"
NEUTRAL     = "#718096"

# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — light-first, respects Streamlit's built-in dark/light toggle
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ─────────────── APP SHELL ─────────────── */
.stApp {{
    background: #F4F6FF;
}}
.main .block-container {{
    padding: 1rem 2rem 2.5rem 2rem;
    max-width: 1640px;
}}

/* ─────────────── SIDEBAR ─────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0B1060 0%, {BRAND_DARK} 45%, {BRAND} 100%);
    border-right: none;
    box-shadow: 4px 0 28px rgba(45,59,224,.20);
    display: block !important;
    visibility: visible !important;
}}
[data-testid="stSidebar"][aria-expanded="false"] {{
    transform: translateX(0) !important;
    min-width: 20rem !important;
    width: 20rem !important;
}}
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[aria-label*="sidebar" i] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}}
[data-testid="stSidebar"] .block-container {{
    padding: 1rem 1.1rem;
}}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown p {{
    color: #C8D0FF !important;
}}
/* select boxes */
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(255,255,255,.10) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 8px !important;
    color: #fff !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background: rgba(255,255,255,.22) !important;
    color: #fff !important;
}}
/* slider track */
[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {{
    background: #fff !important;
}}

/* ─────────────── FIXED TOP-RIGHT LOGO ─────────────── */
.fixed-logo {{
    position: fixed;
    top: 10px;
    right: 18px;
    z-index: 9999;
    pointer-events: none;
}}

/* ─────────────── SIDEBAR LOGO CARD ─────────────── */
.sb-logo-card {{
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(255,255,255,1);
    border-radius: 14px;
    padding: 12px 50px 5px;
    text-align: center;
    margin-bottom: 1.1rem;
    backdrop-filter: blur(8px);
}}
.sb-logo-sub {{
    font-size: .64rem;
    color: rgba(255,255,255,.50);
    margin-top: 8px;
    letter-spacing: .12em;
    font-weight: 600;
    text-transform: uppercase;
}}

/* ─────────────── DIVIDER ─────────────── */
.div-line {{
    border: none;
    border-top: 1px solid rgba(45,59,224,.13);
    margin: .85rem 0;
}}
.div-line-sb {{
    border: none;
    border-top: 1px solid rgba(255,255,255,.15);
    margin: .85rem 0;
}}

/* ─────────────── FILTER PILL ─────────────── */
.filter-pill {{
    display: inline-block;
    background: rgba(255,255,255,.18);
    color: #fff;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: .67rem;
    font-weight: 600;
    letter-spacing: .05em;
    margin-top: 4px;
}}

/* ─────────────── HERO HEADER ─────────────── */
.hero {{
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 80% 15%, rgba(110,140,255,.55) 0%, transparent 38%),
        radial-gradient(circle at 15% 85%, rgba(18,25,140,.48) 0%, transparent 35%),
        linear-gradient(135deg, {BRAND_DARK} 0%, {BRAND} 52%, {BRAND_MID} 100%);
    border-radius: 18px;
    padding: 42px 40px 38px;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 16px 52px rgba(26,36,168,.30);
}}
.hero-pill {{
    display: inline-flex;
    align-items: center;
    gap: 9px;
    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.28);
    border-radius: 999px;
    padding: 10px 22px;
    color: rgba(255,255,255,.88);
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    backdrop-filter: blur(10px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.22);
}}
.hero-kicker {{
    color: rgba(255,255,255,.68);
    font-size: .8rem;
    font-weight: 800;
    letter-spacing: .38em;
    text-transform: uppercase;
    margin-top: 32px;
}}
.hero-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.6rem, 5.5vw, 4.6rem);
    font-weight: 800;
    color: #fff;
    line-height: .97;
    margin: 24px auto 20px;
    max-width: 900px;
    text-shadow: 0 10px 30px rgba(13,18,89,.28);
}}
.hero-subtitle {{
    color: rgba(255,255,255,.72);
    font-size: clamp(.92rem, 1.4vw, 1.1rem);
    line-height: 1.55;
    max-width: 760px;
    margin: 0 auto;
}}

/* ─────────────── KPI CARD ─────────────── */
.kpi-card {{
    background: linear-gradient(140deg, {BRAND} 0%, {BRAND_DARK} 100%);
    border-radius: 16px;
    padding: 20px 16px 16px;
    text-align: center;
    box-shadow: 0 6px 22px rgba(45,59,224,.22);
    min-height: 120px;
    transition: transform .18s, box-shadow .18s;
}}
.kpi-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 34px rgba(45,59,224,.32);
}}
.kpi-icon  {{ font-size: 1.45rem; margin-bottom: 4px; }}
.kpi-label {{
    font-size: .64rem; font-weight: 700; letter-spacing: .12em;
    color: rgba(255,255,255,.68); text-transform: uppercase; margin-bottom: 5px;
}}
.kpi-value {{ font-size: 1.85rem; font-weight: 800; color: #fff; line-height: 1; margin-bottom: 3px; }}
.kpi-delta {{ font-size: .65rem; color: rgba(255,255,255,.55); }}

/* ─────────────── SECTION HEADER ─────────────── */
.sec-hdr {{
    background: linear-gradient(90deg, {BRAND_LIGHT} 0%, transparent 100%);
    border-left: 4px solid {BRAND};
    border-radius: 0 10px 10px 0;
    padding: 9px 16px;
    margin: 1.4rem 0 .9rem;
}}
.sec-hdr h3 {{
    margin: 0; color: {BRAND_DARK};
    font-size: 1rem; font-weight: 700; letter-spacing: .02em;
}}

/* ─────────────── INSIGHT BOX (below charts) ─────────────── */
.insight-box {{
    background: {BRAND_LIGHT};
    border-left: 4px solid {BRAND};
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    font-size: .76rem;
    color: #2d3748;
    line-height: 1.6;
    margin-top: -4px;
    margin-bottom: 1rem;
}}
.insight-box b {{ color: {BRAND_DARK}; }}

/* ─────────────── SUGGESTION CARD ─────────────── */
.sug-card {{
    background: #fff;
    border-left: 5px solid {BRAND};
    border-radius: 0 14px 14px 0;
    padding: 16px 18px;
    box-shadow: 0 3px 14px rgba(45,59,224,.09);
    margin-bottom: .8rem;
    transition: transform .15s, box-shadow .15s;
    height: 100%;
}}
.sug-card:hover {{ transform: translateX(4px); box-shadow: 0 6px 22px rgba(45,59,224,.18); }}
.sug-card.urg  {{ border-left-color: {RED};   }}
.sug-card.med  {{ border-left-color: {AMBER}; }}
.sug-card.win  {{ border-left-color: {GREEN}; }}
.sug-hdr  {{ display:flex; align-items:center; gap:9px; margin-bottom:7px; flex-wrap:wrap; }}
.sug-badge {{
    font-size: .6rem; font-weight: 800; letter-spacing: .1em;
    padding: 3px 9px; border-radius: 20px; text-transform: uppercase; white-space: nowrap;
}}
.b-urg {{ background:#FED7D7; color:#9B2C2C; }}
.b-med {{ background:#FEEBC8; color:#9C4221; }}
.b-win {{ background:#C6F6D5; color:#22543D; }}
.sug-title {{ font-size: .86rem; font-weight: 700; color: #1a202c; }}
.sug-stat  {{
    display: inline-block; font-size: .71rem; font-weight: 600;
    color: {BRAND}; background: {BRAND_LIGHT};
    padding: 2px 9px; border-radius: 8px; margin-bottom: 7px;
}}
.sug-body  {{ font-size: .77rem; color: #4a5568; line-height: 1.65; }}

/* ─────────────── TABS ─────────────── */
.stTabs [data-baseweb="tab-list"] {{
    background: #fff;
    border-radius: 12px;
    padding: 4px;
    gap: 3px;
    border: 1px solid rgba(45,59,224,.14);
    box-shadow: 0 2px 8px rgba(45,59,224,.07);
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 9px;
    color: #4a5568;
    font-weight: 600;
    font-size: .80rem;
    padding: 8px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {BRAND_DARK}, {BRAND}) !important;
    color: #fff !important;
    box-shadow: 0 3px 10px rgba(45,59,224,.28);
}}
.stTabs [data-baseweb="tab-highlight"] {{
    background-color: {BRAND} !important;
}}

/* ─────────────── LEGEND DOT ─────────────── */
.ldot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:5px; vertical-align:middle; }}

/* hide Streamlit chrome but keep the header/sidebar control usable */
#MainMenu, footer {{ visibility: hidden; }}
header {{ background: transparent !important; }}
[data-testid="stToolbar"] {{ visibility: hidden; }}

/* ─────────────── RESPONSIVE ─────────────── */
@media (max-width: 760px) {{
    .main .block-container {{ padding: .7rem .8rem 1.5rem; }}
    .hero {{ padding: 26px 18px 22px; }}
    .hero-title {{ font-size: 2.2rem; margin: 18px auto 16px; }}
}}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# FIXED TOP-RIGHT LOGO
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="fixed-logo">{logo(80)}</div>', unsafe_allow_html=True)

components.html("""
<script>
function openSidebarIfCollapsed() {
  const doc = window.parent.document;
  const sidebar = doc.querySelector('[data-testid="stSidebar"]');
  if (!sidebar || sidebar.getAttribute('aria-expanded') !== 'false') return;

  const buttons = Array.from(doc.querySelectorAll('button'));
  const toggle = buttons.find((button) => {
    const label = (button.getAttribute('aria-label') || '').toLowerCase();
    return label.includes('sidebar') || label.includes('menu');
  });
  if (toggle) toggle.click();
}

setTimeout(openSidebarIfCollapsed, 150);
setTimeout(openSidebarIfCollapsed, 600);
setTimeout(openSidebarIfCollapsed, 1200);
</script>
""", height=0)


# ──────────────────────────────────────────────────────────────────────────────
# PLOTLY SHARED THEME
# ──────────────────────────────────────────────────────────────────────────────
_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#2d3748", size=11),
    title_font=dict(family="Inter", color="#1a202c", size=13),
    legend=dict(
        bgcolor="rgba(255,255,255,.92)",
        bordercolor="rgba(45,59,224,.14)",
        borderwidth=1,
        font=dict(color="#4a5568", size=10),
        title_font=dict(color="#000000", size=10),
    ),
    xaxis=dict(
        gridcolor="rgba(45,59,224,.07)",
        linecolor="rgba(45,59,224,.18)",
        tickcolor="rgba(45,59,224,.18)",
        title_font=dict(color="#4a5568"),
        tickfont=dict(color="#4a5568"),
    ),
    yaxis=dict(
        gridcolor="rgba(45,59,224,.07)",
        linecolor="rgba(45,59,224,.18)",
        tickcolor="rgba(45,59,224,.18)",
        title_font=dict(color="#000000"),
        tickfont=dict(color="#000000"),
    ),
    margin=dict(l=44, r=22, t=52, b=44),
)

SCALE_ATT = [[0, BRAND_LIGHT], [0.5, BRAND], [1, RED]]  # low→high attrition
SCALE_INC = [[0, BRAND_LIGHT], [1, BRAND]]               # income (all positive)
DISC_ATT  = {"Stayed": BRAND, "Left": RED}               # discrete attrition


def _theme(fig, title=""):
    fig.update_layout(**_BASE)
    if title:
        fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left"))
    return fig


def cw(fig, key=None):
    st.plotly_chart(fig, use_container_width=True, key=key)


def sec(icon, txt):
    st.markdown(f'<div class="sec-hdr"><h3>{icon}&nbsp;&nbsp;{txt}</h3></div>', unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)


def kpi(icon, label, value, delta=""):
    return (f'<div class="kpi-card">'
            f'<div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-delta">{delta}</div>'
            f'</div>')

def answer_card(q, title, stat, insight_text, action_text, points=None, tone="urg"):
    pts = f"{points} pts" if points else "Insight"
    return f"""
    <div class="sug-card {tone}">
        <div class="sug-hdr">
            <span class="sug-badge {'b-urg' if tone == 'urg' else 'b-med' if tone == 'med' else 'b-win'}">{q} · {pts}</span>
            <span class="sug-title">{title}</span>
        </div>
        <div class="sug-stat">{stat}</div>
        <div class="sug-body"><b>Insight:</b> {insight_text}<br><br><b>Suggestion:</b> {action_text}</div>
    </div>
    """

def attr_summary(data, group_cols, min_count=1):
    if isinstance(group_cols, str):
        group_cols = [group_cols]
    out = (data.groupby(group_cols, observed=True)["Attrition_Num"]
           .agg(rate="mean", count="count")
           .reset_index())
    out["rate"] *= 100
    return out[out["count"] >= min_count].sort_values("rate", ascending=False)

def pct(value):
    return f"{value:.1f}%"

def count_fmt(value):
    return f"{int(value):,}"

def add_analysis_fields(data):
    out = data.copy()
    if len(out) == 0:
        return out
    out["Age Band"] = pd.cut(out["Age"], bins=[17,25,35,45,55,100],
                             labels=["18-25","26-35","36-45","46-55","56+"], ordered=True)
    out["Dependent Band"] = pd.cut(out["Number of Dependents"], bins=[-1,0,2,99],
                                   labels=["0","1-2","3+"], ordered=True)
    out["Tenure Band"] = pd.cut(out["Years at Company"], bins=[0,1,2,3,5,10,15,100],
                                labels=["<1 yr","1-2 yrs","2-3 yrs","3-5 yrs","5-10 yrs","10-15 yrs","15+ yrs"],
                                right=False, ordered=True)
    def level_quartile(s):
        if len(s) < 4 or s.nunique() < 2:
            return pd.Series(["Q1 low"] * len(s), index=s.index)
        return pd.qcut(s.rank(method="first"), 4, labels=["Q1 low","Q2","Q3","Q4 high"])

    out["Income Quartile in Level"] = out.groupby("Job Level", observed=True)["Monthly Income"].transform(level_quartile)
    return out


# ──────────────────────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("Attrition.csv")
    df["Attrition_Num"] = (df["Attrition"] == "Left").astype(int)

    # Ordinal helpers
    df["WLB_N"]  = df["Work-Life Balance"].map({"Poor":1,"Fair":2,"Good":3,"Excellent":4})
    df["JS_N"]   = df["Job Satisfaction"].map({"Low":1,"Medium":2,"High":3,"Very High":4})
    df["REC_N"]  = df["Employee Recognition"].map({"Low":1,"Medium":2,"High":3,"Very High":4})

    # Ordered categoricals
    WLB_ORD   = ["Poor","Fair","Good","Excellent"]
    JS_ORD    = ["Low","Medium","High","Very High"]
    PERF_ORD  = ["Low","Below Average","Average","High"]
    REP_ORD   = ["Poor","Fair","Good","Excellent"]
    REC_ORD   = ["Low","Medium","High","Very High"]
    LEVEL_ORD = ["Entry","Mid","Senior"]
    EDU_ORD   = ["High School","Associate Degree","Bachelor’s Degree","Master’s Degree","PhD"]
    SIZE_ORD  = ["Small","Medium","Large"]

    for col, order in [
        ("Work-Life Balance", WLB_ORD), ("Job Satisfaction", JS_ORD),
        ("Performance Rating", PERF_ORD), ("Company Reputation", REP_ORD),
        ("Employee Recognition", REC_ORD), ("Job Level", LEVEL_ORD),
        ("Education Level", ["High School","Associate Degree","Bachelor’s Degree","Master’s Degree","PhD"]), ("Company Size", SIZE_ORD),
    ]:
        df[col] = pd.Categorical(df[col], categories=order, ordered=True)

    # Bands
    df["Age Group"] = pd.cut(df["Age"], bins=[17,25,35,45,55,62],
                             labels=["18–25","26–35","36–45","46–55","56+"], ordered=True)
    df["Income Band"] = pd.cut(df["Monthly Income"],
                               bins=[0,4000,7000,10000,25000],
                               labels=["< $4k","$4k–$7k","$7k–$10k","$10k+"], ordered=True)
    df["Tenure Group"] = pd.cut(df["Years at Company"], bins=range(0,27,2), right=False)
    return df


df_raw = load()

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR — filters
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo card
    st.markdown(f"""
    <div class="sb-logo-card">
        {logo(150)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="div-line-sb">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Filters")

    g   = st.multiselect("👤 Gender",       sorted(df_raw["Gender"].unique()),       default=sorted(df_raw["Gender"].unique()))
    rol = st.multiselect("💼 Job Role",     sorted(df_raw["Job Role"].unique()),     default=sorted(df_raw["Job Role"].unique()))
    lvl = st.multiselect("📊 Job Level",   ["Entry","Mid","Senior"],                default=["Entry","Mid","Senior"])
    siz = st.multiselect("🏭 Company Size",["Small","Medium","Large"],              default=["Small","Medium","Large"])
    age = st.slider("🎂 Age",  int(df_raw["Age"].min()), int(df_raw["Age"].max()),
                    (int(df_raw["Age"].min()), int(df_raw["Age"].max())))
    inc = st.slider("💰 Monthly Income ($)",
                    int(df_raw["Monthly Income"].min()), int(df_raw["Monthly Income"].max()),
                    (int(df_raw["Monthly Income"].min()), int(df_raw["Monthly Income"].max())))
    ot  = st.multiselect("⏰ Overtime",     ["No","Yes"],                           default=["No","Yes"])
    ms  = st.multiselect("💍 Marital Status",sorted(df_raw["Marital Status"].unique()),default=sorted(df_raw["Marital Status"].unique()))

    mask = (
        df_raw["Gender"].isin(g) & df_raw["Job Role"].isin(rol) &
        df_raw["Job Level"].isin(lvl) & df_raw["Company Size"].isin(siz) &
        df_raw["Age"].between(age[0], age[1]) &
        df_raw["Monthly Income"].between(inc[0], inc[1]) &
        df_raw["Overtime"].isin(ot) & df_raw["Marital Status"].isin(ms)
    )
    df = df_raw[mask].copy()

    n_tot = len(df)
    n_lft = int((df["Attrition"] == "Left").sum())
    n_sty = int((df["Attrition"] == "Stayed").sum())

    st.markdown('<hr class="div-line-sb">', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="filter-pill">📋 {n_tot:,} employees in view</span></div>',
                unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-pill">
        {logo(16)}&nbsp;&nbsp;HR Attrition Intelligence
    </div>
    <div class="hero-kicker">Kayfa Analytics · Week #1 Task</div>
    <div class="hero-title">Employee Attrition<br>Intelligence Report</div>
    <div class="hero-subtitle">
        Analyse workforce patterns, uncover retention risks, and turn employee data into
        clear action plans — across 74,498 employee records.
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TABS — multipage via st.tabs (st.navigation needs actual file pages; tabs are correct for single-file)
# ──────────────────────────────────────────────────────────────────────────────
tabs = st.tabs(["Overview", "Diagnostic", "Demographic", "Financial", "Suggestions", "Stakeholder Answers"])
t_ov, t_dx, t_dm, t_fi, t_sg, t_ans = tabs


# ════════════════════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with t_ans:
    sec("Q", "Stakeholder Answers: Insights and Actions")
    st.caption("Each answer is calculated from the current sidebar filter view and ends with a business action.")

    qa = add_analysis_fields(df)
    if len(qa) == 0:
        st.warning("No employees match the current filters.")
    else:
        baseline = qa["Attrition_Num"].mean() * 100
        left_total = int(qa["Attrition_Num"].sum())
        total = len(qa)

        role_counts = (qa[qa["Attrition"] == "Left"].groupby("Job Role", observed=True)
                       .size().reset_index(name="leavers").sort_values("leavers", ascending=False))
        role_rates = attr_summary(qa, "Job Role")
        top_role_count = role_counts.iloc[0]
        top_role_rate = role_rates.iloc[0]

        ot_rates = attr_summary(qa, "Overtime")
        ot_yes = ot_rates.loc[ot_rates["Overtime"].astype(str) == "Yes", "rate"].iloc[0] if (ot_rates["Overtime"].astype(str) == "Yes").any() else np.nan
        ot_no = ot_rates.loc[ot_rates["Overtime"].astype(str) == "No", "rate"].iloc[0] if (ot_rates["Overtime"].astype(str) == "No").any() else np.nan
        ot_gap = ot_yes - ot_no if pd.notna(ot_yes) and pd.notna(ot_no) else np.nan

        remote_rates = attr_summary(qa, "Remote Work")
        remote_yes = remote_rates.loc[remote_rates["Remote Work"].astype(str) == "Yes", "rate"].iloc[0] if (remote_rates["Remote Work"].astype(str) == "Yes").any() else np.nan
        remote_no = remote_rates.loc[remote_rates["Remote Work"].astype(str) == "No", "rate"].iloc[0] if (remote_rates["Remote Work"].astype(str) == "No").any() else np.nan
        remote_share = qa["Remote Work"].astype(str).eq("Yes").mean() * 100

        income_level = attr_summary(qa.dropna(subset=["Income Quartile in Level"]), ["Job Level", "Income Quartile in Level"])
        q1 = income_level[income_level["Income Quartile in Level"].astype(str).eq("Q1 low")]
        q4 = income_level[income_level["Income Quartile in Level"].astype(str).eq("Q4 high")]
        pay_gap = (q1["rate"].mean() - q4["rate"].mean()) if len(q1) and len(q4) else np.nan

        tenure_rates = attr_summary(qa.dropna(subset=["Tenure Band"]), "Tenure Band")
        top_tenure = tenure_rates.iloc[0]
        js_wlb = attr_summary(qa, ["Job Satisfaction", "Work-Life Balance"], min_count=50)
        top_engagement = js_wlb.iloc[0]
        life = attr_summary(qa.dropna(subset=["Age Band", "Dependent Band"]),
                            ["Age Band", "Marital Status", "Dependent Band"], min_count=100)
        top_life = life.iloc[0] if len(life) else None

        promo_rates = attr_summary(qa, "Number of Promotions")
        no_promo = promo_rates.loc[promo_rates["Number of Promotions"].eq(0), "rate"].iloc[0] if promo_rates["Number of Promotions"].eq(0).any() else np.nan
        many_promo = promo_rates[promo_rates["Number of Promotions"].isin([3, 4])]["rate"].mean()
        stuck = attr_summary(qa, ["Number of Promotions", "Job Level", "Leadership Opportunities", "Innovation Opportunities"], min_count=100)
        top_stuck = stuck.iloc[0] if len(stuck) else None

        risk_mask = (
            qa["Remote Work"].astype(str).eq("No") &
            qa["Job Level"].astype(str).eq("Entry") &
            qa["Work-Life Balance"].astype(str).eq("Poor") &
            qa["Marital Status"].astype(str).eq("Single")
        )
        risk_count = int(risk_mask.sum())
        risk_rate = qa.loc[risk_mask, "Attrition_Num"].mean() * 100 if risk_count else np.nan
        risk_lift = risk_rate - baseline if pd.notna(risk_rate) else np.nan

        driver_rows = []
        for label, col, value, actionability in [
            ("Single employees", "Marital Status", "Single", "support life-stage flexibility"),
            ("Entry-level employees", "Job Level", "Entry", "fix onboarding and early career paths"),
            ("Poor work-life balance", "Work-Life Balance", "Poor", "rebalance workload"),
            ("No remote work", "Remote Work", "No", "expand hybrid eligibility"),
            ("Overtime", "Overtime", "Yes", "cap recurring overtime"),
        ]:
            mask = qa[col].astype(str).eq(value)
            if mask.any():
                rate = qa.loc[mask, "Attrition_Num"].mean() * 100
                driver_rows.append({"Driver": label, "Rate": rate, "Lift": rate - baseline,
                                    "Employees": int(mask.sum()), "Action": actionability})
        drivers = pd.DataFrame(driver_rows).sort_values("Lift", ascending=False)
        actionable = drivers[drivers["Driver"].isin(["Entry-level employees", "Poor work-life balance", "No remote work", "Overtime"])]
        top_action = actionable.iloc[0] if len(actionable) else drivers.iloc[0]

        entry_rate = qa.loc[qa["Job Level"].astype(str).eq("Entry"), "Attrition_Num"].mean() * 100
        mid_rate = qa.loc[qa["Job Level"].astype(str).eq("Mid"), "Attrition_Num"].mean() * 100
        entry_count = int(qa["Job Level"].astype(str).eq("Entry").sum())
        entry_impact = ((entry_rate - mid_rate) / 100 * entry_count / total * 100) if pd.notna(entry_rate) and pd.notna(mid_rate) else np.nan

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(kpi("A", "Company Attrition", pct(baseline), f"{count_fmt(left_total)} of {count_fmt(total)} left"), unsafe_allow_html=True)
        with k2:
            st.markdown(kpi("R", "Largest Role Leak", str(top_role_count["Job Role"]), f"{count_fmt(top_role_count['leavers'])} leavers"), unsafe_allow_html=True)
        with k3:
            st.markdown(kpi("P", "Highest Risk Profile", pct(risk_rate) if pd.notna(risk_rate) else "N/A", f"{count_fmt(risk_count)} employees"), unsafe_allow_html=True)
        with k4:
            st.markdown(kpi("M", "Best Next Fix", str(top_action["Driver"]).replace(" employees", ""), f"+{top_action['Lift']:.1f} pts over baseline"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(answer_card("1", "The headline",
                f"{pct(baseline)} attrition overall; {top_role_count['Job Role']} has the most departures ({count_fmt(top_role_count['leavers'])}).",
                f"The biggest raw loss is in {top_role_count['Job Role']}, while {top_role_rate['Job Role']} has the highest role rate at {pct(top_role_rate['rate'])}. Leadership should start with the role losing the most people because that is where replacement cost and service disruption are largest.",
                f"Run a role-level retention sprint for {top_role_count['Job Role']}: exit-interview themes, manager workload review, and targeted stay interviews for current employees in that role.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("2", "Overtime",
                f"Overtime attrition is {pct(ot_yes)} vs {pct(ot_no)} without overtime, a {ot_gap:.1f} point gap.",
                "Overtime is not a small irritant; it materially raises exit risk and likely signals workload pressure before resignation.",
                "HR should flag teams with recurring overtime, cap repeated mandatory overtime, and require managers to show a staffing or prioritization plan for overloaded teams.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("3", "Remote work",
                f"Remote attrition is {pct(remote_yes)} vs {pct(remote_no)} on-site; only {pct(remote_share)} of employees work remotely.",
                "Remote work appears strongly protective, but the remote group is a minority, so this is evidence for a controlled pilot rather than proof that every role can go remote.",
                "Expand hybrid/remote eligibility first in high-attrition roles, then compare 6-month attrition against similar on-site teams before scaling.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("4", "Pay fairness",
                f"Within job levels, bottom-quartile pay averages about {pay_gap:.1f} points higher attrition than top-quartile pay.",
                "Lower pay within the same level does increase risk, but the benefit flattens after employees move out of the lowest quartile; level and career stage explain more than unlimited pay increases.",
                "Set a minimum competitive pay floor inside each job level and prioritize bottom-quartile adjustments before broad raises.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("5", "The retention timeline",
                f"Highest tenure band: {top_tenure['Tenure Band']} at {pct(top_tenure['rate'])} attrition.",
                "Attrition peaks early-to-mid tenure, not mainly among long-tenure employees. People are deciding whether the company is worth building a career in during the first several years.",
                "Aim retention at onboarding through year 5: stronger 30/60/90 check-ins, first-year manager coaching, and visible internal mobility before employees disengage.",
                ), unsafe_allow_html=True)

        with c2:
            st.markdown(answer_card("6", "Engagement warning signs",
                f"Highest combo: {top_engagement['Job Satisfaction']} satisfaction plus {top_engagement['Work-Life Balance']} WLB at {pct(top_engagement['rate'])}.",
                "The strongest early warning is poor work-life balance paired with low satisfaction; workload stress plus low enthusiasm is a resignation pattern, not just survey noise.",
                "Managers should treat this combination as a red flag and schedule a stay conversation within two weeks, focused on workload, role fit, and one concrete improvement.",
                ), unsafe_allow_html=True)
            if top_life is not None:
                life_stat = f"{top_life['Age Band']}, {top_life['Marital Status']}, {top_life['Dependent Band']} dependents: {pct(top_life['rate'])} attrition."
                life_insight = "Life stage matters most through single status and younger age; this group is mobile, less anchored, and more likely to leave when the job does not quickly offer growth or flexibility."
            else:
                life_stat = "Current filters leave too few employees for a stable life-stage segment."
                life_insight = "The filtered sample is too small for a reliable life-stage conclusion."
            st.markdown(answer_card("7", "Life stage", life_stat, life_insight,
                "Retain this group with fast career paths, schedule flexibility, social belonging, and benefits that support their actual needs rather than one-size-fits-all family benefits.",
                ), unsafe_allow_html=True)
            stuck_stat = f"No promotions: {pct(no_promo)} attrition; 3-4 promotions average {pct(many_promo)}."
            if top_stuck is not None:
                stuck_stat += f" Highest stuck segment: level {top_stuck['Job Level']}, {int(top_stuck['Number of Promotions'])} promotions, leadership {top_stuck['Leadership Opportunities']}, innovation {top_stuck['Innovation Opportunities']} at {pct(top_stuck['rate'])}."
            st.markdown(answer_card("8", "Career stagnation", stuck_stat,
                "Feeling stuck lines up with leaving: employees with few promotions, entry-level status, and no leadership or innovation access are much more likely to exit.",
                "Create a mobility program: quarterly promotion calibration, project-lead rotations, innovation assignments, and published internal paths from Entry to Mid.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("9", "Highest-risk profile",
                f"On-site + Entry + Poor WLB + Single: {pct(risk_rate)} attrition, {risk_lift:.1f} points above baseline, {count_fmt(risk_count)} employees.",
                "This is a large enough population to act on and the attrition level is extreme; it combines low career security, limited flexibility, workload strain, and high mobility.",
                "Build a named intervention list for this group: manager stay interviews, workload reset, remote/hybrid review, and an early-career progression plan.",
                ), unsafe_allow_html=True)
            st.markdown(answer_card("10", "What moves the needle",
                "Top actionable drivers: " + "; ".join([f"{r.Driver}: +{r.Lift:.1f} pts" for r in actionable.head(3).itertuples()]) + ".",
                f"The strongest fixable lever is {top_action['Driver']}. Bringing entry-level attrition down to mid-level levels would reduce attrition by roughly {entry_impact:.1f} percentage points in the current view.",
                "Fix next quarter's biggest lever with a 90-day early-career retention program: manager check-ins, mentors, workload review, clear promotion criteria, and weekly tracking of regretted exits.",
                ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        fig = px.bar(drivers.head(5), x="Lift", y="Driver", orientation="h",
                     color="Lift", color_continuous_scale=SCALE_ATT,
                     text=drivers.head(5)["Lift"].map(lambda v: f"+{v:.1f} pts"),
                     labels={"Lift": "Attrition lift above baseline", "Driver": ""})
        fig.update_traces(textposition="outside")
        fig.update_coloraxes(showscale=False)
        _theme(fig, "Top Attrition Drivers Above Baseline")
        fig.update_layout(height=320, yaxis=dict(autorange="reversed"))
        cw(fig, "qa_driver_lift")


with t_ov:
    pct_lft = n_lft / n_tot * 100 if n_tot else 0
    pct_sty = n_sty / n_tot * 100 if n_tot else 0
    avg_inc = df["Monthly Income"].mean()
    avg_ten = df["Years at Company"].mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, args in zip(
        [c1, c2, c3, c4, c5],
        [("👥","Total Employees",   f"{n_tot:,}",           "Filtered workforce"),
         ("✅","Retention Rate",     f"{pct_sty:.1f}%",      f"{n_sty:,} stayed"),
         ("🚪","Attrition Rate",     f"{pct_lft:.1f}%",      f"{n_lft:,} departed"),
         ("💵","Avg Monthly Income", f"${avg_inc:,.0f}",     "Per employee"),
         ("📅","Avg Tenure",         f"{avg_ten:.1f} yrs",   "Mean years at company")],
    ):
        with col:
            st.markdown(kpi(*args), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📌", "Workforce Attrition at a Glance")

    # Row 1 — Donut + Role bar
    col_a, col_b = st.columns([1, 1.7])
    with col_a:
        cnt = df["Attrition"].value_counts().reset_index()
        cnt.columns = ["Status", "Count"]
        fig = go.Figure(go.Pie(
            labels=cnt["Status"], values=cnt["Count"], hole=0.62,
            marker=dict(colors=[BRAND, RED], line=dict(color="#fff", width=3)),
            textinfo="label+percent",
            textfont=dict(size=12),
            insidetextorientation="radial",
        ))
        # fig.add_annotation(text=f"<b>{pct_lft:.1f}%</b>",
        #                    font=dict(size=26, color=RED), showarrow=False, y=0.06)
        fig.add_annotation(text="attrition",
                           font=dict(size=11, color=NEUTRAL), showarrow=False, y=-0.11)
        _theme(fig, "Overall Attrition — Stayed vs Left")
        fig.update_layout(height=300, margin=dict(t=50, b=10, l=10, r=10))
        cw(fig, "ov_donut")
        insight("Nearly <b>1 in 2</b> employees in this dataset left the organisation — "
                "a critical signal for HR to prioritise retention initiatives immediately.")

    with col_b:
        role_att = (df.groupby("Job Role", observed=True)["Attrition_Num"]
                    .mean().mul(100).reset_index())
        role_att.columns = ["Job Role", "Attrition Rate (%)"]
        role_att = role_att.sort_values("Attrition Rate (%)", ascending=True)
        fig = px.bar(role_att, y="Job Role", x="Attrition Rate (%)", orientation="h",
                     text=role_att["Attrition Rate (%)"].map(lambda v: f"{v:.1f}%"),
                     labels={"Attrition Rate (%)": "Attrition Rate (%)", "Job Role": "Job Role"})
        fig.update_traces(textposition="outside", marker_color=BRAND, marker_line_color="rgba(0,0,0,0)")
        fig.update_layout(height=300)
        _theme(fig, "Attrition Rate by Job Role")
        cw(fig, "ov_role")
        insight("<b>All roles show attrition between 47–49%</b>, suggesting the drivers are "
                "company-wide — not role-specific. Address systemic issues first: "
                "remote work, promotion pathways, and work-life balance.")

    # Row 2 — Income box + Overtime stacked
    col_c, col_d = st.columns(2)
    with col_c:
        df["Tenure Group"] = pd.cut(df["Years at Company"], bins=range(0, 27, 2), right=False)
        tg = (df.groupby("Tenure Group", observed=True)["Attrition_Num"]
              .mean().mul(100).reset_index())
        tg["Midpoint (Years)"] = tg["Tenure Group"].apply(lambda x: x.left + 1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=tg["Midpoint (Years)"], y=tg["Attrition_Num"],
            mode="lines+markers",
            line=dict(color=BRAND, width=2.5),
            marker=dict(color=BRAND_MID, size=7),
            fill="tozeroy", fillcolor="rgba(45,59,224,.08)",
            name="Attrition Rate (%)",
        ))
        _theme(fig, "Attrition Rate vs Years at Company")
        fig.update_layout(height=300,
                          xaxis_title="Years at Company",
                          yaxis_title="Attrition Rate (%)")
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "ov_tenure")
        insight("Attrition is highest in the <b>first two years</b> of employment, "
                "then steadily declines. Focus retention efforts on the critical "
                "0–24 month window with structured onboarding and early check-ins.")
    

    with col_d:
        ot = df.groupby(["Overtime", "Attrition"], observed=True).size().reset_index(name="Count")
        ot["Pct"] = ot["Count"] / ot.groupby("Overtime")["Count"].transform("sum") * 100
        fig = px.bar(ot, x="Overtime", y="Pct", color="Attrition",
                     barmode="stack", color_discrete_map=DISC_ATT,
                     text=ot["Pct"].map(lambda v: f"{v:.0f}%"),
                     labels={"Overtime": "Overtime Required", "Pct": "Share of Employees (%)",
                             "Attrition": "Attrition Status"})
        fig.update_traces(textposition="inside", textfont_color="white",
                          marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Share by Overtime Requirement")
        fig.update_layout(height=300, yaxis_title="Share of Employees (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "ov_ot")
        insight("Employees required to work overtime have a <b>~6% higher attrition rate</b>. "
                "Capping mandatory overtime and offering compensatory time are high-value quick wins.")

    # Row 3 — Satisfaction grouped + Job Level funnel
    col_e, col_f = st.columns([1.4, 1])
    with col_e:
        rows = []
        for dim, col_n in [("Job Satisfaction", "JS_N"),
                           ("Work-Life Balance", "WLB_N"),
                           ("Employee Recognition", "REC_N")]:
            for status in ["Stayed", "Left"]:
                rows.append({"Dimension": dim, "Attrition Status": status,
                             "Average Score (1–4)": df[df["Attrition"] == status][col_n].mean()})
        sat = pd.DataFrame(rows)
        fig = px.bar(sat, x="Dimension", y="Average Score (1–4)", color="Attrition Status",
                     barmode="group", color_discrete_map=DISC_ATT,
                     text=sat["Average Score (1–4)"].map(lambda v: f"{v:.2f}"))
        fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig.update_layout(height=300, yaxis=dict(range=[0, 4.5]))
        _theme(fig, "Satisfaction Scores — Stayed vs Left (Scale: 1 Low → 4 High)")
        cw(fig, "ov_sat")
        insight("Leavers score <b>lower on all three satisfaction dimensions</b>. "
                "Job Satisfaction shows the widest gap — a targeted engagement programme "
                "for dissatisfied employees could meaningfully reduce turnover.")

    with col_f:
        lvl_att = (df.groupby("Job Level", observed=True)["Attrition_Num"]
                   .mean().mul(100).reset_index())
        lvl_att.columns = ["Job Level", "Attrition Rate (%)"]
        lvl_att = lvl_att.sort_values("Attrition Rate (%)", ascending=False)
        colors_funnel = {
            "Entry":  RED,
            "Mid":    BRAND,
            "Senior": GREEN,
        }
        fig = go.Figure(go.Funnel(
            y=lvl_att["Job Level"],
            x=lvl_att["Attrition Rate (%)"],
            textposition="inside",
            texttemplate="%{value:.1f}%",
            marker=dict(color=[colors_funnel.get(v, BRAND) for v in lvl_att["Job Level"]]),
            connector=dict(line=dict(color="rgba(45,59,224,.18)", width=1)),
        ))
        _theme(fig, "Attrition Rate by Job Level")
        fig.update_layout(height=300)
        cw(fig, "ov_funnel")
        insight("Entry-level employees leave at <b>3× the rate of Senior staff</b>. "
                "Invest in onboarding, mentoring, and clear promotion pathways "
                "to retain early-career talent.")



# ════════════════════════════════════════════════════════════════════════════
#  TAB 2 — DIAGNOSTIC
# ════════════════════════════════════════════════════════════════════════════
with t_dx:
    sec("🔎", "Risk Driver Analysis")

    # Row 1 — Overtime × Marital heatmap + Bubble
    col_a, col_b = st.columns(2)
    with col_a:
        hm = (df.groupby(["Overtime", "Marital Status"], observed=True)["Attrition_Num"]
              .mean().mul(100).unstack(fill_value=0))
        # reorder columns
        for col_ord in [["Divorced","Married","Single"]]:
            hm = hm.reindex(columns=col_ord, fill_value=0)
        fig = go.Figure(go.Heatmap(
            z=hm.values, x=hm.columns.tolist(), y=hm.index.tolist(),
            colorscale=SCALE_ATT,
            text=np.round(hm.values, 1), texttemplate="%{text:.1f}%",
            textfont=dict(color="#1a202c", size=13), showscale=True,
            colorbar=dict(title=dict(text="Attrition %", font=dict(color="#4a5568")),
                          tickfont=dict(color="#4a5568")),
        ))
        _theme(fig, "Attrition Rate — Overtime × Marital Status")
        fig.update_layout(height=300,
                          xaxis_title="Marital Status",
                          yaxis_title="Overtime Required")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_hm")
        insight("Single employees working overtime have the <b>highest attrition</b>. "
                "They have the most flexibility to leave. Consider overtime-reduction "
                "policies and social engagement programmes for this group.")

    with col_b:
        bub = (df.groupby(["Job Role", "Job Level"], observed=True)
               .agg(Rate=("Attrition_Num", "mean"), Lost=("Attrition_Num", "sum"))
               .reset_index())
        bub["Attrition Rate (%)"] = bub["Rate"] * 100
        fig = px.scatter(bub, x="Job Role", y="Job Level",
                         size="Lost", color="Attrition Rate (%)",
                         color_continuous_scale=SCALE_ATT, size_max=55,
                         hover_name="Job Role",
                         hover_data={"Lost": True, "Attrition Rate (%)": ":.1f",
                                     "Job Role": False, "Job Level": False},
                         labels={"Lost": "Employees Lost", "Job Level": "Job Level",
                                 "Job Role": "Job Role"})
        fig.update_coloraxes(
            colorbar=dict(title=dict(text="Attrition Rate (%)", font=dict(color="#4a5568")),
                          tickfont=dict(color="#4a5568")))
        _theme(fig, "Attrition Intensity — Role × Level  (bubble size = employees lost)")
        fig.update_layout(height=300)
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_bubble")
        insight("Entry-level employees across all roles show the largest and darkest bubbles. "
                "<b>No single role is safe</b> — the problem is structural, not departmental.")

    # Row 2 — Job Satisfaction stacked + Distance violin
    col_c, col_d = st.columns(2)
    with col_c:
        js = (df.groupby(["Job Satisfaction", "Attrition"], observed=True)
              .size().reset_index(name="Count"))
        js["Pct"] = js["Count"] / js.groupby("Job Satisfaction")["Count"].transform("sum") * 100
        fig = px.bar(js, x="Job Satisfaction", y="Pct", color="Attrition",
                     barmode="stack", color_discrete_map=DISC_ATT,
                     text=js["Pct"].map(lambda v: f"{v:.0f}%"),
                     labels={"Job Satisfaction": "Job Satisfaction Level",
                             "Pct": "Share of Employees (%)",
                             "Attrition": "Attrition Status"},
                     category_orders={"Job Satisfaction": ["Low","Medium","High","Very High"]})
        fig.update_traces(textposition="inside", textfont_color="white",
                          marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Share by Job Satisfaction Level")
        fig.update_layout(height=300, yaxis_title="Share of Employees (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_js")
        insight("Employees with <b>Low job satisfaction have the highest attrition</b>. "
                "Surprisingly, 'Very High' also shows elevated turnover — possibly top "
                "performers being poached. Run exit interviews to distinguish the two groups.")

    with col_d:
        fig = go.Figure()
        for status, color in [("Stayed", BRAND), ("Left", RED)]:
            sub = df[df["Attrition"] == status]["Distance from Home"]
            r, g, b_ = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            fig.add_trace(go.Violin(
                y=sub, name=status, box_visible=True, meanline_visible=True,
                fillcolor=f"rgba({r},{g},{b_},.22)",
                line_color=color, points="outliers",
                marker=dict(color=color, size=3),
            ))
        _theme(fig, "Distance from Home — Stayed vs Left")
        fig.update_layout(height=300,
                          yaxis_title="Distance from Home (km)",
                          legend_title_text="Attrition Status")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_violin")
        insight("Employees who left tend to live <b>farther from the office</b>. "
                "Remote work or commuter subsidies would directly address this friction point.")

    # Row 3 — Remote × Leadership + Promotions scatter
    col_e, col_f = st.columns(2)
    with col_e:
        rem = (df.groupby(["Remote Work", "Leadership Opportunities"], observed=True)
               ["Attrition_Num"].mean().mul(100).reset_index())
        rem.columns = ["Remote Work", "Leadership Opportunities", "Attrition Rate (%)"]
        fig = px.bar(rem, x="Remote Work", y="Attrition Rate (%)",
                     color="Leadership Opportunities",
                     barmode="group",
                     color_discrete_map={"No": RED, "Yes": BRAND},
                     text=rem["Attrition Rate (%)"].map(lambda v: f"{v:.1f}%"),
                     labels={"Remote Work": "Remote Work Allowed",
                             "Attrition Rate (%)": "Attrition Rate (%)",
                             "Leadership Opportunities": "Leadership Opportunities"})
        fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Rate — Remote Work × Leadership Opportunities")
        fig.update_layout(height=300)
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_rem")
        insight("Remote workers with leadership opportunities have the <b>lowest attrition</b>. "
                "Combining flexible work with growth opportunities is a powerful retention formula.")

    with col_f:
        pg = (df.groupby("Number of Promotions", observed=True)
              .agg(Rate=("Attrition_Num", "mean"), Count=("Attrition_Num", "size"))
              .reset_index())
        pg["Attrition Rate (%)"] = pg["Rate"] * 100
        fig = px.scatter(pg, x="Number of Promotions", y="Attrition Rate (%)",
                         size="Count", color="Attrition Rate (%)",
                         color_continuous_scale=SCALE_ATT,
                         trendline="ols", size_max=50,
                         labels={"Count": "Employee Count",
                                 "Number of Promotions": "Number of Promotions Received"})
        fig.update_traces(selector=dict(mode="lines"),
                          line=dict(color=AMBER, dash="dash", width=2),
                          name="Trend line", showlegend=True)
        fig.update_coloraxes(showscale=False)
        _theme(fig, "Attrition Rate vs Number of Promotions Received")
        fig.update_layout(height=300,
                          xaxis_title="Number of Promotions Received",
                          yaxis_title="Attrition Rate (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_promo")
        insight("<b>3+ promotions halves the attrition rate</b>. "
                "A structured, bi-annual promotion review with transparent criteria "
                "is one of the strongest retention investments HR can make.")

    # Row 4 — Performance Rating + Company Reputation
    col_g, col_h = st.columns(2)
    with col_g:
        pr = (df.groupby(["Performance Rating", "Attrition"], observed=True)
              .size().reset_index(name="Count"))
        pr["Pct"] = pr["Count"] / pr.groupby("Performance Rating")["Count"].transform("sum") * 100
        fig = px.bar(pr, x="Performance Rating", y="Pct", color="Attrition",
                     barmode="group", color_discrete_map=DISC_ATT,
                     text=pr["Pct"].map(lambda v: f"{v:.0f}%"),
                     labels={"Performance Rating": "Performance Rating",
                             "Pct": "Share within Rating (%)",
                             "Attrition": "Attrition Status"},
                     category_orders={"Performance Rating": ["Low","Below Average","Average","High"]})
        fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Share by Performance Rating")
        fig.update_layout(height=300, yaxis_title="Share within Rating (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_perf")
        insight("<b>Low-rated employees leave most</b> — likely disengaged or mismatched. "
                "Pair performance reviews with coaching, not just evaluation, "
                "to address root causes before the exit decision is made.")

    with col_h:
        rep = (df.groupby("Company Reputation", observed=True)["Attrition_Num"]
               .mean().mul(100).reset_index())
        rep.columns = ["Company Reputation", "Attrition Rate (%)"]
        fig = go.Figure(go.Bar(
            x=rep["Company Reputation"],
            y=rep["Attrition Rate (%)"],
            marker=dict(
                color=BRAND,
                line=dict(color="rgba(0,0,0,0)"),
            ),
            text=[f"{v:.1f}%" for v in rep["Attrition Rate (%)"]],
            textposition="outside",
        ))
        _theme(fig, "Attrition Rate by Perceived Company Reputation")
        fig.update_layout(height=300,
                          xaxis_title="Perceived Company Reputation",
                          yaxis_title="Attrition Rate (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dx_rep")
        insight("Employees who rate company reputation as <b>Poor leave at 56%</b> — "
                "almost 13 percentage points above Excellent reputation companies. "
                "Invest in employer branding, leadership transparency, and employee voice programmes.")


# ════════════════════════════════════════════════════════════════════════════
#  TAB 3 — DEMOGRAPHIC
# ════════════════════════════════════════════════════════════════════════════
with t_dm:
    sec("👥", "Workforce Demographics & Attrition Patterns")

    col_a, col_b = st.columns([1.6, 1])
    with col_a:
        fig = go.Figure()
        for status, color in [("Stayed", BRAND), ("Left", RED)]:
            sub = df[df["Attrition"] == status]["Age"]
            r, g, b_ = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            fig.add_trace(go.Histogram(
                x=sub, name=status,
                marker_color=color, opacity=0.72,
                xbins=dict(start=18, end=62, size=2),
                marker_line_color="rgba(0,0,0,0)",
            ))
        _theme(fig, "Age Distribution of Employees — Stayed vs Left")
        fig.update_layout(barmode="overlay", height=300,
                          xaxis_title="Age (years)",
                          yaxis_title="Number of Employees",
                          legend_title_text="Attrition Status")
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dm_agehist")
        insight("The youngest employees (18–30) show <b>the highest attrition volumes</b>. "
                "Early-career workers need visible growth paths to stay motivated.")

    with col_b:
        gc = df.groupby("Gender", observed=True).size().reset_index(name="Count")
        fig = px.pie(gc, names="Gender", values="Count", hole=0.55,
                     color_discrete_map={"Male": BRAND, "Female": "#A855F7"},
                     labels={"Gender": "Gender"})
        fig.update_traces(textfont_size=12, textinfo="label+percent",
                          marker=dict(line=dict(color="#fff", width=3)))
        _theme(fig, "Workforce Gender Split")
        fig.update_layout(height=300)
        cw(fig, "dm_gender")
        insight("The dataset is broadly gender-balanced. "
                "Track attrition <b>by gender × role</b> (see heatmap below) "
                "to catch hidden equity gaps.")

    col_c, col_d = st.columns(2)
    with col_c:
        ab = (df.groupby("Age Group", observed=True)["Attrition_Num"]
              .mean().mul(100).reset_index())
        ab.columns = ["Age Group", "Attrition Rate (%)"]
        fig = px.bar(ab, x="Age Group", y="Attrition Rate (%)",
                     text=ab["Attrition Rate (%)"].map(lambda v: f"{v:.1f}%"),
                     labels={"Age Group": "Age Group", "Attrition Rate (%)": "Attrition Rate (%)"})
        fig.update_traces(textposition="outside", marker_color=BRAND, marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Rate by Age Group")
        fig.update_layout(height=300, yaxis_title="Attrition Rate (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dm_ageband")
        insight("The 18–25 age group has the <b>highest attrition rate</b>. "
                "Structured mentoring, early career development, and competitive entry "
                "salaries are critical retention tools for this cohort.")

    with col_d:
        ms = (df.groupby(["Marital Status", "Attrition"], observed=True)
              .size().reset_index(name="Count"))
        ms["Pct"] = ms["Count"] / ms.groupby("Marital Status")["Count"].transform("sum") * 100
        fig = px.bar(ms, x="Marital Status", y="Pct", color="Attrition",
                     barmode="stack", color_discrete_map=DISC_ATT,
                     text=ms["Pct"].map(lambda v: f"{v:.0f}%"),
                     labels={"Marital Status": "Marital Status",
                             "Pct": "Share of Group (%)",
                             "Attrition": "Attrition Status"})
        fig.update_traces(textposition="inside", textfont_color="white",
                          marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Share by Marital Status")
        fig.update_layout(height=300, yaxis_title="Share of Group (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dm_ms")
        insight("<b>Divorced employees show the highest attrition</b>. "
                "Personal life transitions often coincide with career moves — "
                "targeted wellbeing support for this group could improve retention.")

    col_e, col_f = st.columns(2)
    with col_e:
        edu = (df.groupby("Education Level", observed=True)["Attrition_Num"]
               .mean().mul(100).reset_index())
        edu.columns = ["Education Level", "Attrition Rate (%)"]
        fig = px.bar(edu, y="Education Level", x="Attrition Rate (%)", orientation="h",
                     color="Attrition Rate (%)",
                     color_continuous_scale=SCALE_ATT,
                     text=edu["Attrition Rate (%)"].map(lambda v: f"{v:.1f}%"),
                     labels={"Education Level": "Highest Education Level",
                             "Attrition Rate (%)": "Attrition Rate (%)"},
                     category_orders={"Education Level":
                         ["High School","Associate Degree","Bachelor's Degree",
                          "Master's Degree","PhD"]})
        fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        fig.update_coloraxes(showscale=False)
        _theme(fig, "Attrition Rate by Education Level")
        fig.update_layout(height=320)
        fig.update_yaxes(tickangle=-20)
        cw(fig, "dm_edu")
        insight("Education level alone is not a strong predictor of attrition — "
                "rates are relatively uniform. Focus on <b>role–education fit</b> "
                "and ensure qualifications are being used in assigned roles.")

    with col_f:
        dep = (df.groupby(["Number of Dependents", "Attrition"], observed=True)
               .size().reset_index(name="Count"))
        dep["Pct"] = dep["Count"] / dep.groupby("Number of Dependents")["Count"].transform("sum") * 100
        fig = px.bar(dep, x="Number of Dependents", y="Pct", color="Attrition",
                     barmode="group", color_discrete_map=DISC_ATT,
                     text=dep["Pct"].map(lambda v: f"{v:.0f}%"),
                     labels={"Number of Dependents": "Number of Dependents",
                             "Pct": "Share of Group (%)",
                             "Attrition": "Attrition Status"})
        fig.update_traces(textposition="outside", marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Share by Number of Dependents")
        fig.update_layout(height=320, yaxis_title="Share of Group (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dm_dep")
        insight("Employees with <b>no dependents</b> leave at slightly higher rates, "
                "consistent with greater personal mobility. "
                "Financial benefits like childcare support can anchor employees with families.")

    col_g, col_h = st.columns(2)
    with col_g:
        gr = (df.groupby(["Gender", "Job Role"], observed=True)["Attrition_Num"]
              .mean().mul(100).unstack(fill_value=0))
        fig = go.Figure(go.Heatmap(
            z=gr.values, x=gr.columns.tolist(), y=gr.index.tolist(),
            colorscale=SCALE_ATT,
            text=np.round(gr.values, 1), texttemplate="%{text:.1f}%",
            textfont=dict(color="#1a202c", size=12), showscale=True,
            colorbar=dict(title=dict(text="Attrition Rate (%)", font=dict(color="#4a5568")),
                          tickfont=dict(color="#4a5568")),
        ))
        _theme(fig, "Attrition Rate — Gender × Job Role")
        fig.update_layout(height=300,
                          xaxis_title="Job Role",
                          yaxis_title="Gender")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))

        cw(fig, "dm_grhm")
        insight("Attrition rates are <b>broadly similar across genders within each role</b> — "
                "no single role shows a stark gender gap. "
                "Continue monitoring to catch emerging equity issues early.")

    with col_h:
        fig = px.box(df, x="Job Role", y="Age", color="Attrition",
                     color_discrete_map=DISC_ATT, notched=False,
                     labels={"Job Role": "Job Role", "Age": "Age (years)",
                             "Attrition": "Attrition Status"})
        fig.update_traces(marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Age Range by Job Role and Attrition Status")
        fig.update_layout(height=300, yaxis_title="Age (years)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "dm_agebox")
        insight("Leavers skew <b>younger than stayers</b> across almost every job role. "
                "The 18–30 window is where HR has the most leverage to intervene.")


# ════════════════════════════════════════════════════════════════════════════
#  TAB 4 — FINANCIAL
# ════════════════════════════════════════════════════════════════════════════
with t_fi:
    sec("💲", "Compensation & Financial Retention Signals")

    avg_all   = df["Monthly Income"].mean()
    ai_lft    = df[df["Attrition"] == "Left"]["Monthly Income"].mean()
    ai_sty    = df[df["Attrition"] == "Stayed"]["Monthly Income"].mean()
    gap_val   = ai_sty - ai_lft
    pct_no_p  = (df["Number of Promotions"] == 0).mean() * 100

    fc1, fc2, fc3, fc4 = st.columns(4)
    for col, args in zip(
        [fc1, fc2, fc3, fc4],
        [("💵","Avg Income — Left",   f"${ai_lft:,.0f}",  "Monthly average"),
         ("✅","Avg Income — Stayed",  f"${ai_sty:,.0f}",  "Monthly average"),
         ("📈","Income Gap",           f"${gap_val:,.0f}", "Stayed − Left monthly"),
         ("🏅","Never Promoted",       f"{pct_no_p:.1f}%", "Share of workforce")],
    ):
        with col:
            st.markdown(kpi(*args), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        ib = (df.groupby("Income Band", observed=True)["Attrition_Num"]
              .mean().mul(100).reset_index())
        ib.columns = ["Income Band", "Attrition Rate (%)"]
        fig = px.bar(ib, x="Income Band", y="Attrition Rate (%)",
                     text=ib["Attrition Rate (%)"].map(lambda v: f"{v:.1f}%"),
                     labels={"Income Band": "Monthly Income Band",
                             "Attrition Rate (%)": "Attrition Rate (%)"},
                     category_orders={"Income Band": ["< $4k","$4k–$7k","$7k–$10k","$10k+"]})
        fig.update_traces(textposition="outside", marker_color=BRAND, marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Attrition Rate by Monthly Income Band")
        fig.update_layout(height=300, yaxis_title="Attrition Rate (%)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_ib")
        insight("The <b>lowest income band (&lt;$4k/month) has the highest attrition</b>. "
                "A targeted salary floor increase for this group would have an outsized retention effect.")

    with col_b:
        fig = px.box(df, x="Job Level", y="Monthly Income", color="Attrition",
                     color_discrete_map=DISC_ATT, notched=True,
                     labels={"Job Level": "Job Level", "Monthly Income": "Monthly Income (USD)",
                             "Attrition": "Attrition Status"},
                     category_orders={"Job Level": ["Entry","Mid","Senior"]})
        fig.update_traces(marker_line_color="rgba(0,0,0,0)")
        _theme(fig, "Monthly Income Distribution by Job Level and Attrition Status")
        fig.update_layout(height=300, yaxis_title="Monthly Income (USD)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_lvlbox")
        insight("At <b>every job level, leavers earned less than stayers</b>. "
                "Pay equity audits at each level — not just in aggregate — are essential.")

    col_c, col_d = st.columns([1.6, 1])
    with col_c:
        samp = df.sample(min(3000, len(df)), random_state=42)
        fig = px.scatter(samp, x="Company Tenure", y="Monthly Income",
                         color="Attrition", color_discrete_map=DISC_ATT,
                         opacity=0.50, trendline="lowess",
                         hover_data={"Age": True, "Job Role": True,
                                     "Job Level": True, "Company Tenure": False},
                         labels={"Company Tenure": "Time at Company (months)",
                                 "Monthly Income": "Monthly Income (USD)",
                                 "Attrition": "Attrition Status"})
        fig.update_traces(marker=dict(size=4), selector=dict(mode="markers"))
        fig.update_traces(selector=dict(mode="lines"), line=dict(width=2.5))
        _theme(fig, "Monthly Income vs Time at Company — Sample of 3,000 Employees")
        fig.update_layout(height=340,
                          xaxis_title="Time at Company (months)",
                          yaxis_title="Monthly Income (USD)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_scatter")
        insight("Leavers cluster in the <b>low-income, low-tenure</b> quadrant. "
                "Employees who stay longer tend to earn more — a positive signal "
                "that compensation growth is rewarding loyalty.")

    with col_d:
        ri = df.groupby("Job Role", observed=True)["Monthly Income"].mean().sort_values()
        bar_colors = [RED if v < avg_all else BRAND for v in ri.values]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=ri.index, x=ri.values, orientation="h",
            marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0)")),
            text=[f"${v:,.0f}" for v in ri.values],
            textposition="outside",
            name="Avg Monthly Income",
        ))
        fig.add_vline(x=avg_all, line_color=AMBER, line_dash="dash", line_width=1.8,
                      annotation=dict(text=f"Company avg ${avg_all:,.0f}",
                                      font=dict(color=AMBER, size=10),
                                      xanchor="left"))
        # Manual legend for color meaning
        fig.add_trace(go.Bar(x=[None], y=[None], marker_color=RED,  name="Below company average"))
        fig.add_trace(go.Bar(x=[None], y=[None], marker_color=BRAND, name="Above company average"))
        _theme(fig, "Average Monthly Income by Job Role vs Company Average")
        fig.update_layout(height=340, xaxis_title="Average Monthly Income (USD)",
                          showlegend=True)
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_roleinc")
        insight("Roles <b>below the company average</b> (in red) are prime candidates for "
                "pay benchmarking studies. Closing these gaps is a measurable, "
                "targeted retention intervention.")

    col_e, col_f = st.columns(2)
    with col_e:
        pi = (df.groupby(["Number of Promotions", "Job Level"], observed=True)
              ["Monthly Income"].mean().unstack(fill_value=0))
        pi = pi.reindex(columns=["Entry","Mid","Senior"], fill_value=0)
        fig = go.Figure(go.Heatmap(
            z=pi.values.round(0), x=pi.columns.tolist(),
            y=[str(int(x)) for x in pi.index.tolist()],
            colorscale=SCALE_INC,
            text=pi.values.round(0), texttemplate="$%{text:,.0f}",
            textfont=dict(color="#1a202c", size=11), showscale=True,
            colorbar=dict(title=dict(text="Avg Income (USD)", font=dict(color="#4a5568")),
                          tickfont=dict(color="#4a5568")),
        ))
        _theme(fig, "Average Monthly Income — Promotions Received × Job Level")
        fig.update_layout(height=300,
                          xaxis_title="Job Level",
                          yaxis_title="Number of Promotions Recv")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_prhm")
        insight("<b>Income rises with promotions</b> — but only modestly at Entry level. "
                "Ensure promotion cycles are accompanied by meaningful salary uplifts "
                "to make advancement financially worthwhile.")

    with col_f:
        wi = (df.groupby("Work-Life Balance", observed=True)
              ["Monthly Income"].mean().reset_index())
        wi.columns = ["Work-Life Balance", "Average Monthly Income (USD)"]
        fig = go.Figure(go.Scatter(
            x=wi["Work-Life Balance"].astype(str),
            y=wi["Average Monthly Income (USD)"],
            mode="lines+markers",
            line=dict(color=BRAND, width=3),
            marker=dict(color=BRAND_MID, size=10, line=dict(color=BRAND_DARK, width=2)),
            fill="tozeroy", fillcolor="rgba(45,59,224,.07)",
            name="Avg Monthly Income",
        ))
        _theme(fig, "Average Monthly Income by Work-Life Balance Rating")
        fig.update_layout(height=300,
                          xaxis_title="Work-Life Balance Rating  (Poor → Excellent)",
                          yaxis_title="Average Monthly Income (USD)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        fig.update_xaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_wlb")
        insight("Higher earners report <b>better work-life balance</b>. "
                "This may be because senior/higher-paid roles offer more autonomy and flexibility. "
                "Extend flexible working to lower pay bands too.")

    col_g, col_h = st.columns(2)
    with col_g:
        fig = px.violin(df, x="Company Size", y="Monthly Income", color="Attrition",
                        color_discrete_map=DISC_ATT, box=True, points=False,
                        labels={"Company Size": "Company Size",
                                "Monthly Income": "Monthly Income (USD)",
                                "Attrition": "Attrition Status"},
                        category_orders={"Company Size": ["Small","Medium","Large"]})
        _theme(fig, "Monthly Income Distribution by Company Size and Attrition Status")
        fig.update_layout(height=300, yaxis_title="Monthly Income (USD)")
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_csviolin")
        insight("Income distributions are <b>similar across company sizes</b>, "
                "suggesting company size itself is not the primary financial retention driver — "
                "role and level matter more.")

    with col_h:
        il = (df.groupby(["Innovation Opportunities", "Leadership Opportunities"], observed=True)
              ["Monthly Income"].mean().unstack(fill_value=0))
        fig = go.Figure(go.Heatmap(
            z=il.values.round(0),
            x=[f"Leadership: {v}" for v in il.columns.tolist()],
            y=[f"Innovation: {v}" for v in il.index.tolist()],
            colorscale=SCALE_INC,
            text=il.values.round(0), texttemplate="$%{text:,.0f}",
            textfont=dict(color="#1a202c", size=13), showscale=True,
            colorbar=dict(title=dict(text="Avg Income (USD)", font=dict(color="#4a5568")),
                          tickfont=dict(color="#4a5568")),
        ))
        _theme(fig, "Average Monthly Income — Innovation × Leadership Opportunities")
        fig.update_layout(height=300)
        fig.update_yaxes(title_font=dict(color="#000000"), tickfont=dict(color="#000000"))
        cw(fig, "fi_ilhm")
        insight("Employees with <b>both innovation and leadership opportunities earn the most</b>. "
                "These employees also have lower attrition — reinforcing that "
                "growth opportunities and compensation work as a combined retention package.")


# ════════════════════════════════════════════════════════════════════════════
#  TAB 5 — SUGGESTIONS
# ════════════════════════════════════════════════════════════════════════════
with t_sg:
    # Header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{BRAND_DARK} 0%,{BRAND} 100%);
                border-radius:18px;padding:26px 32px;margin-bottom:1.4rem;
                display:flex;align-items:center;gap:20px;
                box-shadow:0 8px 32px rgba(45,59,224,.28);">
        <div style="width:76px;height:76px;background:#fff;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 6px 18px rgba(0,0,0,.14);">
            {logo(64)}
        </div>
        <div>
            <div style="font-size:1.25rem;font-weight:800;color:#fff;line-height:1.2;">
                Data-Driven Retention Recommendations
            </div>
            <div style="font-size:.76rem;color:rgba(255,255,255,.62);margin-top:5px;">
                Actionable strategies derived from attrition pattern analysis · 74,498 employee records
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Legend
    st.markdown(f"""
    <div style="display:flex;gap:18px;margin-bottom:1.1rem;flex-wrap:wrap;align-items:center;">
        <span style="font-size:.72rem;color:#4a5568;font-weight:700;letter-spacing:.04em;text-transform:uppercase;">Priority:</span>
        <span style="display:flex;align-items:center;gap:6px;font-size:.74rem;color:#4a5568;font-weight:600;">
            <span class="ldot" style="background:{RED};"></span>Urgent — Highest Impact
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:.74rem;color:#4a5568;font-weight:600;">
            <span class="ldot" style="background:{AMBER};"></span>Medium Priority
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:.74rem;color:#4a5568;font-weight:600;">
            <span class="ldot" style="background:{GREEN};"></span>Quick Win
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── URGENT ──────────────────────────────────────────────────────────────
    sec("🚨", "Urgent — Highest Impact Actions")

    ug1, ug2 = st.columns(2)
    with ug1:
        st.markdown("""
        <div class="sug-card urg">
            <div class="sug-hdr">
                <span style="font-size:1.35rem;">🏠</span>
                <span class="sug-badge b-urg">Urgent</span>
                <span class="sug-title">Expand Remote Work Policy</span>
            </div>
            <div class="sug-stat">📊 Remote: 24.7% attrition &nbsp;|&nbsp; On-site: 52.8% attrition</div>
            <div class="sug-body">
                On-site employees leave at <b>more than twice the rate</b> of remote workers.
                Introduce a hybrid or remote-first policy for eligible roles — especially in
                Technology and Finance. Even 2–3 WFH days per week reduces commute fatigue
                and improves retention at mid and entry levels.
                <br><br>
                <b>Action:</b> Run a pilot hybrid programme across the highest-attrition roles,
                measure 6-month attrition change, then scale.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sug-card urg">
            <div class="sug-hdr">
                <span style="font-size:1.35rem;">📉</span>
                <span class="sug-badge b-urg">Urgent</span>
                <span class="sug-title">Address Entry-Level Attrition Crisis</span>
            </div>
            <div class="sug-stat">📊 Entry-level attrition: 63.3% — 3× the Senior rate of 20%</div>
            <div class="sug-body">
                Nearly two-thirds of entry-level employees leave. Implement a structured
                <b>90-day onboarding programme</b>, assign peer mentors to all new hires,
                and conduct 30/60/90-day check-ins. Build clear career ladders showing
                a visible path to Mid and Senior levels within 18–24 months.
                <br><br>
                <b>Action:</b> Appoint an Onboarding Experience Owner in HR and measure
                first-year attrition quarterly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ug2:
        st.markdown("""
        <div class="sug-card urg">
            <div class="sug-hdr">
                <span style="font-size:1.35rem;">⚖️</span>
                <span class="sug-badge b-urg">Urgent</span>
                <span class="sug-title">Fix Work-Life Balance & Overtime Load</span>
            </div>
            <div class="sug-stat">📊 Poor WLB: 60.2% attrition &nbsp;|&nbsp; Overtime workers: 51.5%</div>
            <div class="sug-body">
                Employees with poor work-life balance and overtime requirements leave at
                the highest rates in the dataset. Cap mandatory overtime, introduce
                <b>flex-time scheduling</b>, and offer compensatory days.
                Actively monitor team workloads through manager dashboards.
                <br><br>
                <b>Action:</b> Identify the 20% of teams with the highest overtime usage
                and implement a workload redistribution review within 30 days.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sug-card urg">
            <div class="sug-hdr">
                <span style="font-size:1.35rem;">🏆</span>
                <span class="sug-badge b-urg">Urgent</span>
                <span class="sug-title">Create a Structured Promotion Pathway</span>
            </div>
            <div class="sug-stat">📊 3–4 promotions: 23–25% attrition vs 49% with zero promotions</div>
            <div class="sug-body">
                Employees with 3–4 promotions have <b>half the attrition rate</b>.
                Launch a bi-annual promotion review cycle with transparent criteria.
                Introduce micro-promotions (title upgrades, scope expansion) to signal
                growth even when budget limits large salary increases.
                <br><br>
                <b>Action:</b> Audit current promotion frequency by department —
                flag any team with zero promotions in the past 18 months.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── MEDIUM ───────────────────────────────────────────────────────────────
    sec("⚠️", "Medium Priority — Structural Improvements")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">🌟</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Strengthen Company Reputation</span>
            </div>
            <div class="sug-stat">📊 Poor reputation: 56.0% attrition vs 44.0% for Excellent</div>
            <div class="sug-body">
                Invest in employer branding via transparent leadership communication,
                Glassdoor response management, and employee advocacy programmes.
                Share company wins publicly and involve employees in decisions
                that affect their work.
                <br><br>
                <b>Action:</b> Assign a monthly "Reputation Pulse" score using
                exit interview themes and Glassdoor trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">📈</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Raise the Compensation Floor</span>
            </div>
            <div class="sug-stat">📊 &lt; $4k/month income band has the highest attrition tier</div>
            <div class="sug-body">
                Benchmark the lowest income band against market rates.
                Even a 10–15% uplift to the bottom quartile earners can have an outsized
                retention effect — and costs less than rehiring and retraining.
                <br><br>
                <b>Action:</b> Commission a salary benchmarking study for Entry and
                low-Mid roles within the next quarter.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">💡</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Support Low Performers Before They Leave</span>
            </div>
            <div class="sug-stat">📊 Low performance rating: 57.1% attrition rate</div>
            <div class="sug-body">
                Low-rated employees leave at the highest rate — likely due to disengagement
                or role mismatch. Pair performance reviews with <b>personalised coaching plans</b>,
                not just evaluations. Identify whether the cause is a skill gap or motivational issue.
                <br><br>
                <b>Action:</b> Mandate a coaching conversation alongside every below-average
                performance rating.
            </div>
        </div>
        """, unsafe_allow_html=True)

    m4, m5, m6 = st.columns(3)
    with m4:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">✈️</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Reduce Unnecessary Business Travel</span>
            </div>
            <div class="sug-stat">📊 Frequent travellers show ~25% higher attrition risk</div>
            <div class="sug-body">
                Replace discretionary travel with high-quality video conferencing.
                For essential travel, introduce <b>recovery days</b> post-trip and
                give employees input into their own travel schedules.
                <br><br>
                <b>Action:</b> Require manager sign-off for any travel over 2 consecutive
                weeks and track travel-to-attrition correlation quarterly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">🎯</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Open Up Leadership Opportunities</span>
            </div>
            <div class="sug-stat">📊 Leadership access reduces attrition by ~3 percentage points</div>
            <div class="sug-body">
                Create <b>project lead roles, working groups, and internal committees</b>
                open to all job levels. This signals investment in the employee's future
                and builds the leadership pipeline at the same time.
                <br><br>
                <b>Action:</b> Ensure every team has at least one open leadership
                opportunity listed internally each quarter.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m6:
        st.markdown("""
        <div class="sug-card med">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">🔬</span>
                <span class="sug-badge b-med">Medium</span>
                <span class="sug-title">Foster a Culture of Innovation</span>
            </div>
            <div class="sug-stat">📊 Innovation access reduces attrition by ~3 percentage points</div>
            <div class="sug-body">
                Offer <b>internal hackathons, innovation labs, and 10% personal project time</b>.
                Intellectually challenged employees seek stimulation less elsewhere —
                especially impactful in Technology and Healthcare.
                <br><br>
                <b>Action:</b> Run a quarterly Innovation Challenge — open to all departments,
                with a small prize fund and exec sponsorship.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── QUICK WINS ───────────────────────────────────────────────────────────
    sec("✅", "Quick Wins — Low Effort, Measurable Impact")

    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown("""
        <div class="sug-card win">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">🎖️</span>
                <span class="sug-badge b-win">Quick Win</span>
                <span class="sug-title">Launch an Employee Recognition Programme</span>
            </div>
            <div class="sug-stat">📊 Recognition level consistently linked to retention across all roles</div>
            <div class="sug-body">
                Implement a <b>monthly peer and manager recognition system</b> —
                "Employee of the Month", team shout-outs, and small rewards.
                Low cost, high visibility. Train managers to make recognition
                specific, timely, and sincere.
                <br><br>
                <b>Action:</b> Deploy a recognition tool (e.g. Bonusly, Kudos)
                in 30 days and track participation monthly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with q2:
        st.markdown("""
        <div class="sug-card win">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">📋</span>
                <span class="sug-badge b-win">Quick Win</span>
                <span class="sug-title">Run Quarterly Pulse Surveys</span>
            </div>
            <div class="sug-stat">📊 Leavers score lower on satisfaction — detectable before they resign</div>
            <div class="sug-body">
                Deploy <b>5-question pulse surveys</b> covering satisfaction, workload,
                recognition, growth, and belonging. Share anonymised results and
                mandate manager action plans within 30 days.
                Showing employees their feedback causes change is itself a retention tool.
                <br><br>
                <b>Action:</b> Launch the first pulse survey within 2 weeks.
                Share results at the next all-hands.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with q3:
        st.markdown("""
        <div class="sug-card win">
            <div class="sug-hdr">
                <span style="font-size:1.25rem;">🧭</span>
                <span class="sug-badge b-win">Quick Win</span>
                <span class="sug-title">Build an Early-Warning Attrition Model</span>
            </div>
            <div class="sug-stat">📊 Key risk factors are measurable, combinable, and predictive</div>
            <div class="sug-body">
                Train a <b>predictive attrition risk score</b> using this dataset —
                combining WLB rating, promotion recency, overtime, income band, and job level.
                Flag employees in the top 20% risk tier each quarter for proactive
                manager outreach before the exit decision is made.
                <br><br>
                <b>Action:</b> Build a simple risk score in a spreadsheet this week —
                no ML required for a first version.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{BRAND_DARK} 0%,{BRAND} 100%);
                border-radius:14px;padding:18px 28px;text-align:center;
                box-shadow:0 4px 22px rgba(45,59,224,.2);">
        <div style="width:54px;height:54px;background:#fff;border-radius:9px;
                    display:flex;align-items:center;justify-content:center;
                    margin:0 auto 10px;box-shadow:0 5px 15px rgba(0,0,0,.14);">
            {logo(40)}
        </div>
        <div style="font-size:.67rem;color:rgba(255,255,255,.50);letter-spacing:.10em;text-transform:uppercase;">
            Kayfa HR Analytics Platform · Employee Attrition Intelligence Report · Week #1 Task · 2024
        </div>
    </div>
    """, unsafe_allow_html=True)
