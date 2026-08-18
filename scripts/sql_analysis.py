"""
Squad 54 - Dataset to Insights (Sprint 1)
SQL Analysis (PRD 5.4): answer business questions using SQL via DuckDB
over the cleaned dataset.

Run with: python scripts/sql_analysis.py
"""
from pathlib import Path

import duckdb
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "superstore_clean.csv"


def load() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date", "Order Month"])


def run_query(con, title: str, query: str, params=None) -> pd.DataFrame:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(query.strip())
    print("-" * 60)
    result = con.execute(query, params) if params else con.execute(query)
    result_df = result.fetchdf()
    print(result_df.to_string(index=False))
    return result_df


if __name__ == "__main__":
    df = load()
    con = duckdb.connect()
    con.register("orders", df)

    # Q1: Which category performs best? (filtering + grouping + aggregation + sorting)
    run_query(con, "Q1: Best-performing category by total sales", """
        SELECT "Category" AS category,
               SUM("Sales") AS total_sales,
               SUM("Profit") AS total_profit,
               COUNT(DISTINCT "Order ID") AS orders
        FROM orders
        GROUP BY 1
        ORDER BY total_sales DESC
    """)

    # Q2: Which region has the highest sales / share of total? (ranking)
    total_sales_all = df["Sales"].sum()
    run_query(con, "Q2: Sales and share by region", f"""
        SELECT "Region" AS region,
               SUM("Sales") AS total_sales,
               ROUND(SUM("Sales") / {total_sales_all} * 100, 1) AS pct_of_total
        FROM orders
        GROUP BY 1
        ORDER BY total_sales DESC
    """)

    # Q3: Overall month-on-month growth trend (time-based analysis)
    monthly = run_query(con, "Q3: Monthly sales with month-on-month growth", """
        SELECT date_trunc('month', "Order Date") AS month,
               SUM("Sales") AS total_sales
        FROM orders
        GROUP BY 1
        ORDER BY 1
    """)
    monthly["mom_growth_pct"] = (monthly["total_sales"].pct_change() * 100).round(1)
    print("\nAverage month-on-month growth:", f"{monthly['mom_growth_pct'].mean():.1f}%")

    # Q4: Top 5 sub-categories within the best category (ranking within a filter)
    top_category = con.execute(
        'SELECT "Category" FROM orders GROUP BY 1 ORDER BY SUM("Sales") DESC LIMIT 1'
    ).fetchone()[0]
    run_query(
        con,
        f"Q4: Sub-category breakdown within top category ({top_category})",
        """
        SELECT "Sub-Category" AS sub_category,
               SUM("Sales") AS total_sales,
               ROUND(AVG("Profit Margin") * 100, 1) AS avg_margin_pct,
               SUM("Quantity") AS units_sold
        FROM orders
        WHERE "Category" = ?
        GROUP BY 1
        ORDER BY total_sales DESC
        LIMIT 5
        """,
        params=[top_category],
    )

    # Q5: Which region is losing money on average? (filtering on aggregated result)
    run_query(con, "Q5: Regions with negative average profit margin", """
        SELECT "Region" AS region,
               ROUND(AVG("Profit Margin") * 100, 1) AS avg_margin_pct,
               SUM("Sales") AS total_sales
        FROM orders
        GROUP BY 1
        HAVING AVG("Profit Margin") < 0
        ORDER BY avg_margin_pct
    """)

    # Q6: Top 5 customers by total spend (ranking)
    run_query(con, "Q6: Top 5 customers by total sales", """
        SELECT "Customer Name" AS customer,
               "Segment" AS segment,
               SUM("Sales") AS total_sales,
               COUNT(DISTINCT "Order ID") AS orders
        FROM orders
        GROUP BY 1, 2
        ORDER BY total_sales DESC
        LIMIT 5
    """)