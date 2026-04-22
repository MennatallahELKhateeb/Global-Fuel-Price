import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Oil Price Dashboard",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root {
    --navy:    #0C3559;
    --teal:    #0D8AA6;
    --green:   #04D960;
    --red:     #F22D1B;
    --light:   #F2F2F2;
    --white:   #ffffff;
    --dark-bg: #081828;
    --mid-bg:  #0a1f35;
    --border:  rgba(13,138,166,0.2);
    --text-main: #0C3559;
    --text-sub:  #4a6b8a;
    --text-muted:#7a9ab8;
}

* { box-sizing: border-box; }
body, .stApp { background-color: var(--light) !important; }
.stApp { color: var(--text-main); }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--navy); }
p, div, span, label { font-family: 'Space Grotesk', sans-serif; color: var(--text-sub); }

/* ─── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--dark-bg) 0%, var(--navy) 100%) !important;
    border-right: 1px solid rgba(13,138,166,0.3);
    min-width: 240px;
}
[data-testid="stSidebar"] * { color: #e0ecf5 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* ─── Sidebar header block ────────────────────────────────────────────── */
.sidebar-header {
    padding: 0;
    background: linear-gradient(135deg, #061422 0%, #0a1f35 100%);
    border-bottom: 1px solid rgba(13,138,166,0.35);
}
.sidebar-logo-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 18px 16px 10px;
}
.sidebar-logo-row img {
    height: 36px;
    width: auto;
    border-radius: 4px;
}
.sidebar-logo-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--teal) !important;
    line-height: 1.4;
}
.sidebar-title-block {
    padding: 8px 16px 18px;
}
.sidebar-title-block .dash-name {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: 0.3px;
    line-height: 1.2;
}
.sidebar-title-block .dash-sub {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.58rem !important;
    color: rgba(13,138,166,0.8) !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 3px;
}

/* ─── Nav links ───────────────────────────────────────────────────────── */
.nav-section-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.55rem !important;
    color: rgba(13,138,166,0.6) !important;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    padding: 16px 18px 6px;
}

[data-testid="stPageLink"] {
    border-radius: 8px !important;
    margin: 2px 10px !important;
    transition: all 0.18s ease !important;
}
[data-testid="stPageLink"]:hover {
    background: rgba(13,138,166,0.18) !important;
    transform: translateX(2px);
}
[data-testid="stPageLink"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.83rem !important;
    color: #93bcd4 !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px;
}
[data-testid="stPageLink"][aria-current="page"] {
    background: linear-gradient(90deg, rgba(13,138,166,0.25), rgba(4,217,96,0.08)) !important;
    border-left: 3px solid var(--teal) !important;
}
[data-testid="stPageLink"][aria-current="page"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ─── Sidebar footer ──────────────────────────────────────────────────── */
.sidebar-footer {
    position: absolute;
    bottom: 0;
    left: 0; right: 0;
    padding: 14px 16px;
    border-top: 1px solid rgba(13,138,166,0.2);
    background: rgba(6,20,34,0.6);
}
.sidebar-footer img {
    height: 28px;
    width: auto;
    opacity: 0.75;
}
.sidebar-footer-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.5rem !important;
    color: rgba(147,188,212,0.5) !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ─── Page title strip ────────────────────────────────────────────────── */
.page-title-strip {
    background: linear-gradient(90deg, var(--navy) 0%, #0a2845 60%, rgba(13,138,166,0.15) 100%);
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-left: 4px solid var(--teal);
}
.page-title-strip .page-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
}
.page-title-strip .page-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: rgba(13,138,166,0.9);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}
.page-badge {
    background: rgba(4,217,96,0.12);
    border: 1px solid rgba(4,217,96,0.35);
    color: var(--green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ─── Metric cards ────────────────────────────────────────────────────── */
.api-card {
    background: var(--white);
    border: 1px solid rgba(12,53,89,0.1);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 8px;
    box-shadow: 0 4px 16px rgba(12,53,89,0.08);
    transition: box-shadow 0.2s;
}
.api-card:hover { box-shadow: 0 6px 24px rgba(12,53,89,0.14); }
.api-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
    margin-bottom: 2px;
}
.api-card-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #9db8cc;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.live-pill {
    display: inline-block;
    background: rgba(4,217,96,0.12);
    color: #008f3a !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 600;
    letter-spacing: 0.5px;
    float: right;
    border: 1px solid rgba(4,217,96,0.3);
}
.api-price-main {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.4rem;
    font-weight: 600;
    color: var(--navy);
    line-height: 1.1;
    margin: 6px 0 2px 0;
}
.api-price-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.change-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 6px;
}
.change-up   { background: rgba(4,217,96,0.12);  color: #008f3a !important; border: 1px solid rgba(4,217,96,0.25); }
.change-down { background: rgba(242,45,27,0.1);  color: #c01000 !important; border: 1px solid rgba(242,45,27,0.2); }
.change-flat { background: rgba(12,53,89,0.06);  color: var(--text-muted) !important; }
.prev-price-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--navy);
    margin: 6px 0 2px 0;
}
.sentiment-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    margin-top: 4px;
}
.bullish { background: rgba(4,217,96,0.12);  color: #008f3a !important; border: 1px solid rgba(4,217,96,0.25); }
.bearish { background: rgba(242,45,27,0.1);  color: #c01000 !important; border: 1px solid rgba(242,45,27,0.2); }
.neutral { background: rgba(12,53,89,0.06);  color: var(--text-muted) !important; }
.momentum-bar-wrap {
    background: rgba(12,53,89,0.08);
    border-radius: 8px;
    height: 8px;
    margin: 10px 0 4px 0;
    overflow: hidden;
}
.momentum-bar-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, var(--navy) 0%, var(--teal) 50%, var(--green) 100%);
}
.momentum-labels { display: flex; justify-content: space-between; }
.momentum-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.momentum-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--navy);
    float: right;
    margin-top: -2px;
}
.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(12,53,89,0.1);
}
.live-badge {
    display: inline-block;
    background: rgba(4,217,96,0.12);
    color: #008f3a !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(4,217,96,0.3);
    margin-left: 10px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* ─── Chat ────────────────────────────────────────────────────────────── */
.chat-box {
    background: var(--white);
    border: 1px solid rgba(12,53,89,0.1);
    border-radius: 12px;
    padding: 14px;
    height: 440px;
    overflow-y: auto;
    margin-bottom: 10px;
    box-shadow: 0 2px 10px rgba(12,53,89,0.06);
}
.msg-user {
    background: rgba(12,53,89,0.08);
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px;
    margin: 8px 0 8px 32px;
    color: var(--navy) !important;
    font-size: 0.87rem;
    font-family: 'Space Grotesk', sans-serif;
    border: 1px solid rgba(12,53,89,0.1);
}
.msg-bot {
    background: linear-gradient(135deg, rgba(13,138,166,0.08), rgba(4,217,96,0.05));
    border: 1px solid rgba(13,138,166,0.2);
    border-radius: 12px 12px 12px 2px;
    padding: 10px 14px;
    margin: 8px 32px 8px 0;
    color: var(--navy) !important;
    font-size: 0.87rem;
    font-family: 'Space Grotesk', sans-serif;
}

/* ─── Header ──────────────────────────────────────────────────────────── */
[data-testid="stHeader"]     { background-color: var(--light) !important; }
[data-testid="stDecoration"] { display: none; }
hr { border-color: rgba(12,53,89,0.1); }

/* ─── Streamlit overrides ─────────────────────────────────────────────── */
.stRadio label { font-family: 'Space Grotesk', sans-serif !important; color: var(--text-sub) !important; }
.stSelectbox label { font-family: 'Space Grotesk', sans-serif !important; color: var(--text-sub) !important; }
.stDataFrame { border-radius: 10px; overflow: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Load logos as base64 ───────────────────────────────────────────────────────
def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

marwa_b64 = img_to_b64("assets/marwa_logo.png")
logo_b64  = img_to_b64("assets/logo.png")

marwa_img = f'<img src="data:image/png;base64,{marwa_b64}" style="height:32px;width:auto;">' if marwa_b64 else '<span style="color:#0D8AA6;font-weight:700;font-size:0.85rem;">Marwa Shaaban</span>'
logo_img  = f'<img src="data:image/png;base64,{logo_b64}"  style="height:28px;width:auto;">' if logo_b64  else '<span style="color:#04D960;font-size:1.1rem;">⬡</span>'


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-logo-row">
            {logo_img}
            <div class="sidebar-logo-text">Oil Price<br>Intelligence</div>
        </div>
        <div class="sidebar-title-block">
            <div class="dash-name">Global Fuel Price Dashboard</div>
            <div class="dash-sub">84 Countries · 2020–2026</div>
        </div>
    </div>
    <div class="nav-section-label">Navigation</div>
    """, unsafe_allow_html=True)


pg = st.navigation([
    st.Page("pages/1_Dashboard.py",       title="Dashboard",     icon="📊"),
    st.Page("pages/2_Chatbot.py",         title="AI Analyst",    icon="🤖"),
    st.Page("pages/3_PowerBI.py",         title="Power BI",      icon="📈"),
    st.Page("pages/4_Oil insights.py",    title="Oil Insights",  icon="🔍"),
])


with st.sidebar:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    # Spacer to push footer down
    st.markdown("""<div style="height:60vh; min-height:200px;"></div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-footer">
        {marwa_img}
        <div class="sidebar-footer-text">Data Analyst · Data Scientist</div>
    </div>
    """, unsafe_allow_html=True)

pg.run()