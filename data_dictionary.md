# Data Dictionary — Bluestock Mutual Fund Analytics

This document describes every table and column in `bluestock_mf.db`, including data types, business definitions, and source references.

## dim_fund

Scheme-level metadata dimension table. One row per fund.

Source: `01_fund_master.csv`

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK) | Unique AMFI scheme code identifying the fund |
| fund_house | TEXT | Asset Management Company (AMC) managing the fund |
| scheme_name | TEXT | Full official name of the scheme |
| category | TEXT | Broad category: Equity or Debt |
| sub_category | TEXT | Specific sub-category (e.g. Large Cap, Small Cap, Gilt) |
| plan | TEXT | Plan type: Regular or Direct |
| launch_date | TEXT | Date the scheme was launched |
| benchmark | TEXT | Benchmark index the fund is measured against |
| expense_ratio_pct | REAL | Annual expense ratio as a percentage of AUM |
| exit_load_pct | REAL | Exit load percentage charged on early redemption |
| min_sip_amount | INTEGER | Minimum SIP investment amount in INR |
| min_lumpsum_amount | INTEGER | Minimum lumpsum investment amount in INR |
| fund_manager | TEXT | Name of the fund manager |
| risk_category | TEXT | Risk classification (Low, Moderate, High, Very High) |
| sebi_category_code | TEXT | SEBI-assigned category code |

## dim_date

Calendar dimension table with one row per day, used for time-based grouping and filtering.

Source: Generated programmatically (2022-01-01 to 2026-12-31)

| Column | Type | Description |
|---|---|---|
| date_key | TEXT (PK) | Date in YYYY-MM-DD format, used as the join key |
| full_date | TEXT | Full date, same format as date_key |
| year | INTEGER | Calendar year |
| month | INTEGER | Calendar month (1-12) |
| month_name | TEXT | Full month name (e.g. "January") |
| quarter | INTEGER | Calendar quarter (1-4) |
| day_of_week | TEXT | Day name (e.g. "Monday") |

## fact_nav

Daily NAV records for every scheme. One row per fund per trading day.

Source: `02_nav_history.csv`

| Column | Type | Description |
|---|---|---|
| nav_id | INTEGER (PK) | Auto-incrementing surrogate key |
| amfi_code | INTEGER (FK → dim_fund) | Fund this NAV record belongs to |
| date | TEXT | Date of the NAV observation |
| nav | REAL | Net Asset Value per unit on this date |

## fact_transactions

Individual investor transaction records.

Source: `08_investor_transactions.csv`

| Column | Type | Description |
|---|---|---|
| transaction_id | INTEGER (PK) | Auto-incrementing surrogate key |
| investor_id | TEXT | Unique identifier for the investor |
| transaction_date | TEXT | Date the transaction occurred |
| amfi_code | INTEGER (FK → dim_fund) | Fund the transaction relates to |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | INTEGER | Transaction amount in Indian Rupees |
| state | TEXT | Indian state of the investor |
| city | TEXT | City of the investor |
| city_tier | TEXT | T30 (top 30 cities) or B30 (beyond top 30) |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Investor's annual income in lakhs INR |
| payment_mode | TEXT | Payment method used (UPI, Cheque, Mandate, etc.) |
| kyc_status | TEXT | Verified or Pending |

## fact_performance

Pre-computed performance and risk metrics per scheme. One row per fund.

Source: `07_scheme_performance.csv`

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK, FK → dim_fund) | Fund this record describes |
| return_1yr_pct | REAL | 1-year trailing return (%) |
| return_3yr_pct | REAL | 3-year annualized return (%) |
| return_5yr_pct | REAL | 5-year annualized return (%) |
| benchmark_3yr_pct | REAL | Benchmark's 3-year annualized return (%) |
| alpha | REAL | Excess return vs benchmark, risk-adjusted |
| beta | REAL | Sensitivity of fund returns to benchmark movements |
| sharpe_ratio | REAL | Risk-adjusted return using total volatility |
| sortino_ratio | REAL | Risk-adjusted return using downside volatility only |
| std_dev_ann_pct | REAL | Annualized standard deviation of returns (%) |
| max_drawdown_pct | REAL | Maximum peak-to-trough decline (%) |
| aum_crore | INTEGER | Assets Under Management in INR crore |
| expense_ratio_pct | REAL | Annual expense ratio (%) |
| morningstar_rating | INTEGER | Star rating (1-5) |
| risk_grade | TEXT | Risk classification label |
| is_anomaly | BOOLEAN | Flagged True if any metric fell outside 3 standard deviations |

## fact_aum

Quarterly AUM figures by fund house.

Source: `03_aum_by_fund_house.csv`

| Column | Type | Description |
|---|---|---|
| aum_id | INTEGER (PK) | Auto-incrementing surrogate key |
| date | TEXT | Quarter-end reporting date |
| fund_house | TEXT | Asset Management Company |
| aum_lakh_crore | REAL | Total AUM in lakh crore INR |
| aum_crore | INTEGER | Total AUM in crore INR |
| num_schemes | INTEGER | Number of schemes offered by this fund house |

## fact_sip

Industry-wide monthly SIP inflow statistics.

Source: `04_monthly_sip_inflows.csv`

| Column | Type | Description |
|---|---|---|
| month | TEXT (PK) | Month in YYYY-MM format |
| sip_inflow_crore | INTEGER | Total SIP inflows for the month, in crore INR |
| active_sip_accounts_crore | REAL | Number