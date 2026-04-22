import streamlit as st

st.markdown("""
<style>
/* ── Insights-specific ── */
.ins-hero {
    background: linear-gradient(135deg, #0C3559 0%, #081e35 60%, #0a2845 100%);
    border-radius: 16px;
    padding: 48px 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    border-left: 4px solid #0D8AA6;
}
.ins-hero::before {
    content: '🛢️';
    position: absolute;
    right: 40px; top: 30px;
    font-size: 88px;
    opacity: 0.07;
    line-height: 1;
}
.ins-hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #0D8AA6;
    border: 1px solid rgba(13,138,166,0.4);
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.ins-hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(30px, 4vw, 50px);
    font-weight: 800;
    color: #f0f8ff;
    line-height: 1.1;
    margin: 0 0 8px;
}
.ins-hero-title em {
    font-style: normal;
    color: #04D960;
}
.ins-hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: rgba(13,138,166,0.7);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 14px;
}

/* ── Section label ── */
.ins-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7a9ab8;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.ins-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(12,53,89,0.12);
    max-width: 260px;
}

/* ── Narrative cards ── */
.ins-card {
    background: #ffffff;
    border: 1px solid rgba(12,53,89,0.1);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(12,53,89,0.06);
    border-left: 4px solid rgba(12,53,89,0.08);
}
.ins-card.accent {
    border-left-color: #0D8AA6;
    background: linear-gradient(to right, rgba(13,138,166,0.04), #ffffff);
}
.ins-card-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    color: #b0c8dc;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.ins-card p {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.96rem;
    line-height: 1.85;
    color: #3a5878;
    margin: 0;
}
.ins-card p strong { color: #0C3559; font-weight: 700; }
.ins-card.accent p { color: #0a3050; }
.ins-card.accent p strong { color: #0D8AA6; }

/* ── Driver pills ── */
.ins-drivers {
    display: flex;
    gap: 12px;
    margin: 28px 0;
    flex-wrap: wrap;
}
.ins-driver {
    flex: 1;
    min-width: 140px;
    background: #f5f9fc;
    border: 1px solid rgba(12,53,89,0.1);
    border-radius: 12px;
    padding: 18px 18px 14px;
    text-align: center;
    transition: box-shadow 0.2s;
}
.ins-driver:hover { box-shadow: 0 4px 14px rgba(12,53,89,0.1); }
.ins-driver-icon { font-size: 22px; margin-bottom: 10px; }
.ins-driver-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #7a9ab8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}
.ins-driver-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #0C3559;
}

/* ── Key insight card ── */
.ins-insight {
    background: linear-gradient(135deg, #0C3559 0%, #081e35 100%);
    border-radius: 14px;
    padding: 32px 36px;
    margin-top: 8px;
    position: relative;
    overflow: hidden;
    border-left: 4px solid #04D960;
}
.ins-insight::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(13,138,166,0.2) 0%, transparent 70%);
}
.ins-insight-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 3px;
    color: #04D960;
    text-transform: uppercase;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.ins-insight-tag::before { content: '📌'; font-size: 0.85rem; }
.ins-insight p {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.02rem;
    line-height: 1.8;
    color: #c8dce9;
    margin: 0;
}
.ins-insight p strong { color: #04D960; font-weight: 700; }

/* ── Stats strip ── */
.ins-stats {
    display: flex;
    gap: 1px;
    margin-top: 28px;
    background: rgba(12,53,89,0.1);
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(12,53,89,0.1);
}
.ins-stat {
    flex: 1;
    background: #ffffff;
    padding: 18px 20px;
    text-align: center;
    transition: background 0.2s;
}
.ins-stat:hover { background: #f5f9fc; }
.ins-stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #0C3559;
    line-height: 1;
}
.ins-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #7a9ab8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title-strip">
    <div>
        <div class="page-name">🔍 Oil Insights</div>
        <div class="page-sub">Market Analysis Report · 2020–2026 · Global Market Dynamics</div>
    </div>
    <span class="page-badge">ANALYSIS</span>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ins-hero">
    <div class="ins-hero-tag">Market Analysis Report</div>
    <div class="ins-hero-title">Oil &amp; <em>Petroleum</em> Prices</div>
    <div class="ins-hero-sub">2020 — 2026 &nbsp;·&nbsp; Global Market Dynamics</div>
</div>
""", unsafe_allow_html=True)

# ── NARRATIVE ─────────────────────────────────────────────────────────────────
st.markdown('<div class="ins-section-label">Market Narrative</div>', unsafe_allow_html=True)

st.markdown("""
<div class="ins-card">
    <div class="ins-card-num">01 &mdash; Overview</div>
    <p>
        Between <strong>2020 and 2026</strong>, oil prices were heavily shaped by
        <strong>global instability</strong> rather than purely market fundamentals.
        The data reflects how the energy market reacted dynamically to major economic
        disruptions, geopolitical tensions, and global conflicts that influenced both
        <strong>supply and demand</strong> conditions.
    </p>
</div>

<div class="ins-card">
    <div class="ins-card-num">02 &mdash; Recovery Cycle</div>
    <p>
        The sharp initial decline was driven by a <strong>global demand shock</strong>,
        followed by a recovery phase as economic activity gradually resumed. However,
        stability was short-lived — the market entered a <strong>prolonged period of
        volatility</strong> influenced by ongoing geopolitical tensions, regional conflicts
        affecting energy supply routes, and persistent uncertainty in global trade
        and production systems.
    </p>
</div>

<div class="ins-card accent">
    <div class="ins-card-num">03 &mdash; Pattern</div>
    <p>
        These external pressures led to repeated cycles of <strong>decline, recovery,
        and fluctuation</strong> — showing that the oil market does not follow a linear
        path, but instead <strong>responds continuously to global events</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ── DRIVER PILLS ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="ins-drivers">
    <div class="ins-driver">
        <div class="ins-driver-icon">💥</div>
        <div class="ins-driver-label">Primary Trigger</div>
        <div class="ins-driver-value">Global Demand Shock</div>
    </div>
    <div class="ins-driver">
        <div class="ins-driver-icon">⚔️</div>
        <div class="ins-driver-label">Sustained Factor</div>
        <div class="ins-driver-value">Geopolitical Tensions</div>
    </div>
    <div class="ins-driver">
        <div class="ins-driver-icon">🔗</div>
        <div class="ins-driver-label">Structural Issue</div>
        <div class="ins-driver-value">Supply Chain Disruptions</div>
    </div>
    <div class="ins-driver">
        <div class="ins-driver-icon">📉</div>
        <div class="ins-driver-label">Market Behavior</div>
        <div class="ins-driver-value">Non-Linear Volatility</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KEY INSIGHT ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ins-insight">
    <div class="ins-insight-tag">Key Insight</div>
    <p>
        Oil prices during this period are best understood as a
        <strong>reflection of global instability</strong> — where geopolitical conflicts,
        economic shocks, and supply chain disruptions <strong>consistently reshape
        market behavior</strong>, overriding traditional supply-demand equilibrium models.
    </p>
</div>
""", unsafe_allow_html=True)

# ── STATS STRIP ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ins-stats">
    <div class="ins-stat">
        <div class="ins-stat-num">6</div>
        <div class="ins-stat-label">Years Covered</div>
    </div>
    <div class="ins-stat">
        <div class="ins-stat-num">84</div>
        <div class="ins-stat-label">Countries</div>
    </div>
    <div class="ins-stat">
        <div class="ins-stat-num">27K+</div>
        <div class="ins-stat-label">Observations</div>
    </div>
    <div class="ins-stat">
        <div class="ins-stat-num">3</div>
        <div class="ins-stat-label">Major Disruption Cycles</div>
    </div>
</div>
""", unsafe_allow_html=True)