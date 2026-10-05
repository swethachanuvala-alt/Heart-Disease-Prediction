"""Natural red design system: palette, global CSS, HTML helpers and Plotly styling."""
from __future__ import annotations

import streamlit as st

# Every red used in the app (light -> dark)
PALETTE = {
    "Blush": "#FFF1EE", "Rose petal": "#FADBD8", "Salmon": "#F5A9A0", "Coral": "#EF6F6C",
    "Poppy": "#E63946", "Crimson": "#C1121F", "Cherry": "#A4161A", "Garnet": "#8B0F1A",
    "Burgundy": "#660708", "Wine": "#4A0A12", "Oxblood": "#370617",
}
SAGE = "#6B9A6F"       # natural leaf accent (low-risk / healthy)
RED_SEQ = ["#FADBD8", "#F5A9A0", "#EF6F6C", "#E63946", "#C1121F", "#8B0F1A", "#4A0A12"]
HIGH = "#C1121F"
LOW = "#6B9A6F"
SOFT = "#F5A9A0"


def html(markup: str) -> None:
    """Render raw HTML (blank lines / indentation would break Markdown's HTML blocks, so strip them)."""
    st.markdown(h(markup), unsafe_allow_html=True)


def h(markup: str) -> str:
    return "\n".join(line.strip() for line in markup.splitlines() if line.strip())


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,800&family=DM+Sans:wght@400;500;600;700&display=swap');
:root{ --blush:#FFF1EE; --petal:#FADBD8; --salmon:#F5A9A0; --coral:#EF6F6C; --poppy:#E63946; --crimson:#C1121F;
  --cherry:#A4161A; --garnet:#8B0F1A; --burg:#660708; --wine:#4A0A12; --ink:#3A0D12; --cream:#FFF8F3; --sand:#F6E7DC; --sage:#6B9A6F; }
html, body, [class*="css"], .stApp{ font-family:'DM Sans',sans-serif; color:var(--ink); }
h1,h2,h3,h4,.serif{ font-family:'Fraunces',Georgia,serif !important; letter-spacing:-.01em; color:var(--wine); }

.stApp{
  background:
    radial-gradient(900px 520px at 100% -5%, rgba(239,111,108,.20), transparent 60%),
    radial-gradient(700px 480px at -5% 25%, rgba(107,154,111,.14), transparent 60%),
    radial-gradient(800px 520px at 60% 110%, rgba(193,18,31,.10), transparent 60%),
    linear-gradient(180deg,#FFF8F3 0%,#FDF1EA 100%);
  background-attachment:fixed;
}
[data-testid="stHeader"]{ background:rgba(255,248,243,.82); backdrop-filter:blur(12px); border-bottom:1px solid rgba(193,18,31,.10); }
#MainMenu, footer{ visibility:hidden; }
.block-container{ padding-top:1.4rem; padding-bottom:3rem; max-width:1180px; }

/* ---------- ribbon (site header) ---------- */
.ribbon{ display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:.7rem 1.2rem; margin-bottom:1.3rem;
  background:#fff; border:1px solid rgba(193,18,31,.12); border-radius:18px; box-shadow:0 8px 28px rgba(122,17,19,.08); }
.brand{ display:flex; align-items:center; gap:.65rem; }
.brand img{ width:34px !important; }
.brand b{ font-family:'Fraunces',serif; font-size:1.35rem; color:var(--wine); }
.brand span{ color:#9A5B5F; font-size:.85rem; margin-left:.2rem; }
.rib-pill{ font-size:.78rem; font-weight:600; color:var(--cherry); background:var(--blush); border:1px solid var(--petal); padding:.32rem .8rem; border-radius:99px; white-space:nowrap; }

/* ---------- hero ---------- */
.eyebrow{ display:inline-flex; align-items:center; gap:.5rem; padding:.38rem .95rem; border-radius:99px; background:#fff;
  border:1px solid var(--petal); color:var(--cherry); font-weight:600; font-size:.82rem; box-shadow:0 4px 14px rgba(193,18,31,.08); }
.dot{ width:8px; height:8px; border-radius:50%; background:var(--crimson); animation:blink 1.2s ease-in-out infinite; }
@keyframes blink{ 50%{ opacity:.25; transform:scale(.7); } }
.hero-title{ font-family:'Fraunces',serif; font-weight:700; font-size:3.7rem; line-height:1.04; color:var(--wine); margin:1rem 0 .9rem; }
.hero-title em{ font-style:italic; color:var(--crimson); }
.hero-sub{ font-size:1.12rem; line-height:1.7; color:#6B3A3F; max-width:34rem; }
.hero-visual{ position:relative; }
.float-card{ position:absolute; background:#fff; border-radius:16px; padding:.65rem .95rem; box-shadow:0 14px 34px rgba(122,17,19,.18);
  border:1px solid rgba(193,18,31,.10); font-size:.8rem; color:#7A5256; animation:floaty 5s ease-in-out infinite; }
.float-card b{ display:block; font-family:'Fraunces',serif; font-size:1.25rem; color:var(--wine); line-height:1.1; }
@keyframes floaty{ 0%,100%{ transform:translateY(0);} 50%{ transform:translateY(-9px);} }
.trust{ display:flex; gap:1.4rem; flex-wrap:wrap; margin-top:1.4rem; color:#7A4A4F; font-size:.9rem; font-weight:500; }

/* ---------- cards ---------- */
.card{ background:#fff; border:1px solid rgba(193,18,31,.10); border-radius:24px; padding:1.4rem 1.5rem;
  box-shadow:0 12px 36px rgba(122,17,19,.08); transition:transform .25s ease, box-shadow .25s ease; height:100%; }
.card:hover{ transform:translateY(-5px); box-shadow:0 20px 48px rgba(193,18,31,.16); }
.card h4{ margin:.7rem 0 .35rem; font-size:1.2rem; }
.card p{ color:#6B3A3F; font-size:.95rem; line-height:1.6; margin:0; }
.card .tag{ font-size:.72rem; font-weight:700; letter-spacing:.12em; color:var(--crimson); }
.card.tint{ background:linear-gradient(145deg,#fff 0%,#FFF1EE 100%); }
.card.dark{ background:linear-gradient(145deg,#8B0F1A,#4A0A12); color:#FFE9E5; border:0; }
.card.dark h4,.card.dark p{ color:#FFE9E5; }

.kpi{ background:#fff; border:1px solid rgba(193,18,31,.10); border-radius:20px; padding:1.1rem 1.3rem; box-shadow:0 10px 30px rgba(122,17,19,.07);
  border-left:6px solid var(--crimson); }
.kpi .v{ font-family:'Fraunces',serif; font-weight:700; font-size:2.1rem; color:var(--wine); line-height:1.1; }
.kpi .l{ color:#8A5A5E; font-size:.85rem; margin-top:.2rem; }

.section-title{ font-family:'Fraunces',serif; font-weight:700; font-size:2rem; color:var(--wine); margin:2.6rem 0 .2rem; }
.section-sub{ color:#8A5A5E; margin-bottom:1.1rem; }
.page-title{ font-family:'Fraunces',serif; font-weight:700; font-size:2.6rem; color:var(--wine); margin:.2rem 0 0; }
.page-title em{ color:var(--crimson); font-style:italic; }
.page-sub{ color:#7A4A4F; font-size:1.05rem; margin:.3rem 0 1.4rem; }

.band{ background:linear-gradient(120deg,#A4161A,#660708); color:#FFE9E5; border-radius:28px; padding:2rem 2.2rem; box-shadow:0 24px 56px rgba(102,7,8,.35); }
.band h3{ color:#fff !important; margin:0 0 .4rem; }
.band p{ color:#FFD9D3; margin:0; }

/* ---------- result ---------- */
.verdict{ border-radius:26px; padding:1.5rem 1.7rem; position:relative; overflow:hidden; color:#fff; }
.verdict.hi{ background:linear-gradient(135deg,#8B0F1A 0%,#C1121F 60%,#E63946 100%); box-shadow:0 22px 54px rgba(193,18,31,.38); }
.verdict.mid{ background:linear-gradient(135deg,#B5483A 0%,#E4694F 70%,#F19A7E 100%); box-shadow:0 22px 54px rgba(228,105,79,.35); }
.verdict.lo{ background:linear-gradient(135deg,#3E6B49 0%,#6B9A6F 100%); box-shadow:0 22px 54px rgba(79,122,87,.35); }
.verdict .t{ font-family:'Fraunces',serif; font-weight:700; font-size:2rem; line-height:1.1; color:#fff; }
.verdict .s{ margin-top:.45rem; opacity:.95; }
.pill{ display:inline-block; padding:.28rem .8rem; border-radius:99px; font-size:.8rem; font-weight:600; background:rgba(255,255,255,.2); margin:.7rem .4rem 0 0; color:#fff; }
.tip{ background:#fff; border:1px solid var(--petal); border-left:5px solid var(--crimson); border-radius:14px; padding:.8rem 1rem; margin:.5rem 0; font-size:.95rem; }
.tip.leaf{ border-left-color:var(--sage); }
.note{ background:var(--blush); border:1px dashed var(--salmon); color:#7A3A3F; border-radius:14px; padding:.8rem 1rem; font-size:.9rem; }
.alert{ background:#FFF0F0; border:1px solid #F5B5B5; border-left:6px solid var(--crimson); border-radius:14px; padding:1rem 1.2rem; color:#6B1018; }

.chip{ display:inline-block; margin:.25rem .3rem .25rem 0; padding:.35rem .85rem; border-radius:99px; background:#fff; border:1px solid var(--petal); color:var(--cherry); font-size:.85rem; font-weight:600; }
.dtable{ width:100%; border-collapse:separate; border-spacing:0; border-radius:16px; overflow:hidden; border:1px solid var(--petal); background:#fff; }
.dtable th{ background:var(--crimson); color:#fff; text-align:left; padding:.7rem 1rem; font-family:'Fraunces',serif; font-weight:600; }
.dtable td{ padding:.65rem 1rem; border-top:1px solid #F7E1DC; font-size:.93rem; }
.dtable tr:nth-child(even) td{ background:#FFF8F5; }
.dtable tr.best td{ background:#FDE3DE; font-weight:700; }
.bar-row{ display:flex; align-items:center; gap:.9rem; margin:.65rem 0; }
.bar-label{ width:150px; font-weight:600; font-size:.93rem; }
.bar-track{ flex:1; height:14px; border-radius:99px; background:#F8E3DE; overflow:hidden; }
.bar-fill{ height:100%; border-radius:99px; background:linear-gradient(90deg,#F5A9A0,#E63946,#8B0F1A); }
.bar-val{ width:48px; text-align:right; color:#8A5A5E; font-size:.9rem; font-variant-numeric:tabular-nums; }
.swatches{ display:flex; border-radius:18px; overflow:hidden; box-shadow:0 12px 32px rgba(122,17,19,.18); }
.sw{ flex:1; padding:2rem .2rem .6rem; text-align:center; font-size:.66rem; font-weight:700; transition:flex .3s ease; }
.sw:hover{ flex:2.4; }
.tl{ border-left:3px solid var(--salmon); margin-left:.6rem; padding-left:1.4rem; }
.tl-item{ position:relative; margin-bottom:1.2rem; }
.tl-item::before{ content:""; position:absolute; left:-1.95rem; top:.3rem; width:14px; height:14px; border-radius:50%; background:var(--crimson); box-shadow:0 0 0 4px #FADBD8; }
.tl-item b{ font-family:'Fraunces',serif; font-size:1.05rem; color:var(--wine); }
.tl-item span{ display:block; color:#7A4A4F; font-size:.93rem; }
.footer{ text-align:center; color:#9A6A6E; font-size:.85rem; margin-top:3.2rem; padding-top:1.4rem; border-top:1px solid var(--petal); }
.footer b{ color:var(--cherry); }

/* ---------- Streamlit widgets ---------- */
.stButton>button, .stFormSubmitButton>button, .stDownloadButton>button{ background:linear-gradient(90deg,#A4161A,#E63946); color:#fff; border:0; border-radius:14px; font-weight:700;
  padding:.7rem 1.4rem; box-shadow:0 10px 26px rgba(193,18,31,.35); transition:transform .2s ease, box-shadow .2s ease; }
.stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover{ transform:translateY(-2px); box-shadow:0 16px 34px rgba(193,18,31,.45); color:#fff; border:0; }
.stFormSubmitButton>button{ width:100%; font-size:1.05rem; }
[data-testid="stForm"]{ background:#fff; border:1px solid rgba(193,18,31,.12); border-radius:24px; padding:1.4rem; box-shadow:0 12px 36px rgba(122,17,19,.08); }
[data-testid="stPageLink-NavLink"]{ background:#fff; border:1px solid var(--salmon); border-radius:14px; padding:.55rem 1rem; }
[data-testid="stPageLink-NavLink"]:hover{ background:var(--blush); }
.stTabs [data-baseweb="tab-list"]{ gap:.35rem; }
.stTabs [data-baseweb="tab"]{ background:#fff; border:1px solid var(--petal); border-radius:12px 12px 0 0; padding:.5rem 1.1rem; }
.stTabs [aria-selected="true"]{ background:var(--petal); }
[data-testid="stExpander"]{ background:#fff; border:1px solid var(--petal); border-radius:16px; }
[data-testid="stMetric"]{ background:#fff; border:1px solid var(--petal); border-radius:18px; padding:.9rem 1.1rem; }
@media (max-width:760px){ .hero-title{ font-size:2.5rem; } .page-title{ font-size:2rem; } .rib-pill{ display:none; } .float-card{ display:none; } }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def ribbon() -> None:
    from . import art
    html(f"""
    <div class="ribbon">
      <div class="brand">{art.img(art.pulse_heart_icon(), "34px", alt="logo")}<b>CardioSense</b><span>AI heart-risk screening</span></div>
      <div class="rib-pill">Educational demo · not a medical device</div>
    </div>
    """)


def page_header(title: str, accent: str, subtitle: str) -> None:
    html(f'<div class="page-title">{title} <em>{accent}</em></div><div class="page-sub">{subtitle}</div>')


def section(title: str, subtitle: str = "") -> None:
    sub = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    html(f'<div class="section-title">{title}</div>{sub}')


def kpi(value: str, label: str) -> str:
    return f'<div class="kpi"><div class="v">{value}</div><div class="l">{label}</div></div>'


def card(icon_html: str, title: str, text: str, tag: str = "", cls: str = "") -> str:
    tag_html = f'<div class="tag">{tag}</div>' if tag else ""
    return h(f'<div class="card {cls}">{icon_html}{tag_html}<h4>{title}</h4><p>{text}</p></div>')


def footer() -> None:
    html('<div class="footer"><b>CardioSense</b> · Logistic Regression heart-risk model · Built with Streamlit<br>'
         'For learning and demonstration only. It is <b>not</b> a medical device and does not give medical advice, diagnosis or treatment. '
         'If you have chest pain or other emergency symptoms, call your local emergency number now.</div>')


def style_fig(fig, height: int = 380, legend: bool = True):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#3A0D12", size=13),
        margin=dict(l=10, r=10, t=50, b=10),
        colorway=["#C1121F", "#F5A9A0", "#8B0F1A", "#6B9A6F", "#EF6F6C", "#4A0A12"],
        title=dict(font=dict(family="Fraunces, serif", size=18, color="#4A0A12")),
        showlegend=legend, legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#4A0A12", font=dict(color="#fff")),
    )
    fig.update_xaxes(gridcolor="rgba(193,18,31,.10)", zerolinecolor="rgba(193,18,31,.25)", linecolor="rgba(193,18,31,.25)")
    fig.update_yaxes(gridcolor="rgba(193,18,31,.10)", zerolinecolor="rgba(193,18,31,.25)", linecolor="rgba(193,18,31,.25)")
    return fig
