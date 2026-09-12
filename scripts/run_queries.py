"""
run_queries.py

Runs each analytical query against bluestock_mf.db and prints the results.
"""

import sqlite3
import pandas as pd

DB_PATH = "../bluestock_mf.db"


def run_query(query: str, label: str) -> None:
    """Run a single SQL query and print its results.

    Args:
        query: The SQL query string to execute.
        label: A short description printed above the results.
    """
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql(query, conn)
    conn.close()
    print(f"\n--- {label} ---")
    print(result.to_string(index=False))

if __name__ == "__main__":
    query_1 = """
    SELECT f.scheme_name, f.fund_house, p.aum_crore
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
    ORDER BY p.aum_crore DESC
    LIMIT 5;
    """
    run_query(query_1, "Query 1: Top 5 Funds by AUM")
    query_2 = """
    SELECT strftime('%Y-%m', date) AS month, ROUND(AVG(nav), 2) AS avg_nav
    FROM fact_nav
    GROUP BY month
    ORDER BY month;
    """
    run_query(query_2, "Query 2: Average NAV per Month (all funds)")

    query_3 = """
    SELECT month, sip_inflow_crore, yoy_growth_pct
    FROM fact_sip
    WHERE yoy_growth_pct IS NOT NULL
    ORDER BY month;
    """
    run_query(query_3, "Query 3: SIP YoY Growth by Month")

    query_4 = """
    SELECT state, SUM(amount_inr) AS total_transaction_amount, COUNT(*) AS num_transactions
    FROM fact_transactions
    GROUP BY state
    ORDER BY total_transaction_amount DESC;
    """
    run_query(query_4, "Query 4: Transactions by State")

    query_5 = """
    SELECT scheme_name, fund_house, expense_ratio_pct
    FROM dim_fund
    WHERE expense_ratio_pct < 1.0
    ORDER BY expense_ratio_pct;
    """
    run_query(query_5, "Query 5: Funds with Expense Ratio < 1%")

    query_6 = """
    SELECT f.category, ROUND(AVG(p.sharpe_ratio), 3) AS avg_sharpe_ratio
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
    GROUP BY f.category
    ORDER BY avg_sharpe_ratio DESC;
    """
    run_query(query_6, "Query 6: Average Sharpe Ratio by Category")

    query_7 = """
    SELECT t.transaction_type, COUNT(*) AS num_transactions, SUM(t.amount_inr) AS total_amount
    FROM fact_transactions t
    GROUP BY t.transaction_type
    ORDER BY total_amount DESC;
    """
    run_query(query_7, "Query 7: Transaction Volume by Type (SIP/Lumpsum/Redemption)")

    query_8 = """
    SELECT city_tier, ROUND(AVG(amount_inr), 2) AS avg_transaction_amount, COUNT(*) AS num_transactions
    FROM fact_transactions
    GROUP BY city_tier
    ORDER BY avg_transaction_amount DESC;
    """
    run_query(query_8, "Query 8: Average Transaction Amount by City Tier")

    query_9 = """
    SELECT f.scheme_name, f.category, p.max_drawdown_pct
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
    ORDER BY p.max_drawdown_pct ASC
    LIMIT 5;
    """
    run_query(query_9, "Query 9: Top 5 Worst Maximum Drawdowns")

    query_10 = """
    SELECT age_group, transaction_type, COUNT(*) AS num_transactions
    FROM fact_transactions
    GROUP BY age_group, transaction_type
    ORDER BY age_group, num_transactions DESC;
    """
    run_query(query_10, "Query 10: Transaction Type Preference by Age Group")