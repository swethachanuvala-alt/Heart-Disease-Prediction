"""
CardioSense — Heart Disease Risk Screening
Run:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="CardioSense · Heart Risk Screening", page_icon="❤️",
                   layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_css, ribbon  # noqa: E402  (after set_page_config)

inject_css()
ribbon()

pages = [
    st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/assessment.py", title="Risk Assessment", icon=":material/monitor_heart:"),
    st.Page("views/insights.py", title="Data Insights", icon=":material/insights:"),
    st.Page("views/guide.py", title="Heart Health Guide", icon=":material/eco:"),
    st.Page("views/model_lab.py", title="Model Lab", icon=":material/science:"),
    st.Page("views/about.py", title="About", icon=":material/info:"),
]
try:
    nav = st.navigation(pages, position="top")
except TypeError:                       # older Streamlit -> sidebar menu
    nav = st.navigation(pages)
nav.run()
