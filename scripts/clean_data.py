import pandas as pd
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "data" / "superstore_raw.csv"
CLEAN_PATH = Path(__file__).parent.parent / "data" / "superstore_clean.csv"


def load_raw() -> pd.DataFrame:
    return pd.read_csv(RAW_PATH, encoding="utf-8-sig")


def profile(df: pd.DataFrame, label: str) -> None:
    print(f"\n--- {label} ---")
    print("shape:", df.shape)
    print("nulls per column:\n", df.isnull().sum()[df.isnull().sum() > 0])
    print("duplicate rows:", df.duplicated().sum())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 5.2 Data cleaning: standardise column names for downstream SQL use
    df.columns = [c.strip() for c in df.columns]

    # Correct data types
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # Handle missing values: Postal Code is the only column with nulls in
    # this dataset (a handful of Vermont/Burlington rows). Fill with 0 as a
    # sentinel rather than dropping real transaction rows.
    df["Postal Code"] = df["Postal Code"].fillna(0).astype(int)

    # Remove duplicate records (defensive - source has none, but this keeps
    # the pipeline correct if the raw file changes)
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)

    # Handle invalid/inconsistent data: drop rows where core numeric fields
    # are non-positive/invalid or dates failed to parse
    df = df[(df["Sales"] > 0) & (df["Quantity"] > 0)]
    df = df.dropna(subset=["Order Date", "Ship Date"])

    # Derived fields used across the dashboard
    df["Order Month"] = df["Order Date"].values.astype("datetime64[M]")
    df["Order Year"] = df["Order Date"].dt.year
    df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(4)

    print(f"\nDropped {removed} exact-duplicate rows during cleaning.")
    return df.reset_index(drop=True)


if __name__ == "__main__":
    raw = load_raw()
    profile(raw, "RAW")

    cleaned = clean(raw)
    profile(cleaned, "CLEANED")

    cleaned.to_csv(CLEAN_PATH, index=False)
    print(f"\nWrote clean dataset -> {CLEAN_PATH} ({len(cleaned)} rows)")