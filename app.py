"""
Squad 54 - Dataset to Insights (Sprint 1)
Streamlit dashboard shell - page config, theme, and sidebar navigation.
Page content is added incrementally in later commits.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
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
GREEN = "#16a34a"
RED = "#dc2626"

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
    .kpi-delta-up {{ color: {GREEN}; font-size: 0.85rem; font-weight: 600; }}
    .kpi-delta-down {{ color: {RED}; font-size: 0.85rem; font-weight: 600; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def kpi_card(col, label, value, delta=None, positive=True):
    with col:
        with st.container(border=True):
            st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>{value}</div>", unsafe_allow_html=True)
            if delta:
                cls = "kpi-delta-up" if positive else "kpi-delta-down"
                arrow = "\u2197" if positive else "\u2198"
                st.markdown(f"<span class='{cls}'>{arrow} {delta}</span>", unsafe_allow_html=True)


def style_fig(fig):
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#374151"),
        legend=dict(orientation="h", y=1.1),
    )
    fig.update_xaxes(tickfont=dict(color="#374151"), gridcolor="#e6e9ef", linecolor="#d1d5db")
    fig.update_yaxes(tickfont=dict(color="#374151"), gridcolor="#e6e9ef", linecolor="#d1d5db")
    return fig


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
    st.markdown("<div class='section-title'>Global Sales Performance</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>{len(df):,} records loaded</div>", unsafe_allow_html=True)

    monthly = df.groupby("Order Month")["Sales"].sum().reset_index().sort_values("Order Month")
    total_revenue = df["Sales"].sum()
    avg_order_value = df.groupby("Order ID")["Sales"].sum().mean()

    last_year = df["Order Date"].dt.year.max()
    prev_year = last_year - 1
    rev_last = df[df["Order Date"].dt.year == last_year]["Sales"].sum()
    rev_prev = df[df["Order Date"].dt.year == prev_year]["Sales"].sum()
    growth = (rev_last - rev_prev) / rev_prev * 100 if rev_prev else 0

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "Total Records", f"{len(df):,}")
    kpi_card(c2, "Total Revenue", f"${total_revenue/1e6:.2f}M")
    kpi_card(c3, "Average Order Value", f"${avg_order_value:,.2f}")
    kpi_card(c4, "YoY Growth", f"{growth:+.1f}%", delta=f"{last_year} vs {prev_year}", positive=growth >= 0)

    st.write("")
    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            st.markdown("**Monthly Revenue Performance**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly["Order Month"], y=monthly["Sales"],
                mode="lines", line=dict(color=ACCENT, width=3), fill="tozeroy",
                fillcolor="rgba(47,111,235,0.08)", name="Revenue",
            ))
            st.plotly_chart(style_fig(fig), width="stretch")
    with right:
        with st.container(border=True):
            st.markdown("**Revenue by Region**")
            region_rev = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
            max_rev = region_rev.max()
            for region, rev in region_rev.items():
                pct = rev / max_rev
                st.markdown(f"<div style='display:flex;justify-content:space-between;'>"
                            f"<span style='color:#111827;font-weight:500;'>{region}</span>"
                            f"<span style='color:{TEXT_MUTED};'>${rev/1e3:,.0f}k</span></div>",
                            unsafe_allow_html=True)
                st.progress(pct)

    top_cat = df.groupby("Category")["Sales"].sum().idxmax()
    top_month = monthly.loc[monthly["Sales"].idxmax(), "Order Month"]
    st.markdown(
        f"<span class='badge'>KEY HIGHLIGHT</span> "
        f"<span style='color:{TEXT_MUTED};'>Peak revenue month was "
        f"{pd.Timestamp(top_month).strftime('%B %Y')}, led by the {top_cat} category.</span>",
        unsafe_allow_html=True,
    )


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