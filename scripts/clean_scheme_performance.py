"""
clean_scheme_performance.py

Validates 07_scheme_performance.csv:
- Confirms all return/risk columns are numeric
- Flags statistical anomalies (values outside 3 standard deviations)
- Checks expense_ratio_pct falls within the expected 0.1%-2.5% range
"""

import pandas as pd

RAW_PATH = "../data/raw/07_scheme_performance.csv"
OUTPUT_PATH = "../data/processed/07_scheme_performance_clean.csv"

NUMERIC_COLUMNS = [
    "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct",
    "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
]

EXPENSE_RATIO_MIN = 0.1
EXPENSE_RATIO_MAX = 2.5

def clean_scheme_performance(path: str = RAW_PATH) -> pd.DataFrame:
    """Load and validate the scheme performance dataset.

    Args:
        path: Path to the raw scheme_performance CSV.

    Returns:
        The validated DataFrame, with a new 'is_anomaly' column flagging
        any row where a numeric column falls outside 3 standard deviations
        of that column's mean.
    """
    df = pd.read_csv(path)

    # Confirm all expected numeric columns are actually numeric type
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isnull().any():
            print(f"WARNING: {col} has non-numeric values that could not be converted")

    print("All return/risk columns confirmed numeric")

    # Flag anomalies: values more than 3 standard deviations from the mean
    df["is_anomaly"] = False
    for col in NUMERIC_COLUMNS:
        mean = df[col].mean()
        std = df[col].std()
        outliers = (df[col] - mean).abs() > 3 * std
        df.loc[outliers, "is_anomaly"] = True

    anomaly_count = df["is_anomaly"].sum()
    print(f"Flagged {anomaly_count} rows as statistical anomalies (>3 std dev)")

    # Validate expense_ratio_pct falls within expected range
    out_of_range = df[(df["expense_ratio_pct"] < EXPENSE_RATIO_MIN) | (df["expense_ratio_pct"] > EXPENSE_RATIO_MAX)]
    if len(out_of_range) > 0:
        print(f"WARNING: {len(out_of_range)} rows have expense_ratio_pct outside {EXPENSE_RATIO_MIN}%-{EXPENSE_RATIO_MAX}%")
    else:
        print(f"All expense_ratio_pct values fall within {EXPENSE_RATIO_MIN}%-{EXPENSE_RATIO_MAX}%")

    return df

def save_clean_data(df: pd.DataFrame, path: str = OUTPUT_PATH) -> None:
    """Save the validated DataFrame to CSV.

    Args:
        df: Validated DataFrame to save.
        path: Destination CSV path.
    """
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def main() -> None:
    """Run the full scheme_performance validation workflow."""
    df = clean_scheme_performance()
    save_clean_data(df)


if __name__ == "__main__":
    main()