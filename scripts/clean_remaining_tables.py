"""
clean_remaining_tables.py

Copies the remaining 7 raw tables (not covered by dedicated cleaning
scripts) into data/processed/, parsing their date columns to datetime.
"""

import pandas as pd

RAW_DIR = "../data/raw"
PROCESSED_DIR = "../data/processed"

TABLES_WITH_DATE_COLS = {
    "01_fund_master.csv": None,
    "03_aum_by_fund_house.csv": "date",
    "04_monthly_sip_inflows.csv": None,
    "05_category_inflows.csv": None,
    "06_industry_folio_count.csv": None,
    "09_portfolio_holdings.csv": "portfolio_date",
    "10_benchmark_indices.csv": "date",
}


def main() -> None:
    """Copy each remaining table to processed/, parsing dates where present."""
    for filename, date_col in TABLES_WITH_DATE_COLS.items():
        df = pd.read_csv(f"{RAW_DIR}/{filename}")
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
        output_name = filename.replace(".csv", "_clean.csv")
        df.to_csv(f"{PROCESSED_DIR}/{output_name}", index=False)
        print(f"Saved {len(df)} rows to {PROCESSED_DIR}/{output_name}")


if __name__ == "__main__":
    main()