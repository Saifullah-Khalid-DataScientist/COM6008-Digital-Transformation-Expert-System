# app.py
# Small Business Digital Transformation Advisor
# COM6008 Knowledge-Based Systems — Expert System Implementation

import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from advisor_engine import DigitalTransformationAdvisor

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Digital Transformation Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif !important; }
code, pre { font-family: 'JetBrains Mono', monospace !important; }

/* ── ANIMATIONS ── */
@keyframes fadeSlideIn {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes heroGlow {
    0%,100% { box-shadow: 0 8px 32px rgba(46,110,164,0.25); }
    50%      { box-shadow: 0 8px 56px rgba(46,110,164,0.5), 0 0 80px rgba(26,107,69,0.12); }
}
@keyframes pulseAccent {
    0%,100% { border-left-color:#2e86c1; }
    50%      { border-left-color:#8b6914; }
}
@keyframes slideInLeft {
    from { opacity:0; transform:translateX(-28px); }
    to   { opacity:1; transform:translateX(0); }
}
@keyframes shimmerBtn {
    0%   { background-position:0% 50%; }
    50%  { background-position:100% 50%; }
    100% { background-position:0% 50%; }
}
@keyframes countUp {
    from { opacity:0; transform:scale(0.75); }
    to   { opacity:1; transform:scale(1); }
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #0f0c29 100%);
    min-height:100vh;
}

/* FIX: extra top padding so hero is never cut off */
.block-container {
    padding: 2.5rem 3rem 3rem 3rem !important;
    max-width: 1200px !important;
}

/* Hero — FIX: margin-top added so it clears the Streamlit toolbar */
.hero-box {
    background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
    border: 1px solid #2e6da4;
    border-radius: 16px;
    padding: 2.8rem 3rem;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    text-align: center;
    animation: heroGlow 4s ease-in-out infinite, fadeSlideIn 0.7s ease both;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #e8f4fd;
    margin: 0 0 0.6rem 0;
    letter-spacing: -0.5px;
    animation: fadeSlideIn 0.8s ease both;
}
.hero-sub {
    font-size: 1.15rem;
    color: #7fb3d3;
    margin: 0;
    font-weight: 400;
    animation: fadeSlideIn 1s ease 0.2s both;
}

/* Section headers — slightly larger */
.section-header {
    font-size: 1.35rem;
    font-weight: 600;
    color: #e8f4fd;
    border-left: 4px solid #2e86c1;
    padding-left: 0.8rem;
    margin: 1.6rem 0 1rem 0;
    animation: pulseAccent 3s ease-in-out infinite, slideInLeft 0.5s ease both;
}

/* Profile section container — real styled box */
.profile-section {
    background: rgba(30,58,95,0.45);
    border: 1px solid rgba(46,134,193,0.3);
    border-radius: 14px;
    padding: 1.6rem 1.6rem 0.6rem 1.6rem;
    margin-bottom: 1.8rem;
    animation: fadeSlideIn 0.6s ease 0.1s both;
}
.profile-section-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #7fb3d3;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
}

/* Metric cards */
.metric-row { display:flex; gap:1rem; margin:1.5rem 0; }
.metric-card {
    flex:1;
    background: rgba(30,58,95,0.6);
    border: 1px solid rgba(46,134,193,0.3);
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    text-align: center;
    animation: fadeSlideIn 0.6s ease both;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform:translateY(-4px); box-shadow:0 10px 28px rgba(46,134,193,0.22); }
.metric-value {
    font-size: 2.3rem;
    font-weight: 700;
    color: #c4a35a;
    font-family: 'JetBrains Mono', monospace !important;
    animation: countUp 0.9s cubic-bezier(0.34,1.56,0.64,1) both;
}
.metric-label {
    font-size: 0.88rem;
    color: #7fb3d3;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

/* Question text — bigger */
.q-text {
    color: #d4e6f5;
    font-size: 1.05rem;
    padding-top: 0.45rem;
    line-height: 1.5;
}

/* Category label */
.cat-label {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #c4a35a;
    margin: 1.4rem 0 0.6rem 0;
}

/* Recommendation cards */
.rec-critical {
    background: rgba(139,35,35,0.12);
    border-left: 4px solid #8b2323;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin: 0.45rem 0;
    color: #f0c4bf;
    font-size: 1rem;
    animation: slideInLeft 0.4s ease both;
    transition: background 0.2s, transform 0.2s;
}
.rec-critical:hover { background:rgba(139,35,35,0.22); transform:translateX(4px); }

.rec-important {
    background: rgba(139,105,20,0.12);
    border-left: 4px solid #8b6914;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin: 0.45rem 0;
    color: #f5dca3;
    font-size: 1rem;
    animation: slideInLeft 0.4s ease 0.05s both;
    transition: background 0.2s, transform 0.2s;
}
.rec-important:hover { background:rgba(139,105,20,0.22); transform:translateX(4px); }

.rec-optional {
    background: rgba(26,107,69,0.12);
    border-left: 4px solid #1a6b45;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin: 0.45rem 0;
    color: #a9dfbf;
    font-size: 1rem;
    animation: slideInLeft 0.4s ease 0.1s both;
    transition: background 0.2s, transform 0.2s;
}
.rec-optional:hover { background:rgba(26,107,69,0.22); transform:translateX(4px); }

/* Rule log */
.rule-item {
    background: rgba(30,58,95,0.25);
    border: 1px solid rgba(46,134,193,0.15);
    border-radius: 8px;
    padding: 0.65rem 1rem;
    margin: 0.38rem 0;
    font-size: 0.95rem;
    color: #aed6f1;
    animation: fadeIn 0.3s ease both;
    transition: background 0.2s;
}
.rule-item:hover { background:rgba(30,58,95,0.55); }
.rule-id {
    font-family: 'JetBrains Mono', monospace;
    color: #c4a35a;
    font-weight: 600;
    margin-right: 0.5rem;
    font-size: 0.92rem;
}

/* Divider */
.divider { border:none; border-top:1px solid rgba(46,134,193,0.2); margin:1.5rem 0; }

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(30,58,95,0.7) !important;
    border: 1px solid rgba(46,134,193,0.4) !important;
    border-radius: 8px !important;
    color: #e8f4fd !important;
    font-size: 1rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(139,105,20,0.7) !important;
}
div[data-testid="stButton"] > button {
    background: linear-gradient(270deg, #8b2323, #8b6914, #1a6b45, #8b6914, #8b2323);
    background-size: 400% 400%;
    color: white; border: none; border-radius: 10px;
    padding: 0.7rem 2.5rem; font-size: 1.05rem; font-weight: 600;
    width: 100%; letter-spacing: 0.5px;
    animation: shimmerBtn 5s ease infinite;
    transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(139,105,20,0.45);
}
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1a6b45 0%, #0d3d26 100%);
    color: white; border: 1px solid #1a6b45; border-radius: 10px;
    padding: 0.65rem 2rem; font-size: 1rem; font-weight: 600; width: 100%;
    transition: all 0.2s;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #27ae60, #1a6b45);
    box-shadow: 0 6px 20px rgba(26,107,69,0.4);
}
label { color: #aed6f1 !important; font-size: 1rem !important; }
.stExpander {
    background: rgba(30,58,95,0.3) !important;
    border: 1px solid rgba(46,134,193,0.2) !important;
    border-radius: 10px !important;
    animation: fadeSlideIn 0.5s ease both;
}
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-box">
  <div class="hero-title">🚀 Small Business Digital Transformation Advisor</div>
  <div class="hero-sub">
    An intelligent rule-based expert system to assess your digital maturity
    and deliver actionable transformation recommendations
  </div>
</div>
""", unsafe_allow_html=True)

# ── SECTION: BUSINESS PROFILE ─────────────────────────────────────────────────
# FIX: Use st.container() with native Streamlit columns — no fake HTML divs

st.markdown('<div class="section-header">Step 1 — Business Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="profile-section"><div class="profile-section-label">📋 Tell us about your organisation</div></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    company_size = st.selectbox("🏢 Company Size",
        ["— Select —","Micro (1–9 staff)","Small (10–49 staff)","Medium (50–249 staff)"],
        key="company_size")
with col2:
    industry = st.selectbox("🏭 Industry Sector",
        ["— Select —","Retail / E-Commerce","Healthcare","Manufacturing",
         "Financial Services","Hospitality / Tourism","Professional Services","Other"],
        key="industry")
with col3:
    budget = st.selectbox("💰 Annual Digital Budget",
        ["— Select —","Under £5,000","£5,000 – £20,000","£20,000 – £100,000","Over £100,000"],
        key="budget")
with col4:
    years = st.selectbox("📅 Years in Operation",
        ["— Select —","Less than 2 years","2–5 years","6–15 years","Over 15 years"],
        key="years")

# Visual border below profile to separate it clearly
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION: DIAGNOSTIC QUESTIONS ────────────────────────────────────────────

st.markdown('<div class="section-header">Step 2 — Digital Capability Assessment</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#7fb3d3; font-size:1.05rem; margin-bottom:1.4rem; line-height:1.6;">'
    'Answer all 19 questions honestly. The system will apply <strong style="color:#c4a35a;">25 expert rules</strong> '
    'to evaluate your digital maturity across six capability domains.</p>',
    unsafe_allow_html=True)

QUESTIONS = [
    ("cloud",               "Infrastructure",        "☁️", "Does your business use cloud computing (e.g. AWS, Azure, Google Cloud, Microsoft 365)?"),
    ("security",            "Infrastructure",        "🔒", "Are active cybersecurity measures in place (firewall, antivirus, MFA, security audits)?"),
    ("backup",              "Infrastructure",        "💾", "Are automated data backups maintained on a regular schedule?"),
    ("mobile_access",       "Infrastructure",        "📱", "Can employees access business systems securely via mobile devices?"),
    ("analytics",           "Data & Intelligence",   "📊", "Does your business use data analytics tools to support decision-making?"),
    ("data_management",     "Data & Intelligence",   "🗄️", "Is business data stored and managed in a centralised, organised system?"),
    ("performance_tracking","Data & Intelligence",   "📈", "Are business KPIs and performance metrics tracked through digital tools?"),
    ("automation",          "Automation & AI",       "⚙️", "Are any repetitive business processes automated (e.g. invoicing, stock alerts, scheduling)?"),
    ("ai_tools",            "Automation & AI",       "🤖", "Does your business use any AI-powered tools (chatbots, predictive analytics, AI assistants)?"),
    ("agile",               "Automation & AI",       "🔄", "Does your team use agile or iterative project management methods (Scrum, Kanban)?"),
    ("crm",                 "Customer & Market",     "👥", "Do you use a CRM system to manage customer relationships and sales pipelines?"),
    ("customer_platform",   "Customer & Market",     "🌐", "Do customers interact with your business through a digital platform (website, app, portal)?"),
    ("digital_marketing",   "Customer & Market",     "📣", "Do you actively use digital marketing channels (SEO, email, social media, paid ads)?"),
    ("strategy",            "Strategy & Governance", "🎯", "Does your business have a documented digital transformation strategy or roadmap?"),
    ("leadership",          "Strategy & Governance", "👔", "Does senior leadership actively champion and invest in digital transformation?"),
    ("governance",          "Strategy & Governance", "📋", "Are formal IT governance policies defined (data privacy, access control, compliance)?"),
    ("training",            "People & Collaboration","🎓", "Do employees receive structured training on digital tools and skills?"),
    ("collaboration",       "People & Collaboration","💬", "Do teams use digital collaboration platforms (Teams, Slack, Notion, Google Workspace)?"),
    ("remote_work",         "People & Collaboration","🏠", "Does your business have the infrastructure to support remote or hybrid working?"),
]

answers = {}
prev_category = None

for key, category, icon, question in QUESTIONS:
    if category != prev_category:
        st.markdown(
            f'<div class="cat-label">{icon}  {category}</div>',
            unsafe_allow_html=True)
        prev_category = category

    col_q, col_a = st.columns([4, 1])
    with col_q:
        st.markdown(f'<div class="q-text">{question}</div>', unsafe_allow_html=True)
    with col_a:
        answers[key] = st.selectbox(
            label=" ", options=["— Select —","Yes","No"],
            key=key, label_visibility="collapsed")

# ── ANALYSE BUTTON ────────────────────────────────────────────────────────────

st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    analyse_clicked = st.button("🔍  Run Expert System Analysis")

# ── VALIDATION & RESULTS ──────────────────────────────────────────────────────

if analyse_clicked:

    profile_labels_vals = [
        ("Company Size", company_size), ("Industry Sector", industry),
        ("Annual Digital Budget", budget), ("Years in Operation", years)
    ]
    missing_profile = [l for l, v in profile_labels_vals if v.startswith("—")]
    unanswered = [key for key, _, _, _ in QUESTIONS if answers.get(key,"— Select —").startswith("—")]

    if missing_profile or unanswered:
        if missing_profile:
            st.error(f"⚠️  Please complete your business profile: **{', '.join(missing_profile)}**")
        if unanswered:
            st.error(f"⚠️  Please answer all {len(unanswered)} remaining question(s) before running the analysis.")
        st.stop()

    processed = {k: 1 if v == "Yes" else 0 for k, v in answers.items()}
    advisor   = DigitalTransformationAdvisor(processed)
    result    = advisor.evaluate()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Assessment Results</div>', unsafe_allow_html=True)

    # ── METRIC CARDS ─────────────────────────────────────────────────────────

    level_color = result["level_color"]
    risk_color  = {"HIGH":"#8b2323","MEDIUM":"#8b6914","LOW":"#1a6b45"}[result["risk_level"]]

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-value" style="color:{level_color};">
            {result['score']}<span style="font-size:1rem;color:#7fb3d3;">/100</span>
        </div>
        <div class="metric-label">Maturity Score</div>
      </div>
      <div class="metric-card">
        <div class="metric-value" style="color:{level_color};font-size:1.25rem;line-height:1.3;">
            {result['level']}
        </div>
        <div class="metric-label">Digital Maturity Level</div>
      </div>
      <div class="metric-card">
        <div class="metric-value" style="color:{risk_color};font-size:1.9rem;">
            {result['risk_level']}
        </div>
        <div class="metric-label">Risk Level</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{len(result['rules_triggered'])}</div>
        <div class="metric-label">Rules Fired</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<p style="color:#aed6f1;font-size:1.02rem;margin-bottom:1.5rem;padding:0.8rem 1.1rem;'
        f'background:rgba(46,134,193,0.07);border-radius:8px;border:1px solid rgba(46,134,193,0.18);line-height:1.6;">'
        f'<strong>Risk Assessment:</strong> {result["risk_description"]}</p>',
        unsafe_allow_html=True)

    # ── CRITICAL GAPS BANNER ──────────────────────────────────────────────────

    if result["critical_gaps"]:
        gaps_str = " &nbsp;|&nbsp; ".join([f"⛔ {g}" for g in result["critical_gaps"]])
        st.markdown(
            f'<div style="background:rgba(139,35,35,0.12);border:1px solid #8b2323;border-radius:10px;'
            f'padding:0.9rem 1.3rem;margin-bottom:1.2rem;color:#f0c4bf;font-size:1rem;">'
            f'<strong>Critical Gaps Identified:</strong> {gaps_str}</div>',
            unsafe_allow_html=True)

    # ── CHART CONSTANTS ───────────────────────────────────────────────────────

    COL_ACHIEVED = "#1a6b45"
    COL_GAP      = "#8b2323"
    COL_AMBER    = "#8b6914"
    COL_NAVY     = "#0d1b2a"
    COL_TEXT     = "#d4e6f5"
    COL_GRID     = "#1e3a5f"

    max_per_cat = {
        "Infrastructure":        23,
        "Data & Intelligence":   16,
        "Automation & AI":       18,
        "Customer & Market":     16,
        "Strategy & Governance": 16,
        "People & Collaboration":14,
    }

    chart_col1, chart_col2 = st.columns(2)

    # ── RADAR CHART ───────────────────────────────────────────────────────────
    with chart_col1:
        st.markdown('<div class="section-header" style="font-size:1.05rem;">Capability Radar</div>', unsafe_allow_html=True)

        categories  = list(max_per_cat.keys())
        short_names = ["Infra.", "Data", "Auto/AI", "Customer", "Strategy", "People"]
        vals = [min(result["category_scores"].get(c, 0) / max_per_cat[c] * 100, 100) for c in categories]

        N           = len(categories)
        angles      = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        vals_plot   = vals  + [vals[0]]
        angles_plot = angles + [angles[0]]

        fig1, ax1 = plt.subplots(figsize=(5.2, 4.8), subplot_kw=dict(polar=True))
        fig1.patch.set_facecolor(COL_NAVY)
        ax1.set_facecolor(COL_NAVY)

        ax1.fill(angles_plot, [100]*len(angles_plot), color=COL_GAP,      alpha=0.07)
        ax1.fill(angles_plot, [60] *len(angles_plot), color=COL_AMBER,    alpha=0.09)
        ax1.fill(angles_plot, [30] *len(angles_plot), color=COL_ACHIEVED, alpha=0.11)

        ax1.plot(angles_plot, vals_plot,  color=COL_ACHIEVED, linewidth=2.5)
        ax1.fill(angles_plot, vals_plot,  color=COL_ACHIEVED, alpha=0.28)
        ax1.scatter(angles, vals, color=COL_AMBER, s=50, zorder=5)

        ax1.set_xticks(angles)
        ax1.set_xticklabels(short_names, color=COL_TEXT, fontsize=9)
        ax1.set_yticklabels([])
        ax1.set_ylim(0, 100)
        ax1.spines["polar"].set_color(COL_GRID)
        ax1.grid(color=COL_GRID, linestyle="--", linewidth=0.6)

        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)
        plt.close()

    # ── GAP ANALYSIS BAR CHART ────────────────────────────────────────────────
    with chart_col2:
        st.markdown('<div class="section-header" style="font-size:1.05rem;">Gap Analysis by Category</div>', unsafe_allow_html=True)

        cat_labels   = list(max_per_cat.keys())
        cat_achieved = [result["category_scores"].get(c, 0) for c in cat_labels]
        cat_max      = [max_per_cat[c] for c in cat_labels]
        cat_gap      = [m - a for m, a in zip(cat_max, cat_achieved)]
        short_labels = ["Infra.", "Data", "Auto/AI", "Customer", "Strategy", "People"]
        x = np.arange(len(cat_labels))

        fig2, ax2 = plt.subplots(figsize=(5.5, 4.8))
        fig2.patch.set_facecolor(COL_NAVY)
        ax2.set_facecolor(COL_NAVY)

        ax2.bar(x, cat_achieved, color=COL_ACHIEVED, label="Achieved", width=0.45, zorder=3, edgecolor=COL_NAVY)
        ax2.bar(x, cat_gap, bottom=cat_achieved, color=COL_GAP, label="Gap",
                width=0.45, zorder=3, alpha=0.6, edgecolor=COL_NAVY)

        for xi, val in zip(x, cat_achieved):
            if val > 0:
                ax2.text(xi, val + 0.2, str(int(val)),
                         ha="center", va="bottom", color=COL_TEXT, fontsize=9, fontweight="bold")

        ax2.set_xticks(x)
        ax2.set_xticklabels(short_labels, color=COL_TEXT, fontsize=9, rotation=18, ha="right")
        ax2.set_ylabel("Score (points)", color=COL_TEXT, fontsize=10, labelpad=8)
        ax2.tick_params(axis="y", colors=COL_TEXT, labelsize=9)
        ax2.tick_params(axis="x", colors=COL_TEXT)
        for sp in ["top","right"]: ax2.spines[sp].set_visible(False)
        for sp in ["bottom","left"]: ax2.spines[sp].set_color(COL_GRID)
        ax2.grid(axis="y", color=COL_GRID, linestyle="--", linewidth=0.5, zorder=0)
        ax2.legend(facecolor=COL_NAVY, edgecolor=COL_GRID, labelcolor=COL_TEXT, fontsize=9, loc="upper right")

        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()

    chart_col3, chart_col4 = st.columns(2)

    # ── PIE CHART ────────────────────────────────────────────────────────────
    with chart_col3:
        st.markdown('<div class="section-header" style="font-size:1.05rem;">Capability Adoption Ratio</div>', unsafe_allow_html=True)

        adopted = sum(processed.values())
        missing = len(processed) - adopted

        fig3, ax3 = plt.subplots(figsize=(4.8, 4.2))
        fig3.patch.set_facecolor(COL_NAVY)
        ax3.set_facecolor(COL_NAVY)

        wedges, texts, autotexts = ax3.pie(
            [adopted, missing],
            labels=["Implemented", "Not Yet Adopted"],
            autopct="%1.1f%%",
            colors=[COL_ACHIEVED, COL_GAP],
            startangle=90,
            wedgeprops=dict(edgecolor=COL_NAVY, linewidth=2.5),
            textprops=dict(color=COL_TEXT, fontsize=10)
        )
        for at in autotexts:
            at.set_color("#e8f4fd"); at.set_fontsize(10); at.set_fontweight("bold")

        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close()

    # ── MATURITY GAUGE ────────────────────────────────────────────────────────
    with chart_col4:
        st.markdown('<div class="section-header" style="font-size:1.05rem;">Maturity Score Position</div>', unsafe_allow_html=True)

        fig4, ax4 = plt.subplots(figsize=(5.2, 4.2))
        fig4.patch.set_facecolor(COL_NAVY)
        ax4.set_facecolor(COL_NAVY)

        tiers = [("Early Stage\n(0–41)", COL_GAP, 41),
                 ("Developing\n(42–71)", COL_AMBER, 30),
                 ("Advanced\n(72–100)", COL_ACHIEVED, 29)]
        left = 0
        for label, color, width in tiers:
            ax4.barh(0, width, left=left, color=color, alpha=0.55,
                     height=0.32, edgecolor=COL_NAVY, linewidth=1.5)
            ax4.text(left + width/2, 0, label, ha="center", va="center",
                     color="#e8f4fd", fontsize=9)
            left += width

        score = result["score"]
        ax4.axvline(score, color="white", linewidth=2.5, linestyle="--", zorder=5)
        ax4.text(score, 0.22, f"  ▼ {score}", color="white",
                 fontsize=11, fontweight="bold", va="bottom")

        ax4.set_xlim(0, 100)
        ax4.set_ylim(-0.3, 0.45)
        ax4.axis("off")

        plt.tight_layout()
        st.pyplot(fig4, use_container_width=True)
        plt.close()

    # ── RECOMMENDATIONS ───────────────────────────────────────────────────────

    st.markdown('<div class="section-header">Expert Recommendations</div>', unsafe_allow_html=True)

    priority_map = {
        "Critical":  ("rec-critical",  "⛔  Critical Priority"),
        "Important": ("rec-important", "⚠️  Important"),
        "Optional":  ("rec-optional",  "💡  Optional Enhancement"),
    }
    prev_p = None
    for rec in result["recommendations"]:
        p = rec["priority"]
        css_class, label = priority_map[p]
        if p != prev_p:
            st.markdown(
                f'<p style="font-size:0.88rem;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:1.5px;color:#7fb3d3;margin:1.1rem 0 0.5rem 0;">{label}</p>',
                unsafe_allow_html=True)
            prev_p = p
        st.markdown(
            f'<div class="{css_class}"><strong>[{rec["category"]}]</strong> {rec["text"]}</div>',
            unsafe_allow_html=True)

    # ── RISK FLAGS ────────────────────────────────────────────────────────────

    if result["risk_flags"]:
        with st.expander("⚠️  Risk Flags Identified"):
            for flag in result["risk_flags"]:
                st.markdown(
                    f'<div style="color:#f0c4bf;padding:0.45rem 0;font-size:1rem;">🔴 {flag}</div>',
                    unsafe_allow_html=True)

    # ── RULE TRACE ────────────────────────────────────────────────────────────

    with st.expander(f"🧠  View Expert Rule Trace  ({len(result['rules_triggered'])} rules fired)"):
        cat_color_map = {
            "Infrastructure":        "#2e86c1",
            "Data & Intelligence":   "#8b6914",
            "Automation & AI":       "#9b59b6",
            "Customer & Market":     "#1a6b45",
            "Strategy & Governance": "#8b2323",
            "People & Collaboration":"#117a65",
        }
        for rule in result["rules_triggered"]:
            cat_col = cat_color_map.get(rule["category"], "#aed6f1")
            st.markdown(
                f'<div class="rule-item">'
                f'<span class="rule-id">Rule {rule["id"]:02d}</span>'
                f'<span style="color:{cat_col};font-size:0.85rem;margin-right:0.6rem;font-weight:600;">'
                f'[{rule["category"]}]</span>'
                f'<span>{rule["description"]}</span>'
                f'<span style="float:right;color:#c4a35a;font-family:monospace;font-size:0.88rem;font-weight:600;">'
                f'+{rule["points"]} pts</span>'
                f'</div>',
                unsafe_allow_html=True)

    # ── PDF EXPORT ────────────────────────────────────────────────────────────

    def generate_pdf(result, company_size, industry, budget, years):
        buffer = BytesIO()
        # FIX: narrower right margin so rule description column has more room
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=1.8*cm, leftMargin=1.8*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()

        title_s = ParagraphStyle("title", parent=styles["Title"],
                                 fontSize=20, spaceAfter=6,
                                 textColor=colors.HexColor("#1a4a7a"), alignment=TA_CENTER)
        sub_s   = ParagraphStyle("sub", parent=styles["Normal"],
                                 fontSize=11, textColor=colors.grey,
                                 alignment=TA_CENTER, spaceAfter=16)
        h2_s    = ParagraphStyle("h2", parent=styles["Heading2"],
                                 fontSize=14, textColor=colors.HexColor("#1a4a7a"),
                                 spaceBefore=14, spaceAfter=7)
        body_s  = ParagraphStyle("body", parent=styles["Normal"],
                                 fontSize=11, leading=15, spaceAfter=6)
        rec_s   = ParagraphStyle("rec", parent=styles["Normal"],
                                 fontSize=10, leading=14, spaceAfter=4, leftIndent=10)

        story = []
        story.append(Paragraph("Small Business Digital Transformation Advisor", title_s))
        story.append(Paragraph("Expert System Assessment Report — COM6008 Knowledge-Based Systems", sub_s))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1a6b45")))
        story.append(Spacer(1, 0.4*cm))

        # Profile
        story.append(Paragraph("Business Profile", h2_s))
        usable = 16.4*cm  # A4 width minus margins
        pt = Table([
            ["Company Size",        company_size],
            ["Industry Sector",     industry],
            ["Annual Digital Budget",budget],
            ["Years in Operation",  years],
        ], colWidths=[5*cm, usable - 5*cm])
        pt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eaf4fb")),
            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
            ("FONTSIZE",(0,0),(-1,-1),11),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ]))
        story.append(pt)
        story.append(Spacer(1, 0.4*cm))

        # Results
        story.append(Paragraph("Assessment Results", h2_s))
        rt = Table([
            ["Maturity Score",      f"{result['score']} / 100"],
            ["Digital Maturity Level", result["level"]],
            ["Risk Level",          result["risk_level"]],
            ["Rules Fired",         str(len(result["rules_triggered"]))],
        ], colWidths=[5*cm, usable - 5*cm])
        rt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eaf4fb")),
            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
            ("FONTSIZE",(0,0),(-1,-1),11),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ]))
        story.append(rt)
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(result["risk_description"], body_s))

        # Recommendations
        story.append(Paragraph("Expert Recommendations", h2_s))
        prefix_map = {"Critical":"[CRITICAL]","Important":"[IMPORTANT]","Optional":"[OPTIONAL]"}
        for rec in result["recommendations"]:
            story.append(Paragraph(
                f'<b>{prefix_map[rec["priority"]]} {rec["category"]}:</b> {rec["text"]}', rec_s))

        # Rule trace — FIX overlapping: tighter col widths, word wrap, smaller font
        story.append(Paragraph("Expert Rule Trace", h2_s))
        rule_data = [["Rule", "Category", "Description", "Pts"]]
        for r in result["rules_triggered"]:
            rule_data.append([
                Paragraph(f"Rule {r['id']:02d}",
                          ParagraphStyle("rc", fontSize=9, leading=11)),
                Paragraph(r["category"],
                          ParagraphStyle("rc", fontSize=9, leading=11)),
                Paragraph(r["description"],
                          ParagraphStyle("rd", fontSize=9, leading=12, wordWrap="LTR")),
                Paragraph(f"+{r['points']}",
                          ParagraphStyle("rp", fontSize=9, leading=11)),
            ])

        # Column widths: Rule | Category | Description | Pts
        col_w = [1.4*cm, 3.8*cm, usable - 1.4*cm - 3.8*cm - 1.1*cm, 1.1*cm]
        rule_tbl = Table(rule_data, colWidths=col_w, repeatRows=1)
        rule_tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1a6b45")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),10),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(rule_tbl)

        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
        story.append(Paragraph(
            "Generated by the Small Business Digital Transformation Advisor | "
            "Rules derived from McKinsey Digital Maturity Framework (2023) & Gartner IT Maturity Model (2024) | "
            "COM6008 Knowledge-Based Systems — Buckinghamshire New University",
            ParagraphStyle("footer", parent=styles["Normal"], fontSize=8,
                           textColor=colors.grey, alignment=TA_CENTER, spaceBefore=8)))
        doc.build(story)
        return buffer.getvalue()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📥 Download Full Report</div>', unsafe_allow_html=True)
    pdf_bytes = generate_pdf(result, company_size, industry, budget, years)
    st.download_button(
        label="📄  Download PDF Assessment Report",
        data=pdf_bytes,
        file_name="digital_transformation_report.pdf",
        mime="application/pdf"
    )

    # ── FOOTER ────────────────────────────────────────────────────────────────

    st.markdown("""
    <div style="text-align:center;color:#4a6fa5;font-size:0.88rem;margin-top:3rem;
                padding-top:1.5rem;border-top:1px solid rgba(46,134,193,0.15);">
        COM6008 Knowledge-Based Systems in AI &nbsp;|&nbsp;
        McKinsey Digital Maturity Framework (2023) &amp; Gartner IT Maturity Model (2024)
        &nbsp;|&nbsp; Buckinghamshire New University
    </div>
    """, unsafe_allow_html=True)