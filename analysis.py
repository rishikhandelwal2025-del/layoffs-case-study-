"""
Global Tech Layoffs (2020-2023) — Case Study Analysis
-------------------------------------------------------
Reproduces every step used in the case study: inspection, cleaning,
exploratory analysis, and the key findings.

Usage:
    pip install pandas
    python scripts/analysis.py
"""

import pandas as pd

RAW_PATH = "data/layoffs_raw.csv"
CLEAN_PATH = "data/layoffs_clean.csv"


def inspect(df: pd.DataFrame) -> None:
    """Step 1: Look before touching anything."""
    print("=== SHAPE ===")
    print(df.shape)

    print("\n=== DTYPES ===")
    print(df.dtypes)

    print("\n=== NULLS PER COLUMN ===")
    print(df.isnull().sum())

    print("\n=== EXACT DUPLICATE ROWS ===")
    print(df.duplicated().sum())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2: Clean with documented judgment calls."""
    df = df.drop_duplicates()

    df["company"] = df["company"].str.strip()
    df["industry"] = df["industry"].replace(
        {"Crypto Currency": "Crypto", "CryptoCurrency": "Crypto"}
    )
    df["country"] = df["country"].str.rstrip(".")
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y", errors="coerce")

    # Judgment call: drop rows with NO layoff numbers at all.
    # Can't measure impact without at least one of the two metrics.
    before = len(df)
    df = df.dropna(subset=["total_laid_off", "percentage_laid_off"], how="all")
    print(f"Dropped {before - len(df)} rows with no layoff numbers at all.")

    df["year"] = df["date"].dt.year
    return df


def explore(df: pd.DataFrame) -> None:
    """Step 3: Exploratory analysis — the questions that produced the findings."""
    print("\n=== TOTAL LAID OFF BY YEAR ===")
    print(df.groupby("year")["total_laid_off"].sum())

    print("\n=== TOP 10 INDUSTRIES BY TOTAL LAID OFF ===")
    print(df.groupby("industry")["total_laid_off"].sum().sort_values(ascending=False).head(10))

    print("\n=== TOP 10 COMPANIES BY TOTAL LAID OFF ===")
    print(df.groupby("company")["total_laid_off"].sum().sort_values(ascending=False).head(10))

    print("\n=== TOTAL LAID OFF BY FUNDING STAGE ===")
    print(df.groupby("stage")["total_laid_off"].sum().sort_values(ascending=False).head(8))

    print("\n=== CORRELATION: FUNDS RAISED vs TOTAL LAID OFF ===")
    print(df[["funds_raised_millions", "total_laid_off"]].corr())

    print("\n=== COMPANIES THAT SHUT DOWN ENTIRELY (100% LAID OFF) ===")
    shutdowns = df[df["percentage_laid_off"] == 1][
        ["company", "total_laid_off", "stage"]
    ].sort_values("total_laid_off", ascending=False)
    print(shutdowns.head(8))


def main():
    df = pd.read_csv(RAW_PATH)
    inspect(df)

    df_clean = clean(df)
    df_clean.to_csv(CLEAN_PATH, index=False)

    explore(df_clean)


if __name__ == "__main__":
    main()
