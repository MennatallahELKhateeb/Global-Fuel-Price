import streamlit as st
import pandas as pd
from groq import Groq

# ══════════════════════════════════════════════════════════════════════════════
#  تحميل الداتا
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("global_fuel_prices_2020_2026.csv", parse_dates=["date"])
    return df

df = load_data()

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
#  Context للـ AI
# ══════════════════════════════════════════════════════════════════════════════
def build_context():
    yearly_str = "\n".join([
        f"  {r.year}: بنزين ${r.avg_petrol} | ديزل ${r.avg_diesel} | برنت ${r.avg_brent}/bbl"
        for _, r in yearly_df.iterrows()
    ])
    regional_str = "\n".join([
        f"  {r.region}: بنزين ${r.petrol} | ديزل ${r.diesel} ({int(r.countries)} دولة)"
        for _, r in regional_latest.iterrows()
    ])
    top5_exp = latest_df.nlargest(5,"petrol_usd_liter")[["country","petrol_usd_liter"]].to_string(index=False)
    top5_chp = latest_df.nsmallest(5,"petrol_usd_liter")[["country","petrol_usd_liter"]].to_string(index=False)
    country_str = "\n".join([
        f"  {r.country} ({r.region}): بنزين ${r.petrol_usd_liter} | ديزل ${r.diesel_usd_liter} | دعم={r.subsidy_level} | ضريبة={r.tax_percentage}%"
        for _, r in latest_df.sort_values("petrol_usd_liter", ascending=False).iterrows()
    ])
    return f"""أنت محللة وقود عالمية. عندك البيانات التالية:
قاعدة البيانات: 27,468 سجل | 84 دولة | 7 مناطق | 2020–2026
المتوسطات السنوية:
{yearly_str}
آخر تحديث ({latest_date.strftime('%Y-%m-%d')}) — إقليمي:
{regional_str}
أغلى 5 دول (بنزين):
{top5_exp}
أرخص 5 دول (بنزين):
{top5_chp}
جميع الدول:
{country_str}
أجيبي بنفس لغة السؤال (عربي أو إنجليزي). استخدمي الأرقام الفعلية دائماً.
"""


# ══════════════════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# 🤖 AI Oil Analyst")
st.caption("اسألني بالعربي أو الإنجليزي — 84 دولة · 2020–2026")
st.divider()

# ── Session state init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ── Chat box ──────────────────────────────────────────────────────────────────
chat_html = '<div class="chat-box">'
if not st.session_state.messages:
    chat_html += """
    <p style="color:#94a3b8;text-align:center;margin-top:40px;
              font-family:'DM Mono',monospace;font-size:0.82rem;line-height:2.2">
    👋 جرب اسألني:<br>
    <em>"أرخص وأغلى 5 دول في البنزين؟"</em><br>
    <em>"قارن أوروبا vs الشرق الأوسط"</em><br>
    <em>"تأثير 2022 على الأسعار؟"</em><br>
    <em>"Which countries have Very High subsidies?"</em>
    </p>"""
for msg in st.session_state.messages:
    cls  = "msg-user" if msg["role"] == "user" else "msg-bot"
    icon = "👤" if msg["role"] == "user" else "🤖"
    content = msg["content"].replace("\n", "<br>")
    chat_html += f'<div class="{cls}">{icon} {content}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Quick suggestions ─────────────────────────────────────────────────────────
suggestions = [
    "أرخص وأغلى 5 دول في البنزين؟",
    "قارن أوروبا vs الشرق الأوسط",
    "تأثير أزمة 2022 على الأسعار",
    "أكثر الدول دعماً للوقود؟",
    "ما علاقة الضريبة بسعر البنزين؟",
    "Which region has cheapest fuel?",
]
sg1, sg2 = st.columns(2)
for i, s in enumerate(suggestions):
    with (sg1 if i % 2 == 0 else sg2):
        if st.button(s, key=f"sg_{i}", use_container_width=True):
            st.session_state.pending_question = s

user_input = st.chat_input("اسألني عن الداتا...")

question = user_input
if question is None and st.session_state.pending_question is not None:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_ctx = build_context()
        full_messages = [{"role": "system", "content": system_ctx}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            max_tokens=800,
        )
        answer = res.choices[0].message.content
    except KeyError:
        answer = "⚠️ أضيفي GROQ_API_KEY في ملف .streamlit/secrets.toml"
    except Exception as e:
        answer = f"⚠️ خطأ: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

if st.session_state.messages:
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with st.expander("⚙️ إعداد الـ API Keys"):
    st.markdown("""
أنشئ ملف `.streamlit/secrets.toml` وأضف:
```toml
GROQ_API_KEY = "gsk_..."
OIL_API_KEY  = "your_oilpriceapi_key"
```
""")