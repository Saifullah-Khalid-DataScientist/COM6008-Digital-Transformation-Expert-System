# app.py — Small Business Digital Transformation Advisor
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

st.set_page_config(
    page_title="Digital Transformation Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

DARK = {
    "app_bg":          "linear-gradient(135deg,#0f0c29 0%,#1a1a3e 50%,#0f0c29 100%)",
    "hero_bg":         "linear-gradient(135deg,#1e3a5f 0%,#0d2137 100%)",
    "hero_border":     "#2e6da4","hero_title":"#e8f4fd","hero_sub":"#7fb3d3",
    "section_hdr":     "#e8f4fd","profile_bg":"rgba(30,58,95,0.45)",
    "profile_border":  "rgba(46,134,193,0.3)","profile_label":"#7fb3d3",
    "metric_bg":       "rgba(30,58,95,0.6)","metric_border":"rgba(46,134,193,0.3)",
    "metric_label":    "#7fb3d3","metric_value":"#c4a35a",
    "q_text":          "#d4e6f5","cat_label":"#c4a35a","divider":"rgba(46,134,193,0.2)",
    "risk_bg":         "rgba(46,134,193,0.07)","risk_border":"rgba(46,134,193,0.18)","risk_txt":"#aed6f1",
    "gap_bg":          "rgba(139,35,35,0.12)","gap_border":"#8b2323","gap_txt":"#f0c4bf",
    "crit_bg":         "rgba(139,35,35,0.12)","crit_brd":"#8b2323","crit_txt":"#f0c4bf",
    "imp_bg":          "rgba(139,105,20,0.12)","imp_brd":"#8b6914","imp_txt":"#f5dca3",
    "opt_bg":          "rgba(26,107,69,0.12)","opt_brd":"#1a6b45","opt_txt":"#a9dfbf",
    "rule_bg":         "rgba(30,58,95,0.25)","rule_border":"rgba(46,134,193,0.15)",
    "rule_txt":        "#aed6f1","rule_id":"#c4a35a",
    "box_bg":          "rgba(30,58,95,0.3)","box_border":"rgba(46,134,193,0.2)","box_txt":"#aed6f1",
    "flag_txt":        "#f0c4bf","footer_txt":"#4a6fa5","footer_border":"rgba(46,134,193,0.15)",
    "sel_bg":          "rgba(30,58,95,0.7)","sel_border":"rgba(46,134,193,0.4)","sel_txt":"#e8f4fd",
    "lbl":             "#aed6f1","prio":"#7fb3d3",
    "chart_bg":        "#0d1b2a","chart_txt":"#d4e6f5","chart_grid":"#1e3a5f",
    "marker":          "white","sub_txt":"#7fb3d3","amber_txt":"#c4a35a",
}

LIGHT = {
    "app_bg":          "#f0f4f8",
    "hero_bg":         "linear-gradient(135deg,#1e3a5f 0%,#154360 100%)",
    "hero_border":     "#1a6b9a","hero_title":"#ffffff","hero_sub":"#aed6f1",
    "section_hdr":     "#0d2137","profile_bg":"#ffffff",
    "profile_border":  "#b0cfe8","profile_label":"#1a4a7a",
    "metric_bg":       "#ffffff","metric_border":"#b0cfe8",
    "metric_label":    "#1a4a7a","metric_value":"#8b6914",
    "q_text":          "#1a2a3a","cat_label":"#8b5000","divider":"#b0cfe8",
    "risk_bg":         "#eaf4fb","risk_border":"#7fb3d3","risk_txt":"#1a3a5a",
    "gap_bg":          "#fdecea","gap_border":"#c0392b","gap_txt":"#7b1a1a",
    "crit_bg":         "#fdecea","crit_brd":"#c0392b","crit_txt":"#7b1a1a",
    "imp_bg":          "#fef9e7","imp_brd":"#d4a017","imp_txt":"#5a3a00",
    "opt_bg":          "#eafaf1","opt_brd":"#1a6b45","opt_txt":"#0b4a2a",
    "rule_bg":         "#f0f7ff","rule_border":"#b0cfe8",
    "rule_txt":        "#1a2a3a","rule_id":"#8b5000",
    "box_bg":          "#eaf4fb","box_border":"#7fb3d3","box_txt":"#1a3a5a",
    "flag_txt":        "#7b1a1a","footer_txt":"#1a4a7a","footer_border":"#b0cfe8",
    "sel_bg":          "#ffffff","sel_border":"#7fb3d3","sel_txt":"#1a2a3a",
    "lbl":             "#1a2a3a","prio":"#1a4a7a",
    "chart_bg":        "#ffffff","chart_txt":"#1a2a3a","chart_grid":"#c8dff0",
    "marker":          "#1a2a3a","sub_txt":"#1a4a7a","amber_txt":"#b35a00",
}

T = DARK if st.session_state.theme == "dark" else LIGHT

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
* {{ font-family:'Inter',sans-serif !important; }}
code,pre {{ font-family:'JetBrains Mono',monospace !important; }}
@keyframes fadeSlideIn {{ from{{opacity:0;transform:translateY(22px)}} to{{opacity:1;transform:translateY(0)}} }}
@keyframes heroGlow {{ 0%,100%{{box-shadow:0 8px 32px rgba(46,110,164,.25)}} 50%{{box-shadow:0 8px 56px rgba(46,110,164,.5)}} }}
@keyframes pulseAccent {{ 0%,100%{{border-left-color:#2e86c1}} 50%{{border-left-color:#8b6914}} }}
@keyframes slideInLeft {{ from{{opacity:0;transform:translateX(-28px)}} to{{opacity:1;transform:translateX(0)}} }}
@keyframes shimmerBtn {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}
@keyframes countUp {{ from{{opacity:0;transform:scale(.75)}} to{{opacity:1;transform:scale(1)}} }}
@keyframes fadeIn {{ from{{opacity:0}} to{{opacity:1}} }}

.stApp {{ background:{T["app_bg"]} !important; min-height:100vh; }}
.block-container {{ padding:2.5rem 3rem 3rem !important; max-width:1200px !important; }}

.hero-box {{ background:{T["hero_bg"]}; border:1px solid {T["hero_border"]}; border-radius:16px;
    padding:2.8rem 3rem; margin-top:0.5rem; margin-bottom:2rem; text-align:center;
    animation:heroGlow 4s ease-in-out infinite,fadeSlideIn .7s ease both; }}
.hero-title {{ font-size:2.5rem; font-weight:700; color:{T["hero_title"]}; margin:0 0 .6rem; letter-spacing:-.5px; }}
.hero-sub   {{ font-size:1.15rem; color:{T["hero_sub"]}; margin:0; font-weight:400; }}

.section-header {{ font-size:1.35rem; font-weight:600; color:{T["section_hdr"]};
    border-left:4px solid #2e86c1; padding-left:.8rem; margin:1.6rem 0 1rem;
    animation:pulseAccent 3s ease-in-out infinite,slideInLeft .5s ease both; }}

.profile-section {{ background:{T["profile_bg"]}; border:1px solid {T["profile_border"]};
    border-radius:14px; padding:1.6rem 1.6rem .6rem; margin-bottom:1.8rem; }}
.profile-section-label {{ font-size:.82rem; font-weight:600; color:{T["profile_label"]};
    text-transform:uppercase; letter-spacing:1.5px; margin-bottom:1rem; }}

.metric-row {{ display:flex; gap:1rem; margin:1.5rem 0; }}
.metric-card {{ flex:1; background:{T["metric_bg"]}; border:1px solid {T["metric_border"]};
    border-radius:12px; padding:1.3rem 1.5rem; text-align:center;
    animation:fadeSlideIn .6s ease both; transition:transform .2s,box-shadow .2s; }}
.metric-card:hover {{ transform:translateY(-4px); box-shadow:0 10px 28px rgba(46,134,193,.22); }}
.metric-value {{ font-size:2.3rem; font-weight:700; color:{T["metric_value"]};
    font-family:'JetBrains Mono',monospace !important; animation:countUp .9s cubic-bezier(.34,1.56,.64,1) both; }}
.metric-label {{ font-size:.88rem; color:{T["metric_label"]}; text-transform:uppercase; letter-spacing:1px; margin-top:.3rem; }}

.q-text   {{ color:{T["q_text"]}; font-size:1.05rem; padding-top:.45rem; line-height:1.5; }}
.cat-label {{ font-size:.82rem; font-weight:600; text-transform:uppercase; letter-spacing:2px;
    color:{T["cat_label"]}; margin:1.4rem 0 .6rem; }}
.divider {{ border:none; border-top:1px solid {T["divider"]}; margin:1.5rem 0; }}

.rec-critical {{ background:{T["crit_bg"]}; border-left:4px solid {T["crit_brd"]}; border-radius:0 8px 8px 0;
    padding:.9rem 1.1rem; margin:.45rem 0; color:{T["crit_txt"]}; font-size:1rem;
    animation:slideInLeft .4s ease both; transition:transform .2s; }}
.rec-critical:hover {{ transform:translateX(4px); }}
.rec-important {{ background:{T["imp_bg"]}; border-left:4px solid {T["imp_brd"]}; border-radius:0 8px 8px 0;
    padding:.9rem 1.1rem; margin:.45rem 0; color:{T["imp_txt"]}; font-size:1rem;
    animation:slideInLeft .4s ease .05s both; transition:transform .2s; }}
.rec-important:hover {{ transform:translateX(4px); }}
.rec-optional {{ background:{T["opt_bg"]}; border-left:4px solid {T["opt_brd"]}; border-radius:0 8px 8px 0;
    padding:.9rem 1.1rem; margin:.45rem 0; color:{T["opt_txt"]}; font-size:1rem;
    animation:slideInLeft .4s ease .1s both; transition:transform .2s; }}
.rec-optional:hover {{ transform:translateX(4px); }}

.rule-item {{ background:{T["rule_bg"]}; border:1px solid {T["rule_border"]}; border-radius:8px;
    padding:.65rem 1rem; margin:.38rem 0; font-size:.95rem; color:{T["rule_txt"]};
    animation:fadeIn .3s ease both; transition:background .2s; }}
.rule-id {{ font-family:'JetBrains Mono',monospace; color:{T["rule_id"]}; font-weight:600;
    margin-right:.5rem; font-size:.92rem; }}

div[data-testid="stSelectbox"]>div>div {{
    background:{T["sel_bg"]} !important; border:1px solid {T["sel_border"]} !important;
    border-radius:8px !important; color:{T["sel_txt"]} !important; font-size:1rem !important; }}
div[data-testid="stButton"]>button {{
    background:linear-gradient(270deg,#8b2323,#8b6914,#1a6b45,#8b6914,#8b2323);
    background-size:400% 400%; color:white; border:none; border-radius:10px;
    padding:.7rem 2.5rem; font-size:1.05rem; font-weight:600; width:100%;
    animation:shimmerBtn 5s ease infinite; transition:transform .2s,box-shadow .2s; }}
div[data-testid="stButton"]>button:hover {{
    transform:translateY(-2px); box-shadow:0 8px 28px rgba(139,105,20,.45); }}

div[data-testid="stDownloadButton"]>button {{
    background:linear-gradient(135deg,#1a6b45 0%,#0d3d26 100%);
    color:white; border:1px solid #1a6b45; border-radius:10px;
    padding:.65rem 2rem; font-size:1rem; font-weight:600; width:100%; transition:all .2s; }}
div[data-testid="stDownloadButton"]>button:hover {{
    background:linear-gradient(135deg,#27ae60,#1a6b45); box-shadow:0 6px 20px rgba(26,107,69,.4); }}
    
label {{ color:{T["lbl"]} !important; font-size:1rem !important; }}
</style>
""", unsafe_allow_html=True)

# ── THEME TOGGLE ──────────────────────────────────────────────────────────────
st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
tcol1, tcol2 = st.columns([11, 1])
with tcol2:
    btn_label = "☀️ Light" if st.session_state.theme == "dark" else "🌙 Dark"
    st.markdown(f"""
    <style>
    div[data-testid="stButton"] > button {{
        background: rgba(30,58,95,0.5) !important;
        color: #e8f4fd !important;
        border: 1px solid rgba(46,134,193,0.5) !important;
        border-radius: 20px !important;
        padding: 0.3rem 0.9rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        width: auto !important;
        min-width: unset !important;
        animation: none !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        background: rgba(46,134,193,0.3) !important;
        transform: none !important;
        box-shadow: 0 2px 8px rgba(46,134,193,0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    if st.button(btn_label, key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-title">🚀 Small Business Digital Transformation Advisor</div>
  <div class="hero-sub">An intelligent rule-based expert system to assess your digital maturity
    and deliver actionable transformation recommendations</div>
</div>""", unsafe_allow_html=True)

# ── BUSINESS PROFILE ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Step 1 — Business Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="profile-section"><div class="profile-section-label">📋 Tell us about your organisation</div></div>', unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)
with col1:
    company_size = st.selectbox("🏢 Company Size",
        ["— Select —","Micro (1–9 staff)","Small (10–49 staff)","Medium (50–249 staff)"],key="company_size")
with col2:
    industry = st.selectbox("🏭 Industry Sector",
        ["— Select —","Retail / E-Commerce","Healthcare","Manufacturing",
         "Financial Services","Hospitality / Tourism","Professional Services","Other"],key="industry")
with col3:
    budget = st.selectbox("💰 Annual Digital Budget",
        ["— Select —","Under £5,000","£5,000 – £20,000","£20,000 – £100,000","Over £100,000"],key="budget")
with col4:
    years = st.selectbox("📅 Years in Operation",
        ["— Select —","Less than 2 years","2–5 years","6–15 years","Over 15 years"],key="years")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── DIAGNOSTIC QUESTIONS ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">Step 2 — Digital Capability Assessment</div>', unsafe_allow_html=True)
st.markdown(
    f'<p style="color:{T["sub_txt"]};font-size:1.05rem;margin-bottom:1.4rem;line-height:1.6;">'
    f'Answer all 19 questions honestly. The system will apply '
    f'<strong style="color:{T["amber_txt"]};">25 expert rules</strong> '
    f'to evaluate your digital maturity across six capability domains.</p>',
    unsafe_allow_html=True)

QUESTIONS = [
    ("cloud","Infrastructure","☁️","Does your business use cloud computing (e.g. AWS, Azure, Google Cloud, Microsoft 365)?"),
    ("security","Infrastructure","🔒","Are active cybersecurity measures in place (firewall, antivirus, MFA, security audits)?"),
    ("backup","Infrastructure","💾","Are automated data backups maintained on a regular schedule?"),
    ("mobile_access","Infrastructure","📱","Can employees access business systems securely via mobile devices?"),
    ("analytics","Data & Intelligence","📊","Does your business use data analytics tools to support decision-making?"),
    ("data_management","Data & Intelligence","🗄️","Is business data stored and managed in a centralised, organised system?"),
    ("performance_tracking","Data & Intelligence","📈","Are business KPIs and performance metrics tracked through digital tools?"),
    ("automation","Automation & AI","⚙️","Are any repetitive business processes automated (e.g. invoicing, stock alerts, scheduling)?"),
    ("ai_tools","Automation & AI","🤖","Does your business use any AI-powered tools (chatbots, predictive analytics, AI assistants)?"),
    ("agile","Automation & AI","🔄","Does your team use agile or iterative project management methods (Scrum, Kanban)?"),
    ("crm","Customer & Market","👥","Do you use a CRM system to manage customer relationships and sales pipelines?"),
    ("customer_platform","Customer & Market","🌐","Do customers interact with your business through a digital platform (website, app, portal)?"),
    ("digital_marketing","Customer & Market","📣","Do you actively use digital marketing channels (SEO, email, social media, paid ads)?"),
    ("strategy","Strategy & Governance","🎯","Does your business have a documented digital transformation strategy or roadmap?"),
    ("leadership","Strategy & Governance","👔","Does senior leadership actively champion and invest in digital transformation?"),
    ("governance","Strategy & Governance","📋","Are formal IT governance policies defined (data privacy, access control, compliance)?"),
    ("training","People & Collaboration","🎓","Do employees receive structured training on digital tools and skills?"),
    ("collaboration","People & Collaboration","💬","Do teams use digital collaboration platforms (Teams, Slack, Notion, Google Workspace)?"),
    ("remote_work","People & Collaboration","🏠","Does your business have the infrastructure to support remote or hybrid working?"),
]

answers = {}
prev_category = None
for key,category,icon,question in QUESTIONS:
    if category != prev_category:
        st.markdown(f'<div class="cat-label">{icon}  {category}</div>',unsafe_allow_html=True)
        prev_category = category
    cq,ca = st.columns([4,1])
    with cq:
        st.markdown(f'<div class="q-text">{question}</div>',unsafe_allow_html=True)
    with ca:
        answers[key] = st.selectbox(label=" ",options=["— Select —","Yes","No"],
                                    key=key,label_visibility="collapsed")

st.markdown("<div style='height:1.8rem'></div>",unsafe_allow_html=True)
_,col_btn,_ = st.columns([1,2,1])
with col_btn:
    analyse_clicked = st.button("🔍  Run Expert System Analysis")

# ── RESULTS ───────────────────────────────────────────────────────────────────
if analyse_clicked:
    profile_vals = [("Company Size",company_size),("Industry Sector",industry),
                    ("Annual Digital Budget",budget),("Years in Operation",years)]
    missing_profile = [l for l,v in profile_vals if v.startswith("—")]
    unanswered = [k for k,_,_,_ in QUESTIONS if answers.get(k,"— Select —").startswith("—")]

    if missing_profile or unanswered:
        if missing_profile:
            st.error(f"⚠️  Please complete: **{', '.join(missing_profile)}**")
        if unanswered:
            st.error(f"⚠️  Please answer all {len(unanswered)} remaining question(s).")
        st.stop()

    processed = {k:1 if v=="Yes" else 0 for k,v in answers.items()}
    advisor   = DigitalTransformationAdvisor(processed)
    result    = advisor.evaluate()

    st.markdown('<hr class="divider">',unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Assessment Results</div>',unsafe_allow_html=True)

    lc = result["level_color"]
    rc = {"HIGH":"#c0392b","MEDIUM":"#d4a017","LOW":"#1a6b45"}[result["risk_level"]]

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-value" style="color:{lc};">{result['score']}<span style="font-size:1rem;color:{T['metric_label']};">/100</span></div>
        <div class="metric-label">Maturity Score</div>
      </div>
      <div class="metric-card">
        <div class="metric-value" style="color:{lc};font-size:1.25rem;line-height:1.3;">{result['level']}</div>
        <div class="metric-label">Digital Maturity Level</div>
      </div>
      <div class="metric-card">
        <div class="metric-value" style="color:{rc};font-size:1.9rem;">{result['risk_level']}</div>
        <div class="metric-label">Risk Level</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{len(result['rules_triggered'])}</div>
        <div class="metric-label">Rules Fired</div>
      </div>
    </div>""",unsafe_allow_html=True)

    st.markdown(
        f'<p style="color:{T["risk_txt"]};font-size:1.02rem;margin-bottom:1.5rem;padding:.8rem 1.1rem;'
        f'background:{T["risk_bg"]};border-radius:8px;border:1px solid {T["risk_border"]};line-height:1.6;">'
        f'<strong>Risk Assessment:</strong> {result["risk_description"]}</p>',
        unsafe_allow_html=True)

    if result["critical_gaps"]:
        gaps_str = " &nbsp;|&nbsp; ".join([f"⛔ {g}" for g in result["critical_gaps"]])
        st.markdown(
            f'<div style="background:{T["gap_bg"]};border:1px solid {T["gap_border"]};border-radius:10px;'
            f'padding:.9rem 1.3rem;margin-bottom:1.2rem;color:{T["gap_txt"]};font-size:1rem;">'
            f'<strong>Critical Gaps Identified:</strong> {gaps_str}</div>',
            unsafe_allow_html=True)

    # chart palette
    CA   = "#1a6b45"  # achieved green
    CG   = "#c0392b"  # gap red
    CAMB = "#d4a017"  # amber
    CBG  = T["chart_bg"]
    CTX  = T["chart_txt"]
    CGR  = T["chart_grid"]
    MRK  = T["marker"]

    max_per_cat = {
        "Infrastructure":23,"Data & Intelligence":16,"Automation & AI":18,
        "Customer & Market":16,"Strategy & Governance":16,"People & Collaboration":14,
    }
    short = ["Infra.","Data","Auto/AI","Customer","Strategy","People"]

    cc1,cc2 = st.columns(2)

    # RADAR
    with cc1:
        st.markdown(f'<div class="section-header" style="font-size:1.05rem;color:{T["section_hdr"]};">Capability Radar</div>',unsafe_allow_html=True)
        cats = list(max_per_cat.keys())
        vals = [min(result["category_scores"].get(c,0)/max_per_cat[c]*100,100) for c in cats]
        N = len(cats)
        angs = np.linspace(0,2*np.pi,N,endpoint=False).tolist()
        vp = vals+[vals[0]]; ap = angs+[angs[0]]
        fig1,ax1 = plt.subplots(figsize=(5.2,4.8),subplot_kw=dict(polar=True))
        fig1.patch.set_facecolor(CBG); ax1.set_facecolor(CBG)
        ax1.fill(ap,[100]*len(ap),color=CG,alpha=0.07)
        ax1.fill(ap,[60]*len(ap),color=CAMB,alpha=0.09)
        ax1.fill(ap,[30]*len(ap),color=CA,alpha=0.11)
        ax1.plot(ap,vp,color=CA,linewidth=2.5)
        ax1.fill(ap,vp,color=CA,alpha=0.28)
        ax1.scatter(angs,vals,color=CAMB,s=50,zorder=5)
        ax1.set_xticks(angs); ax1.set_xticklabels(short,color=CTX,fontsize=9)
        ax1.set_yticklabels([]); ax1.set_ylim(0,100)
        ax1.spines["polar"].set_color(CGR); ax1.grid(color=CGR,linestyle="--",linewidth=0.6)
        plt.tight_layout(); st.pyplot(fig1,use_container_width=True); plt.close()

    # BAR
    with cc2:
        st.markdown(f'<div class="section-header" style="font-size:1.05rem;color:{T["section_hdr"]};">Gap Analysis by Category</div>',unsafe_allow_html=True)
        ach = [result["category_scores"].get(c,0) for c in cats]
        mx  = [max_per_cat[c] for c in cats]
        gap = [m-a for m,a in zip(mx,ach)]
        x   = np.arange(len(cats))
        fig2,ax2 = plt.subplots(figsize=(5.5,4.8))
        fig2.patch.set_facecolor(CBG); ax2.set_facecolor(CBG)
        ax2.bar(x,ach,color=CA,label="Achieved",width=0.45,zorder=3,edgecolor=CBG)
        ax2.bar(x,gap,bottom=ach,color=CG,label="Gap",width=0.45,zorder=3,alpha=0.75,edgecolor=CBG)
        for xi,val in zip(x,ach):
            if val>0: ax2.text(xi,val+.2,str(int(val)),ha="center",va="bottom",color=CTX,fontsize=9,fontweight="bold")
        ax2.set_xticks(x); ax2.set_xticklabels(short,color=CTX,fontsize=9,rotation=18,ha="right")
        ax2.set_ylabel("Score (points)",color=CTX,fontsize=10,labelpad=8)
        ax2.tick_params(axis="y",colors=CTX,labelsize=9); ax2.tick_params(axis="x",colors=CTX)
        for sp in ["top","right"]: ax2.spines[sp].set_visible(False)
        for sp in ["bottom","left"]: ax2.spines[sp].set_color(CGR)
        ax2.grid(axis="y",color=CGR,linestyle="--",linewidth=0.5,zorder=0)
        ax2.legend(facecolor=CBG,edgecolor=CGR,labelcolor=CTX,fontsize=9,loc="upper right")
        plt.tight_layout(); st.pyplot(fig2,use_container_width=True); plt.close()

    cc3,cc4 = st.columns(2)

    # PIE
    with cc3:
        st.markdown(f'<div class="section-header" style="font-size:1.05rem;color:{T["section_hdr"]};">Capability Adoption Ratio</div>',unsafe_allow_html=True)
        adopted = sum(processed.values()); missing_n = len(processed)-adopted
        fig3,ax3 = plt.subplots(figsize=(4.8,4.2))
        fig3.patch.set_facecolor(CBG); ax3.set_facecolor(CBG)
        wedges,texts,autotexts = ax3.pie(
            [adopted,missing_n],labels=["Implemented","Not Yet Adopted"],autopct="%1.1f%%",
            colors=[CA,CG],startangle=90,
            wedgeprops=dict(edgecolor=CBG,linewidth=2.5),
            textprops=dict(color=CTX,fontsize=10))
        for at in autotexts: at.set_color(CTX); at.set_fontsize(10); at.set_fontweight("bold")
        plt.tight_layout(); st.pyplot(fig3,use_container_width=True); plt.close()

    # GAUGE
    with cc4:
        st.markdown(f'<div class="section-header" style="font-size:1.05rem;color:{T["section_hdr"]};">Maturity Score Position</div>',unsafe_allow_html=True)
        fig4,ax4 = plt.subplots(figsize=(5.2,4.2))
        fig4.patch.set_facecolor(CBG); ax4.set_facecolor(CBG)
        tiers = [("Early Stage\n(0–41)",CG,41),("Developing\n(42–71)",CAMB,30),("Advanced\n(72–100)",CA,29)]
        left=0
        for lbl,col,wid in tiers:
            ax4.barh(0,wid,left=left,color=col,alpha=0.65,height=0.32,edgecolor=CBG,linewidth=1.5)
            ax4.text(left+wid/2,0,lbl,ha="center",va="center",color=CTX,fontsize=9)
            left+=wid
        sc = result["score"]
        ax4.axvline(sc,color=MRK,linewidth=2.5,linestyle="--",zorder=5)
        ax4.text(sc,0.22,f"  ▼ {sc}",color=MRK,fontsize=11,fontweight="bold",va="bottom")
        ax4.set_xlim(0,100); ax4.set_ylim(-0.3,0.45); ax4.axis("off")
        plt.tight_layout(); st.pyplot(fig4,use_container_width=True); plt.close()

    # RECOMMENDATIONS
    st.markdown('<div class="section-header">Expert Recommendations</div>',unsafe_allow_html=True)
    pmap = {"Critical":("rec-critical","⛔  Critical Priority"),
            "Important":("rec-important","⚠️  Important"),
            "Optional":("rec-optional","💡  Optional Enhancement")}
    prev_p=None
    for rec in result["recommendations"]:
        p=rec["priority"]; css,lbl=pmap[p]
        if p!=prev_p:
            st.markdown(f'<p style="font-size:.88rem;font-weight:600;text-transform:uppercase;'
                        f'letter-spacing:1.5px;color:{T["prio"]};margin:1.1rem 0 .5rem;">{lbl}</p>',
                        unsafe_allow_html=True)
            prev_p=p
        st.markdown(f'<div class="{css}"><strong>[{rec["category"]}]</strong> {rec["text"]}</div>',unsafe_allow_html=True)

    # RISK FLAGS
    if result["risk_flags"]:
        st.markdown(
            f'<div style="background:{T["box_bg"]};border:1px solid {T["box_border"]};'
            f'border-radius:10px;padding:.75rem 1rem;margin:.8rem 0 .3rem;">'
            f'<span style="color:{T["box_txt"]};font-size:1rem;font-weight:600;">&#9660; Risk Flags Identified</span></div>',
            unsafe_allow_html=True)
        for flag in result["risk_flags"]:
            st.markdown(f'<div style="color:{T["flag_txt"]};padding:.45rem 1rem;font-size:1rem;">🔴 {flag}</div>',unsafe_allow_html=True)

    # RULE TRACE
    nr = len(result["rules_triggered"])
    st.markdown(
        f'<div style="background:{T["box_bg"]};border:1px solid {T["box_border"]};'
        f'border-radius:10px;padding:.75rem 1rem;margin:.8rem 0 .3rem;">'
        f'<span style="color:{T["box_txt"]};font-size:1rem;font-weight:600;">&#9660; Expert Rule Trace ({nr} rules fired)</span></div>',
        unsafe_allow_html=True)
    cat_col_map = {
        "Infrastructure":"#2e86c1","Data & Intelligence":"#8b6914",
        "Automation & AI":"#9b59b6","Customer & Market":"#1a6b45",
        "Strategy & Governance":"#c0392b","People & Collaboration":"#117a65",
    }
    for rule in result["rules_triggered"]:
        cc = cat_col_map.get(rule["category"],"#aed6f1")
        st.markdown(
            f'<div class="rule-item">'
            f'<span class="rule-id">Rule {rule["id"]:02d}</span>'
            f'<span style="color:{cc};font-size:.85rem;margin-right:.6rem;font-weight:600;">[{rule["category"]}]</span>'
            f'<span style="color:{T["rule_txt"]};">{rule["description"]}</span>'
            f'<span style="float:right;color:{T["rule_id"]};font-family:monospace;font-size:.88rem;font-weight:600;">+{rule["points"]} pts</span>'
            f'</div>',unsafe_allow_html=True)

    # PDF EXPORT
    def generate_pdf(result,company_size,industry,budget,years):
        buffer=BytesIO()
        doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=1.8*cm,leftMargin=1.8*cm,topMargin=2*cm,bottomMargin=2*cm)
        styles=getSampleStyleSheet()
        title_s=ParagraphStyle("title",parent=styles["Title"],fontSize=20,spaceAfter=6,textColor=colors.HexColor("#1a4a7a"),alignment=TA_CENTER)
        sub_s=ParagraphStyle("sub",parent=styles["Normal"],fontSize=11,textColor=colors.grey,alignment=TA_CENTER,spaceAfter=16)
        h2_s=ParagraphStyle("h2",parent=styles["Heading2"],fontSize=14,textColor=colors.HexColor("#1a4a7a"),spaceBefore=14,spaceAfter=7)
        body_s=ParagraphStyle("body",parent=styles["Normal"],fontSize=11,leading=15,spaceAfter=6)
        rec_s=ParagraphStyle("rec",parent=styles["Normal"],fontSize=10,leading=14,spaceAfter=4,leftIndent=10)
        story=[]
        story.append(Paragraph("Small Business Digital Transformation Advisor",title_s))
        story.append(Paragraph("Expert System Assessment Report — COM6008 Knowledge-Based Systems",sub_s))
        story.append(HRFlowable(width="100%",thickness=1.5,color=colors.HexColor("#1a6b45")))
        story.append(Spacer(1,0.4*cm))
        story.append(Paragraph("Business Profile",h2_s))
        usable=16.4*cm
        pt=Table([["Company Size",company_size],["Industry Sector",industry],
                  ["Annual Digital Budget",budget],["Years in Operation",years]],
                 colWidths=[5*cm,usable-5*cm])
        pt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eaf4fb")),
            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),11),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),]))
        story.append(pt); story.append(Spacer(1,0.4*cm))
        story.append(Paragraph("Assessment Results",h2_s))
        rt=Table([["Maturity Score",f"{result['score']} / 100"],
                  ["Digital Maturity Level",result["level"]],
                  ["Risk Level",result["risk_level"]],
                  ["Rules Fired",str(len(result["rules_triggered"]))]],
                 colWidths=[5*cm,usable-5*cm])
        rt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eaf4fb")),
            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),11),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),]))
        story.append(rt); story.append(Spacer(1,0.2*cm))
        story.append(Paragraph(result["risk_description"],body_s))
        story.append(Paragraph("Expert Recommendations",h2_s))
        pfix={"Critical":"[CRITICAL]","Important":"[IMPORTANT]","Optional":"[OPTIONAL]"}
        for rec in result["recommendations"]:
            story.append(Paragraph(f'<b>{pfix[rec["priority"]]} {rec["category"]}:</b> {rec["text"]}',rec_s))
        story.append(Paragraph("Expert Rule Trace",h2_s))
        rd=[["Rule","Category","Description","Pts"]]
        for r in result["rules_triggered"]:
            rd.append([Paragraph(f"Rule {r['id']:02d}",ParagraphStyle("rc",fontSize=9,leading=11)),
                       Paragraph(r["category"],ParagraphStyle("rc",fontSize=9,leading=11)),
                       Paragraph(r["description"],ParagraphStyle("rd",fontSize=9,leading=12,wordWrap="LTR")),
                       Paragraph(f"+{r['points']}",ParagraphStyle("rp",fontSize=9,leading=11))])
        cw=[1.4*cm,3.8*cm,usable-1.4*cm-3.8*cm-1.1*cm,1.1*cm]
        rtbl=Table(rd,colWidths=cw,repeatRows=1)
        rtbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1a6b45")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),10),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cce0f0")),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f5faff")]),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("VALIGN",(0,0),(-1,-1),"TOP")]))
        story.append(rtbl)
        story.append(Spacer(1,0.5*cm))
        story.append(HRFlowable(width="100%",thickness=0.5,color=colors.grey))
        story.append(Paragraph(
            "Generated by the Small Business Digital Transformation Advisor | "
            "Rules derived from McKinsey Digital Maturity Framework (2023) & Gartner IT Maturity Model (2024) | "
            "COM6008 Knowledge-Based Systems — Buckinghamshire New University",
            ParagraphStyle("footer",parent=styles["Normal"],fontSize=8,textColor=colors.grey,alignment=TA_CENTER,spaceBefore=8)))
        doc.build(story)
        return buffer.getvalue()

    st.markdown("<div style='height:1rem'></div>",unsafe_allow_html=True)
    st.markdown('<div class="section-header">📥 Download Full Report</div>',unsafe_allow_html=True)
    pdf_bytes=generate_pdf(result,company_size,industry,budget,years)
    st.download_button(label="📄  Download PDF Assessment Report",data=pdf_bytes,
                       file_name="digital_transformation_report.pdf",mime="application/pdf")

    st.markdown(f"""
    <div style="text-align:center;color:{T['footer_txt']};font-size:.88rem;margin-top:3rem;
                padding-top:1.5rem;border-top:1px solid {T['footer_border']};">
        COM6008 Knowledge-Based Systems in AI &nbsp;|&nbsp;
        McKinsey Digital Maturity Framework (2023) &amp; Gartner IT Maturity Model (2024)
        &nbsp;|&nbsp; Buckinghamshire New University
    </div>""",unsafe_allow_html=True)
