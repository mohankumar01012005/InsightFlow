"""Overview page: KPI cards, monthly revenue trend, revenue by region."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from pages_logic.theme import ACCENT, TEXT_MUTED, kpi_card, style_fig


def render(df: pd.DataFrame):
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