"""
load_to_sqlite.py

Creates bluestock_mf.db using schema.sql, then loads all cleaned CSVs
from data/processed/ into their corresponding tables using SQLAlchemy.
Verifies row counts match the source CSVs after loading.
"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "../bluestock_mf.db"
SCHEMA_PATH = "schema.sql"
PROCESSED_DIR = "../data/processed"

def create_database_from_schema(db_path: str = DB_PATH, schema_path: str = SCHEMA_PATH) -> None:
    """Create a fresh SQLite database file and run the schema SQL against it.

    Args:
        db_path: Where to create the .db file.
        schema_path: Path to the schema.sql file containing CREATE TABLE statements.
    """
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"Database created at {db_path} with schema applied")

def load_dim_date(engine) -> None:
    """Generate and load dim_date with one row per day from 2022 to 2026."""
    dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="D")
    df = pd.DataFrame({
        "date_key": dates.strftime("%Y-%m-%d"),
        "full_date": dates.strftime("%Y-%m-%d"),
        "year": dates.year,
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "quarter": dates.quarter,
        "day_of_week": dates.strftime("%A"),
    })
    df.to_sql("dim_date", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into dim_date")

def load_dim_fund(engine) -> None:
    """Load dim_fund from the cleaned fund master CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/01_fund_master_clean.csv")
    df.to_sql("dim_fund", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into dim_fund")


def load_fact_performance(engine) -> None:
    """Load fact_performance from the cleaned scheme performance CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/07_scheme_performance_clean.csv")
    # Keep only columns that match the fact_performance schema
    cols = [
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio", "sortino_ratio",
        "std_dev_ann_pct", "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
        "morningstar_rating", "risk_grade",
    ]
    df = df[cols]
    df.to_sql("fact_performance", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into fact_performance")

def load_fact_nav(engine) -> None:
    """Load fact_nav from the cleaned NAV history CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/02_nav_history_clean.csv")
    df = df[["amfi_code", "date", "nav"]]
    df.to_sql("fact_nav", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into fact_nav")


def load_fact_transactions(engine) -> None:
    """Load fact_transactions from the cleaned investor transactions CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/08_investor_transactions_clean.csv")
    df.to_sql("fact_transactions", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into fact_transactions")


def load_fact_aum(engine) -> None:
    """Load fact_aum from the cleaned AUM by fund house CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/03_aum_by_fund_house_clean.csv")
    df.to_sql("fact_aum", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into fact_aum")

def verify_row_counts(engine) -> None:
    """Compare row counts in each SQLite table against their source CSVs."""
    checks = [
        ("dim_fund", f"{PROCESSED_DIR}/01_fund_master_clean.csv"),
        ("fact_nav", f"{PROCESSED_DIR}/02_nav_history_clean.csv"),
        ("fact_performance", f"{PROCESSED_DIR}/07_scheme_performance_clean.csv"),
        ("fact_transactions", f"{PROCESSED_DIR}/08_investor_transactions_clean.csv"),
        ("fact_aum", f"{PROCESSED_DIR}/03_aum_by_fund_house_clean.csv"),
    ]

    print("\n--- Row Count Verification ---")
    for table_name, csv_path in checks:
        csv_count = len(pd.read_csv(csv_path))
        db_count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", engine)["cnt"].iloc[0]
        status = "MATCH" if csv_count == db_count else "MISMATCH"
        print(f"{table_name}: CSV={csv_count}, DB={db_count} — {status}")

def load_fact_sip(engine) -> None:
    """Load fact_sip from the cleaned monthly SIP inflows CSV."""
    df = pd.read_csv(f"{PROCESSED_DIR}/04_monthly_sip_inflows_clean.csv")
    df.to_sql("fact_sip", engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into fact_sip")

def main() -> None:
    """Run the full database creation and loading workflow."""
    create_database_from_schema()
    engine = create_engine(f"sqlite:///{DB_PATH}")

    load_dim_date(engine)
    load_dim_fund(engine)
    load_fact_nav(engine)
    load_fact_performance(engine)
    load_fact_transactions(engine)
    load_fact_aum(engine)
    load_fact_sip(engine)

    verify_row_counts(engine)


if __name__ == "__main__":
    main()