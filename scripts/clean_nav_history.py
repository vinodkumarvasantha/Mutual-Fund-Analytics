"""
clean_nav_history.py

Cleans 02_nav_history.csv:
- Parses dates to datetime
- Sorts by amfi_code + date
- Forward-fills missing NAV values (holidays/weekends)
- Removes duplicate rows
- Validates all NAV values are > 0
"""

import pandas as pd

RAW_PATH = "../data/raw/02_nav_history.csv"
OUTPUT_PATH = "../data/processed/02_nav_history_clean.csv"
def clean_nav_history(path: str = RAW_PATH) -> pd.DataFrame:
    """Load and clean the NAV history dataset.

    Args:
        path: Path to the raw nav_history CSV.

    Returns:
        A cleaned DataFrame: dates parsed, sorted, forward-filled,
        de-duplicated, with all NAV values validated as positive.
    """
    df = pd.read_csv(path)

    # Parse dates to proper datetime type
    df["date"] = pd.to_datetime(df["date"])

    # Sort so each fund's NAV history is in chronological order
    df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    # Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows")

    # Forward-fill missing NAV values within each fund (holidays/weekends)
    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    # Validate: all NAV values must be positive
    invalid = df[df["nav"] <= 0]
    if len(invalid) > 0:
        print(f"WARNING: {len(invalid)} rows have NAV <= 0")
    else:
        print("All NAV values are positive — validation passed")

    return df
def save_clean_data(df: pd.DataFrame, path: str = OUTPUT_PATH) -> None:
    """Save the cleaned DataFrame to CSV.

    Args:
        df: Cleaned DataFrame to save.
        path: Destination CSV path.
    """
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def main() -> None:
    """Run the full nav_history cleaning workflow."""
    df = clean_nav_history()
    save_clean_data(df)


if __name__ == "__main__":
    main()