"""
clean_investor_transactions.py

Cleans 08_investor_transactions.csv:
- Standardises transaction_type values (SIP/Lumpsum/Redemption)
- Validates amount_inr > 0
- Parses transaction_date to datetime
- Checks kyc_status against expected enum values
"""

import pandas as pd

RAW_PATH = "../data/raw/08_investor_transactions.csv"
OUTPUT_PATH = "../data/processed/08_investor_transactions_clean.csv"

VALID_TRANSACTION_TYPES = {"SIP", "Lumpsum", "Redemption"}
VALID_KYC_STATUSES = {"Verified", "Pending"}

def clean_investor_transactions(path: str = RAW_PATH) -> pd.DataFrame:
    """Load and clean the investor transactions dataset.

    Args:
        path: Path to the raw investor_transactions CSV.

    Returns:
        A cleaned DataFrame with validated transaction types, positive
        amounts, parsed dates, and validated KYC status values.
    """
    df = pd.read_csv(path)

    # Parse transaction_date to proper datetime type
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Standardise transaction_type: trim whitespace, fix casing
    df["transaction_type"] = df["transaction_type"].str.strip().str.capitalize()
    df["transaction_type"] = df["transaction_type"].replace({"Sip": "SIP"})

    invalid_types = df[~df["transaction_type"].isin(VALID_TRANSACTION_TYPES)]
    if len(invalid_types) > 0:
        print(f"WARNING: {len(invalid_types)} rows have unexpected transaction_type values")
    else:
        print("All transaction_type values are valid")

    # Validate amount_inr is positive
    invalid_amounts = df[df["amount_inr"] <= 0]
    if len(invalid_amounts) > 0:
        print(f"WARNING: {len(invalid_amounts)} rows have amount_inr <= 0")
    else:
        print("All amount_inr values are positive")

    # Check kyc_status against expected enum values
    invalid_kyc = df[~df["kyc_status"].isin(VALID_KYC_STATUSES)]
    if len(invalid_kyc) > 0:
        print(f"WARNING: {len(invalid_kyc)} rows have unexpected kyc_status values: {invalid_kyc['kyc_status'].unique()}")
    else:
        print("All kyc_status values are valid")

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
    """Run the full investor_transactions cleaning workflow."""
    df = clean_investor_transactions()
    save_clean_data(df)


if __name__ == "__main__":
    main()