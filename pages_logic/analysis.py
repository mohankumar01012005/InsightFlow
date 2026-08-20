"""Analysis page: date/category/region filters, filtered KPIs, segment comparison, detailed table."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from pages_logic.theme import ACCENT, TEXT_MUTED, kpi_card, style_fig


def render(df: pd.DataFrame):
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