"""Business Insights page: computed executive summary, health index, and recommendations."""
import numpy as np
import pandas as pd
import streamlit as st


def render(df: pd.DataFrame):
    st.markdown("<div class='section-title'>Business Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Strategic recommendations derived from the analysis above.</div>",
                unsafe_allow_html=True)

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    overall_margin = total_profit / total_sales * 100
    loss_making_share = (df["Profit"] < 0).mean() * 100

    cat_profit = df.groupby("Category")["Profit"].sum().sort_values()
    weakest_category = cat_profit.index[0]
    strongest_category = cat_profit.index[-1]

    region_margin = df.groupby("Region")["Profit Margin"].mean().sort_values()
    weakest_region = region_margin.index[0]

    region_growth = df.groupby([df["Order Date"].dt.year, "Region"])["Sales"].sum().reset_index()
    last_year = df["Order Date"].dt.year.max()
    region_last = region_growth[region_growth["Order Date"] == last_year].set_index("Region")["Sales"]
    region_prev = region_growth[region_growth["Order Date"] == last_year - 1].set_index("Region")["Sales"]
    region_growth_pct = ((region_last - region_prev) / region_prev * 100).dropna().sort_values(ascending=False)
    fastest_growing_region = region_growth_pct.index[0] if len(region_growth_pct) else "N/A"

    health_index = int(np.clip(50 + overall_margin * 2 - loss_making_share, 0, 100))
    risk_level = "Low" if loss_making_share < 15 else ("Medium" if loss_making_share < 25 else "High")

    with st.container(border=True):
        left, right = st.columns([2.2, 1])
        with left:
            st.markdown("<span class='badge'>EXECUTIVE SUMMARY</span>", unsafe_allow_html=True)
            st.write(
                f"Overall profit margin across the dataset is **{overall_margin:.1f}%**, with "
                f"**{loss_making_share:.1f}%** of order lines selling at a loss. "
                f"**{strongest_category}** contributes the most profit, while **{weakest_category}** "
                f"is the weakest-margin category and the main driver of the loss-making share. "
                f"The **{weakest_region}** region has the lowest average profit margin of any region, "
                f"while **{fastest_growing_region}** was the fastest-growing region year-over-year."
            )
            m1, m2, m3 = st.columns(3)
            m1.metric("Health Index", f"{health_index}/100")
            m2.metric("Profit Margin", f"{overall_margin:.1f}%")
            m3.metric("Risk Level", risk_level)
        with right:
            st.markdown("**Priority Recommendations**")
            st.markdown(
                f"- Review discounting on **{weakest_category}** — it drags overall margin down\n"
                f"- Investigate **{weakest_region}** region's cost/discount structure — lowest margin region\n"
                f"- Double down on **{strongest_category}**, the strongest profit contributor\n"
                f"- Prioritise inventory/marketing spend in **{fastest_growing_region}**, "
                f"the fastest-growing region"
            )

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("<span class='badge'>EXPANSION OPPORTUNITY</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{fastest_growing_region}</div>", unsafe_allow_html=True)
        st.caption("Fastest revenue growth YoY")
    with c2, st.container(border=True):
        st.markdown("<span class='badge'>MARGIN RISK</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{weakest_region}</div>", unsafe_allow_html=True)
        st.caption("Lowest average profit margin by region")
    with c3, st.container(border=True):
        st.markdown("<span class='badge'>LOSS-MAKING ORDERS</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{loss_making_share:.1f}%</div>", unsafe_allow_html=True)
        st.caption("Share of order lines sold at a loss")