"""
Squad 54 - Dataset to Insights (Sprint 1)
Exploratory Data Analysis (PRD 5.3): category/region/segment trends + outliers.

Run with: python scripts/eda.py
Outputs: printed summary tables in the terminal, and chart images saved to
eda_outputs/ for use in the PRD write-up / mentor updates.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no GUI needed - just save PNGs
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "superstore_clean.csv"
OUT_DIR = Path(__file__).parent.parent / "eda_outputs"
OUT_DIR.mkdir(exist_ok=True)


def load() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date", "Order Month"])


def summarize_by(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    summary = df.groupby(group_col).agg(
        orders=("Order ID", "nunique"),
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
        avg_discount=("Discount", "mean"),
        avg_margin=("Profit Margin", "mean"),
    ).sort_values("total_sales", ascending=False)
    summary["total_sales"] = summary["total_sales"].round(2)
    summary["total_profit"] = summary["total_profit"].round(2)
    summary["avg_discount"] = (summary["avg_discount"] * 100).round(1)
    summary["avg_margin"] = (summary["avg_margin"] * 100).round(1)
    return summary


def plot_bar(summary: pd.DataFrame, value_col: str, title: str, fname: str, ylabel: str):
    fig, ax = plt.subplots(figsize=(7, 4))
    summary[value_col].plot(kind="bar", ax=ax, color="#2f6feb")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    fig.savefig(OUT_DIR / fname, dpi=150)
    plt.close(fig)


def detect_outliers(df: pd.DataFrame, col: str) -> pd.DataFrame:
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    return outliers, lower, upper


if __name__ == "__main__":
    df = load()

    print("=" * 60)
    print("CATEGORY TRENDS")
    print("=" * 60)
    cat_summary = summarize_by(df, "Category")
    print(cat_summary)
    plot_bar(cat_summary, "total_sales", "Total Sales by Category", "sales_by_category.png", "Sales ($)")
    plot_bar(cat_summary, "avg_margin", "Average Profit Margin by Category (%)", "margin_by_category.png", "Margin (%)")

    print("\n" + "=" * 60)
    print("REGION TRENDS")
    print("=" * 60)
    region_summary = summarize_by(df, "Region")
    print(region_summary)
    plot_bar(region_summary, "total_sales", "Total Sales by Region", "sales_by_region.png", "Sales ($)")

    print("\n" + "=" * 60)
    print("SEGMENT TRENDS")
    print("=" * 60)
    segment_summary = summarize_by(df, "Segment")
    print(segment_summary)
    plot_bar(segment_summary, "total_sales", "Total Sales by Segment", "sales_by_segment.png", "Sales ($)")

    print("\n" + "=" * 60)
    print("MONTHLY TREND")
    print("=" * 60)
    monthly = df.groupby("Order Month")["Sales"].sum()
    fig, ax = plt.subplots(figsize=(9, 4))
    monthly.plot(ax=ax, color="#2f6feb", linewidth=2)
    ax.set_title("Monthly Sales Trend")
    ax.set_ylabel("Sales ($)")
    ax.set_xlabel("")
    plt.tight_layout()
    fig.savefig(OUT_DIR / "monthly_sales_trend.png", dpi=150)
    plt.close(fig)
    print(f"Date range: {monthly.index.min()} to {monthly.index.max()}")
    print(f"Peak month: {monthly.idxmax()} (${monthly.max():,.2f})")
    print(f"Lowest month: {monthly.idxmin()} (${monthly.min():,.2f})")

    print("\n" + "=" * 60)
    print("OUTLIER DETECTION (IQR method)")
    print("=" * 60)
    for col in ["Sales", "Profit", "Discount"]:
        outliers, lower, upper = detect_outliers(df, col)
        print(f"\n{col}: normal range [{lower:.2f}, {upper:.2f}]")
        print(f"  {len(outliers)} outlier rows ({len(outliers) / len(df) * 100:.1f}% of data)")
        if len(outliers):
            direction = "above upper bound" if col != "Discount" else "outside range"
            top = outliers.reindex(outliers[col].abs().sort_values(ascending=False).index).head(3)
            print(f"  Top 3 by magnitude:")
            print(top[["Order ID", "Category", "Sales", "Profit", "Discount"]].to_string(index=False))

    print(f"\nCharts saved to {OUT_DIR}/")