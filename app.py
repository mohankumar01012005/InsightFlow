"""
Squad 54 - Dataset to Insights (Sprint 1)
Streamlit dashboard entry point - page config, theme, sidebar navigation.
Each page's logic lives in its own module under pages_logic/.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from pages_logic import overview, analysis, sql_insights, business_insights
from pages_logic.theme import inject_css

DATA_PATH = Path(__file__).parent / "data" / "superstore_clean.csv"

st.set_page_config(
    page_title="DataLens | Squad 54",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date", "Order Month"])


df = load_data()

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Overview"

PAGES = ["Overview", "Analysis", "SQL Insights", "Business Insights"]

with st.sidebar:
    st.markdown(
        "<div style='padding:14px 6px 4px 6px;'>"
        "<span style='font-size:1.3rem;font-weight:800;'>\U0001F4CA DataLens</span><br>"
        "<span style='font-size:0.75rem;color:#8b93a7;'>SQUAD 54 · SPRINT 1</span>"
        "</div><hr style='border-color:#22304a;margin:10px 0;'>",
        unsafe_allow_html=True,
    )
    for p in PAGES:
        prefix = "\u25CF " if st.session_state.page == p else "\u25CB "
        if st.button(prefix + p, key=f"nav_{p}"):
            st.session_state.page = p
    st.markdown("<hr style='border-color:#22304a;margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown(
        f"<span style='font-size:0.75rem;color:#8b93a7;'>Dataset: Sample Superstore"
        f"<br>{len(df):,} records</span>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Dispatch to the active page's module
# ---------------------------------------------------------------------------
PAGE_MODULES = {
    "Overview": overview,
    "Analysis": analysis,
    "SQL Insights": sql_insights,
    "Business Insights": business_insights,
}
PAGE_MODULES[st.session_state.page].render(df)