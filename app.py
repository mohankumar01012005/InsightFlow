"""
Squad 54 - Dataset to Insights (Sprint 1)
Streamlit dashboard shell - page config, theme, and sidebar navigation.
Page content is added incrementally in later commits.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "superstore_clean.csv"

st.set_page_config(
    page_title="DataLens | Squad 54",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme / CSS - dark navy sidebar, light content, blue accent (matches mock)
# ---------------------------------------------------------------------------
NAVY = "#0b1526"
NAVY_2 = "#111e35"
ACCENT = "#2f6feb"
BG = "#f5f7fa"
CARD = "#ffffff"
BORDER = "#e6e9ef"
TEXT_MUTED = "#6b7280"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {BG}; }}
    section[data-testid="stSidebar"] {{
        background-color: {NAVY};
        min-width: 250px;
    }}
    section[data-testid="stSidebar"] * {{ color: #e5e9f0 !important; }}
    section[data-testid="stSidebar"] .stButton button {{
        width: 100%;
        text-align: left;
        background-color: transparent;
        border: none;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background-color: {NAVY_2};
        color: #ffffff !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 0.25rem 0.25rem;
    }}
    .kpi-label {{ color: {TEXT_MUTED}; font-size: 0.8rem; font-weight: 600;
                  text-transform: uppercase; letter-spacing: .03em; }}
    .kpi-value {{ font-size: 1.9rem; font-weight: 700; color: #111827; margin: 2px 0; }}
    .section-title {{ font-size: 1.3rem; font-weight: 700; color: #111827; margin-bottom: 0.1rem; }}
    .section-sub {{ color: {TEXT_MUTED}; font-size: 0.9rem; margin-bottom: 1rem; }}
    .badge {{
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        background-color: #e8f0fe; color: {ACCENT}; font-size: 0.75rem; font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


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
# Page placeholders - content added in later commits
# ---------------------------------------------------------------------------
def page_overview():
    st.markdown("<div class='section-title'>Overview</div>", unsafe_allow_html=True)
    st.info("Overview page content coming soon.")


def page_analysis():
    st.markdown("<div class='section-title'>Analysis</div>", unsafe_allow_html=True)
    st.info("Analysis page content coming soon.")


def page_sql_insights():
    st.markdown("<div class='section-title'>SQL Insights</div>", unsafe_allow_html=True)
    st.info("SQL Insights page content coming soon.")


def page_business_insights():
    st.markdown("<div class='section-title'>Business Insights</div>", unsafe_allow_html=True)
    st.info("Business Insights page content coming soon.")


PAGE_FUNCS = {
    "Overview": page_overview,
    "Analysis": page_analysis,
    "SQL Insights": page_sql_insights,
    "Business Insights": page_business_insights,
}
PAGE_FUNCS[st.session_state.page]()