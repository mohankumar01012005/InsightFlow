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
    st.markdown("<div class='section-title'>Data Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Explore and filter the raw dataset to uncover patterns.</div>",
                unsafe_allow_html=True)

    min_d, max_d = df["Order Date"].min().date(), df["Order Date"].max().date()
    f1, f2, f3 = st.columns([1.6, 1, 1])
    with f1:
        date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    with f2:
        category = st.selectbox("Category", ["All Categories"] + sorted(df["Category"].unique().tolist()))
    with f3:
        region = st.selectbox("Region", ["All Regions"] + sorted(df["Region"].unique().tolist()))

    filtered = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[(filtered["Order Date"].dt.date >= start) & (filtered["Order Date"].dt.date <= end)]
    else:
        start, end = min_d, max_d
    if category != "All Categories":
        filtered = filtered[filtered["Category"] == category]
    if region != "All Regions":
        filtered = filtered[filtered["Region"] == region]

    seg_revenue = filtered["Sales"].sum()
    full_rev_same_period = df[
        (df["Order Date"].dt.date >= start) & (df["Order Date"].dt.date <= end)
    ]["Sales"].sum()
    seg_share = (seg_revenue / full_rev_same_period * 100) if full_rev_same_period else 0

    st.write("")
    c1, c2, c3 = st.columns(3)
    kpi_card(c1, "Filtered Records", f"{len(filtered):,}")
    kpi_card(c2, "Segment Revenue", f"${seg_revenue/1e3:,.1f}k")
    kpi_card(c3, "Segment Share", f"{seg_share:.1f}%", delta="of period revenue", positive=True)

    st.write("")
    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            st.markdown("**Trend Analysis** — daily revenue over the filtered period")
            daily = filtered.groupby(filtered["Order Date"].dt.date)["Sales"].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily["Order Date"], y=daily["Sales"],
                                      mode="lines", line=dict(color=ACCENT, width=2)))
            st.plotly_chart(style_fig(fig), width="stretch")
    with right:
        with st.container(border=True):
            st.markdown("**Segment Comparison**")
            seg_comp = filtered.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
            if len(seg_comp):
                best = seg_comp.idxmax()
                max_val = seg_comp.max()
                for seg, val in seg_comp.items():
                    st.markdown(f"<div style='display:flex;justify-content:space-between;'>"
                                f"<span style='color:#111827;font-weight:500;'>{seg}</span>"
                                f"<span style='color:{TEXT_MUTED};'>${val/1e3:,.0f}k</span></div>",
                                unsafe_allow_html=True)
                    st.progress(val / max_val if max_val else 0)
                st.markdown(f"<span class='badge'>Best Performer</span> {best}", unsafe_allow_html=True)
            else:
                st.caption("No data for the current filters.")

    st.write("")
    with st.container(border=True):
        st.markdown("**Detailed Results**")
        show_cols = ["Order ID", "Order Date", "Customer Name", "Region", "Category", "Sub-Category", "Sales", "Profit"]
        display_df = filtered[show_cols].sort_values("Order Date", ascending=False).head(200).rename(
            columns={"Order ID": "ID", "Order Date": "Date", "Customer Name": "Customer"}
        )
        st.dataframe(display_df, width="stretch", hide_index=True)
        st.caption(f"Showing up to 200 of {len(filtered):,} filtered records.")


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