"""
recommender.py

Simple fund recommender: given a risk appetite (Low/Moderate/High),
returns the top 3 funds by Sharpe Ratio within the matching risk grade(s).

Usage:
    python recommender.py
    (then enter Low, Moderate, or High when prompted)
"""

import pandas as pd

DATA_DIR = "../data/raw"

RISK_MAPPING = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"],
}


def load_data() -> pd.DataFrame:
    """Load and merge fund master and scheme performance data.

    Returns:
        Merged DataFrame with scheme_name, fund_house, risk_grade, and sharpe_ratio.
    """
    fund_master = pd.read_csv(f"{DATA_DIR}/01_fund_master.csv")
    performance = pd.read_csv(f"{DATA_DIR}/07_scheme_performance.csv")
    merged = performance.merge(fund_master[["amfi_code", "fund_house"]], on="amfi_code", suffixes=("", "_dup"))
    return merged


def recommend_funds(risk_appetite: str, df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Return the top N funds by Sharpe Ratio matching the given risk appetite.

    Args:
        risk_appetite: One of "Low", "Moderate", "High".
        df: Merged fund/performance DataFrame.
        top_n: Number of funds to return.

    Returns:
        DataFrame with the top N matching funds, sorted by Sharpe Ratio descending.
    """
    if risk_appetite not in RISK_MAPPING:
        raise ValueError(f"risk_appetite must be one of {list(RISK_MAPPING.keys())}")

    matching_grades = RISK_MAPPING[risk_appetite]
    matches = df[df["risk_grade"].isin(matching_grades)]
    top_matches = matches.sort_values("sharpe_ratio", ascending=False).head(top_n)
    return top_matches[["scheme_name", "fund_house", "risk_grade", "sharpe_ratio", "return_3yr_pct", "expense_ratio_pct"]]


def main() -> None:
    """Prompt the user for risk appetite and print a recommendation table."""
    df = load_data()
    risk_appetite = input("Enter your risk appetite (Low / Moderate / High): ").strip().capitalize()

    try:
        recommendations = recommend_funds(risk_appetite, df)
        print(f"\nTop {len(recommendations)} funds for '{risk_appetite}' risk appetite:\n")
        print(recommendations.to_string(index=False))
    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()