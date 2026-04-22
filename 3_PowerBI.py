import streamlit as st
import streamlit.components.v1 as components

st.markdown(f"""
<div class="page-title-strip">
    <div>
        <div class="page-name">📈 Power BI Dashboard</div>
        <div class="page-sub">Interactive oil market analytics — embedded from Power BI</div>
    </div>
    <span class="page-badge">INTERACTIVE</span>
</div>
""", unsafe_allow_html=True)

POWERBI_URL = "https://app.powerbi.com/view?r=eyJrIjoiMmVkMTY1ZjAtNTg2Yy00M2JhLTlhZDUtNjY1YTU0ODU0ODk0IiwidCI6IjJiYjZlNWJjLWMxMDktNDdmYi05NDMzLWMxYzZmNGZhMzNmZiIsImMiOjl9&pageName=9b0f933c3c37dc9a09ad"

components.iframe(
    src=POWERBI_URL,
    height=700,
    scrolling=True
)