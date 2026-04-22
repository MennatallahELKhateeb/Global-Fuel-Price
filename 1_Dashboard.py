import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
#  Data
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("global_fuel_prices_2020_2026.csv", parse_dates=["date"])
    return df

df = load_data()

global_weekly = (
    df.groupby("date")
    .agg(petrol=("petrol_usd_liter","mean"),
         diesel=("diesel_usd_liter","mean"),
         brent=("brent_crude_usd","mean"))
    .round(3).reset_index()
)

latest_date = df["date"].max()
latest_df   = df[df["date"] == latest_date].copy()

regional_latest = (
    latest_df.groupby("region")
    .agg(petrol=("petrol_usd_liter","mean"),
         diesel=("diesel_usd_liter","mean"),
         countries=("country","count"))
    .round(3).reset_index()
    .sort_values("petrol", ascending=False)
)

yearly_df = (
    df.assign(year=df["date"].dt.year)
    .groupby("year")
    .agg(avg_petrol=("petrol_usd_liter","mean"),
         avg_diesel=("diesel_usd_liter","mean"),
         avg_brent=("brent_crude_usd","mean"))
    .round(3).reset_index()
)

# ══════════════════════════════════════════════════════════════════════════════
#  Live API
# ══════════════════════════════════════════════════════════════════════════════
def fetch_live_data():
    debug = []
    try:
        key = st.secrets.get("OIL_API_KEY", "")
        debug.append(f"✅ Key found: {'YES — ' + key[:6] + '...' if key else 'NO — empty!'}")
        if not key:
            return None, "\n".join(debug)
        headers = {"Authorization": f"Token {key}"}
        r_now = requests.get(
            "https://api.oilpriceapi.com/v1/prices/latest",
            params={"by_code": "BRENT_CRUDE_USD"},
            headers=headers, timeout=8
        )
        debug.append(f"📡 /prices/latest status: {r_now.status_code}")
        r_now.raise_for_status()
        raw_now = r_now.json()
        if isinstance(raw_now.get("data"), list):
            d_now = raw_now["data"][0]
        else:
            d_now = raw_now["data"]
        current_price = d_now["price"]
        change        = d_now.get("change", None)
        change_pct    = d_now.get("change_percent", None)
        r_day = requests.get(
            "https://api.oilpriceapi.com/v1/prices/past_day",
            params={"by_code": "BRENT_CRUDE_USD"},
            headers=headers, timeout=8
        )
        prev_price = None
        if r_day.status_code == 200:
            d_day = r_day.json().get("data", [])
            if isinstance(d_day, list) and len(d_day) > 0:
                prices_sorted = sorted(d_day, key=lambda x: x.get("created_at", ""))
                prev_price = prices_sorted[0].get("price", None)
        if change is None and prev_price:
            change     = round(current_price - prev_price, 2)
            change_pct = round((change / prev_price) * 100, 2)
        momentum_pct = 50
        if change_pct is not None:
            raw = (change_pct + 5) / 10
            momentum_pct = max(0, min(100, round(raw * 100)))
        result = {
            "current_price": current_price,
            "prev_price"   : prev_price,
            "change"       : change,
            "change_pct"   : change_pct,
            "momentum_pct" : momentum_pct,
        }
        return result, "\n".join(debug)
    except Exception as e:
        debug.append(f"❌ Exception: {type(e).__name__}: {e}")
        return None, "\n".join(debug)

live, _debug_info = fetch_live_data()

# ══════════════════════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════════════════════
def change_pill_html(change, change_pct):
    if change is None:
        return "<span class='change-pill change-flat'>— N/A</span>"
    arrow = "▲" if change >= 0 else "▼"
    cls   = "change-up" if change >= 0 else "change-down"
    sign  = "+" if change >= 0 else ""
    return f"<span class='change-pill {cls}'>{arrow} {abs(change_pct):.2f}%&nbsp;&nbsp;{sign}{change:.2f}</span>"

def sentiment_pill_html(change_pct):
    if change_pct is None:
        return "<span class='sentiment-pill neutral'>Neutral</span>"
    if change_pct >= 0.5:
        return "<span class='sentiment-pill bullish'>▲ Bullish</span>"
    elif change_pct <= -0.5:
        return "<span class='sentiment-pill bearish'>▼ Bearish</span>"
    return "<span class='sentiment-pill neutral'>Neutral</span>"

# ══════════════════════════════════════════════════════════════════════════════
#  Page Header
# ══════════════════════════════════════════════════════════════════════════════
badge = "● LIVE" if live else "● DATA"
st.markdown(f"""
<div class="page-title-strip">
    <div>
        <div class="page-name">📊 Global Fuel Price Dashboard</div>
        <div class="page-sub">84 countries · 2020–2026 · Last update: {latest_date.strftime('%d %b %Y')} · {datetime.now().strftime('%H:%M')}</div>
    </div>
    <span class="page-badge">{badge}</span>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 API Debug Info"):
    st.code(_debug_info)
    st.write(f"**live value:** `{live}`")
    if st.button("🔄 Force Refresh API"):
        st.cache_data.clear()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  Metric Cards
# ══════════════════════════════════════════════════════════════════════════════
m1, m2, m3, m4 = st.columns(4)

if live:
    cp   = live["current_price"]
    pp   = live["prev_price"]
    chg  = live["change"]
    cpct = live["change_pct"]
    mom  = live["momentum_pct"]

    with m1:
        st.markdown(f"""
        <div class="api-card">
            <div>
                <span class="api-card-title">🛢 BRENT_CRUDE_USD</span>
                <span class="live-pill">● LIVE</span>
            </div>
            <div class="api-card-subtitle" style="margin-top:10px">CURRENT PRICE</div>
            <div class="api-price-main">{cp:.1f}</div>
            <div class="api-price-unit">USD / barrel</div>
            {change_pill_html(chg, cpct)}
        </div>""", unsafe_allow_html=True)

    with m2:
        pp_str    = f"${pp:.2f}" if pp else "—"
        delta_str = ('+' if chg >= 0 else '') + str(round(chg, 2)) if chg is not None else "—"
        st.markdown(f"""
        <div class="api-card">
            <div class="api-card-title">24H COMPARISON</div>
            <div style="margin-top:14px">
                <div class="api-card-subtitle">PREVIOUS PRICE</div>
                <div class="prev-price-value">{pp_str}</div>
            </div>
            <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center">
                <div>
                    <div class="api-card-subtitle">SENTIMENT</div>
                    {sentiment_pill_html(cpct)}
                </div>
                <div style="text-align:right">
                    <div class="api-card-subtitle">DELTA</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:0.9rem; font-weight:600; color:#0C3559; margin-top:3px">
                        {delta_str}
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="api-card">
            <div style="display:flex; justify-content:space-between; align-items:center">
                <div class="api-card-title">PRICE MOMENTUM</div>
                <span class="momentum-pct">{mom}%</span>
            </div>
            <div class="momentum-bar-wrap">
                <div class="momentum-bar-fill" style="width:{mom}%"></div>
            </div>
            <div class="momentum-labels">
                <span class="momentum-label">LOW</span>
                <span class="momentum-label">HIGH</span>
            </div>
            <div style="margin-top:12px">
                {change_pill_html(chg, cpct)}
            </div>
        </div>""", unsafe_allow_html=True)

    with m4:
        yoy_now  = yearly_df.iloc[-1]["avg_petrol"]
        yoy_prev = yearly_df.iloc[-2]["avg_petrol"]
        yoy_pct  = ((yoy_now - yoy_prev) / yoy_prev) * 100
        yc = "change-up" if yoy_pct >= 0 else "change-down"
        ya = "▲" if yoy_pct >= 0 else "▼"
        st.markdown(f"""
        <div class="api-card">
            <div class="api-card-title">YOY PETROL AVG</div>
            <div style="margin-top:14px">
                <div class="api-card-subtitle">CURRENT YEAR AVG</div>
                <div class="prev-price-value">${yoy_now:.3f}<span style="font-size:0.85rem;color:#7a9ab8">/L</span></div>
            </div>
            <div style="margin-top:10px">
                <span class="change-pill {yc}">{ya} {abs(yoy_pct):.1f}% vs prev year</span>
            </div>
        </div>""", unsafe_allow_html=True)

else:
    g_lat  = global_weekly.iloc[-1]
    g_prev = global_weekly.iloc[-2]
    p_chg  = g_lat["petrol"] - g_prev["petrol"]
    p_pct  = (p_chg / g_prev["petrol"]) * 100
    yoy_now  = yearly_df.iloc[-1]["avg_petrol"]
    yoy_prev = yearly_df.iloc[-2]["avg_petrol"]
    yoy_pct  = ((yoy_now - yoy_prev) / yoy_prev) * 100

    fallback_cards = [
        ("Global Avg Petrol", f"${g_lat['petrol']:.3f}", f"{'▲' if p_chg>=0 else '▼'} {abs(p_pct):.1f}%",
         "change-up" if p_chg >= 0 else "change-down"),
        ("Global Avg Diesel", f"${g_lat['diesel']:.3f}", "USD / liter", "change-flat"),
        ("Brent Crude",       f"${g_lat['brent']:.1f}",  "from dataset · API unavailable", "change-flat"),
        ("YoY Change",        f"{'▲' if yoy_pct>=0 else '▼'}{abs(yoy_pct):.1f}%", "petrol avg",
         "change-up" if yoy_pct >= 0 else "change-down"),
    ]
    for col, (label, val, sub, cls) in zip([m1, m2, m3, m4], fallback_cards):
        with col:
            st.markdown(f"""
            <div class="api-card">
                <div class="api-card-title">{label}</div>
                <div class="prev-price-value" style="margin:12px 0 8px">{val}</div>
                <span class="change-pill {cls}">{sub}</span>
            </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  Trend Chart
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Global Fuel Price Trend</div>', unsafe_allow_html=True)
period_opts = {"1Y": 52, "3Y": 156, "All": len(global_weekly)}
period = st.radio("Period:", list(period_opts.keys()), horizontal=True, index=2)
td = global_weekly.tail(period_opts[period])

fig = go.Figure()
fig.add_trace(go.Scatter(x=td["date"], y=td["petrol"], name="Petrol",
    line=dict(color="#0D8AA6", width=2.5),
    fill="tozeroy", fillcolor="rgba(13,138,166,0.08)",
    hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:.3f}/L<extra></extra>"))
fig.add_trace(go.Scatter(x=td["date"], y=td["diesel"], name="Diesel",
    line=dict(color="#04D960", width=1.8),
    hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:.3f}/L<extra></extra>"))
fig.add_trace(go.Scatter(x=td["date"], y=(td["brent"]/10).round(3),
    name="Brent÷10", line=dict(color="#0C3559", width=1.2, dash="dot"),
    hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:.2f}×10/bbl<extra></extra>"))
fig.update_layout(
    paper_bgcolor="#ffffff", plot_bgcolor="#f7f9fc", height=280,
    font=dict(family="JetBrains Mono", color="#4a6b8a", size=11),
    xaxis=dict(showgrid=False, color="#7a9ab8", linecolor="#e0e8f0"),
    yaxis=dict(showgrid=True, gridcolor="#edf2f7", color="#7a9ab8",
               tickprefix="$", ticksuffix="/L"),
    legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1, x=0,
                font=dict(color="#4a6b8a")),
    margin=dict(l=10, r=10, t=40, b=10),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  Regional Bar
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Regional Breakdown — Latest</div>', unsafe_allow_html=True)
fig_r = px.bar(
    regional_latest.sort_values("petrol"), x="petrol", y="region",
    orientation="h", color="petrol",
    color_continuous_scale=[[0, "#e8f4f8"], [0.5, "#0D8AA6"], [1, "#0C3559"]],
    hover_data={"diesel": True, "countries": True},
    labels={"petrol": "Petrol $/L", "region": ""},
)
fig_r.update_layout(
    paper_bgcolor="#ffffff", plot_bgcolor="#f7f9fc", height=280,
    margin=dict(l=10, r=10, t=10, b=10),
    coloraxis_showscale=False,
    font=dict(family="JetBrains Mono", color="#4a6b8a"),
    xaxis=dict(showgrid=True, gridcolor="#edf2f7", color="#7a9ab8"),
    yaxis=dict(color="#4a6b8a"),
)
st.plotly_chart(fig_r, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  Country Table
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Country Data — Latest</div>', unsafe_allow_html=True)
v1, v2 = st.columns([2, 2])
with v1:
    view = st.radio("View:", ["All", "By Region", "By Subsidy"], horizontal=False)
with v2:
    sort_by = st.selectbox("Sort:", ["petrol_usd_liter", "diesel_usd_liter", "tax_percentage"])

df_show = latest_df.copy()
if view == "By Region":
    r_sel = st.selectbox("Region:", sorted(df_show["region"].unique()))
    df_show = df_show[df_show["region"] == r_sel]
elif view == "By Subsidy":
    s_sel = st.selectbox("Subsidy:", sorted(df_show["subsidy_level"].unique()))
    df_show = df_show[df_show["subsidy_level"] == s_sel]

df_show = df_show.sort_values(sort_by, ascending=False).reset_index(drop=True)
cols_show = ["country", "region", "subsidy_level", "petrol_usd_liter", "diesel_usd_liter", "tax_percentage"]
df_disp = df_show[cols_show].copy()
df_disp.columns = ["Country", "Region", "Subsidy", "Petrol $/L", "Diesel $/L", "Tax %"]
st.dataframe(df_disp, use_container_width=True, height=280, hide_index=True)