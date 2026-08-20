"""SQL Insights page: DuckDB queries answering key business questions."""
import duckdb
import numpy as np
import pandas as pd
import streamlit as st


def render(df: pd.DataFrame):
    st.markdown("<div class='section-title'>SQL Insights</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Business questions answered with SQL queries (via DuckDB) "
        "over the cleaned dataset.</div>",
        unsafe_allow_html=True,
    )

    con = duckdb.connect()
    con.register("orders", df)

    top_category_q = """
        SELECT "Category" AS category, SUM("Sales") AS total_sales
        FROM orders GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    """
    top_category = con.execute(top_category_q).fetchdf().iloc[0]

    top_region_q = """
        SELECT "Region" AS region, SUM("Sales") AS total_sales
        FROM orders GROUP BY 1 ORDER BY 2 DESC LIMIT 1
    """
    top_region = con.execute(top_region_q).fetchdf().iloc[0]
    total_sales_all = df["Sales"].sum()
    region_share = top_region["total_sales"] / total_sales_all * 100

    growth_q = """
        SELECT date_trunc('year', "Order Date") AS year, SUM("Sales") AS total_sales
        FROM orders GROUP BY 1 ORDER BY 1
    """
    yearly_sql = con.execute(growth_q).fetchdf()
    yearly_sql["yoy_growth"] = yearly_sql["total_sales"].pct_change() * 100
    avg_yoy = yearly_sql["yoy_growth"].mean()

    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("<span class='badge'>TOP PERFORMER</span>", unsafe_allow_html=True)
            st.caption("Which category performs best?")
            st.markdown(f"<div class='kpi-value'>{top_category['category']}</div>", unsafe_allow_html=True)
            st.caption(f"${top_category['total_sales']/1e6:.2f}M in total sales")
            with st.expander("View SQL Query"):
                st.code(top_category_q, language="sql")
    with c2:
        with st.container(border=True):
            st.markdown("<span class='badge'>REGIONAL DATA</span>", unsafe_allow_html=True)
            st.caption("Which region has the highest sales?")
            st.markdown(f"<div class='kpi-value'>{top_region['region']}</div>", unsafe_allow_html=True)
            st.caption(f"{region_share:.0f}% share of total revenue")
            with st.expander("View SQL Query"):
                st.code(top_region_q, language="sql")
    with c3:
        with st.container(border=True):
            st.markdown("<span class='badge'>GROWTH TREND</span>", unsafe_allow_html=True)
            st.caption("What is the year-over-year trend?")
            trend_word = "Growing" if avg_yoy > 0 else "Declining"
            st.markdown(f"<div class='kpi-value'>{trend_word}</div>", unsafe_allow_html=True)
            st.caption(f"Avg {avg_yoy:+.1f}% YoY across the dataset")
            with st.expander("View SQL Query"):
                st.code(growth_q, language="sql")

    st.write("")
    with st.container(border=True):
        st.markdown(f"**Sub-Category Breakdown: {top_category['category']}**")
        breakdown_q = """
            SELECT "Sub-Category" AS sub_category,
                   SUM("Sales") AS total_sales,
                   SUM("Quantity") AS units_sold,
                   AVG("Profit Margin") AS avg_margin
            FROM orders
            WHERE "Category" = ?
            GROUP BY 1 ORDER BY 2 DESC
        """
        breakdown = con.execute(breakdown_q, [top_category["category"]]).fetchdf()
        breakdown["Status"] = np.where(
            breakdown["avg_margin"] > 0.15, "High Performance",
            np.where(breakdown["avg_margin"] > 0, "Stable", "Needs Attention")
        )
        breakdown = breakdown.rename(columns={
            "sub_category": "Sub-Category", "total_sales": "Total Sales",
            "units_sold": "Units Sold", "avg_margin": "Avg Margin",
        })
        breakdown["Total Sales"] = breakdown["Total Sales"].map(lambda v: f"${v:,.0f}")
        breakdown["Avg Margin"] = breakdown["Avg Margin"].map(lambda v: f"{v*100:.1f}%")
        st.dataframe(breakdown, width="stretch", hide_index=True)
        with st.expander("View SQL Query"):
            st.code(breakdown_q, language="sql")