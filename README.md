# Bluestock Mutual Fund Analytics

A capstone project analyzing 40 Indian mutual fund schemes using Python for data engineering and performance analytics, and Power BI for interactive dashboarding.

## Overview

This project builds an end-to-end pipeline covering data ingestion and quality checks, live NAV fetching from the mfapi.in API, statistical performance analysis (Sharpe/Sortino ratios, Alpha/Beta, CAGR, drawdown), a composite fund scorecard, and a 4-page interactive Power BI dashboard.

## Setup Instructions

1. Install Python 3.8 or newer.
2. Install required libraries:
3. Clone or download this repository.
4. Place the 10 raw CSV files into `data/raw/`.

## How to Run the ETL Pipeline

From the `scripts/` folder, run:

```
python run_pipeline.py
```

This will:
1. Load all 10 raw CSVs and check for nulls, duplicates, and AMFI code consistency between fund_master and nav_history.
2. Fetch live NAV data for 5 sample schemes from the mfapi.in API.
3. Prompt you to run the full analytics notebook for performance calculations.

To skip the live API fetch (e.g. if offline):
```
python run_pipeline.py --skip-fetch
```
## How to Run the Performance Analytics

Open and run `Performance_Analytics.ipynb` in Jupyter:

```
python -m notebook
```

Then open the notebook and select **Run → Run All Cells**. This computes daily returns, CAGR (1/3/5yr), Sharpe Ratio, Sortino Ratio, Alpha/Beta vs Nifty 100, Maximum Drawdown, and the composite Fund Scorecard, and generates the benchmark comparison chart. Outputs are saved to `outputs/`.

## How to Open the Dashboard

1. Install Power BI Desktop (free, via Microsoft Store).
2. Open `bluestock_mf_dashboard.pbix` in Power BI Desktop.
3. If prompted about data sources, point it to your local `data/raw/` folder.
4. The dashboard has 4 pages: Industry Overview, Fund Performance, Investor Analytics, and SIP & Market Trends.

## Dataset Descriptions

| File | Description |
|---|---|
| `01_fund_master.csv` | Scheme metadata: AMFI code, name, category, fund house, expense ratio, benchmark |
| `02_nav_history.csv` | Daily NAV records for all 40 schemes, 2022–2026 |
| `03_aum_by_fund_house.csv` | Quarterly AUM and scheme counts by AMC |
| `04_monthly_sip_inflows.csv` | Industry-wide monthly SIP inflow figures |
| `05_category_inflows.csv` | Monthly net inflows by fund category |
| `06_industry_folio_count.csv` | Monthly investor folio counts by category |
| `07_scheme_performance.csv` | Pre-computed return, risk, and rating metrics per scheme |
| `08_investor_transactions.csv` | 32,778 individual transaction records with investor demographics |
| `09_portfolio_holdings.csv` | Fund portfolio composition snapshots |
| `10_benchmark_indices.csv` | Daily closing values for 7 market indices |

## Project Structure

```
mutual-fund-analytics/
├── data/raw/                      # 10 raw CSV files
├── scripts/                       # Cleaned Python ETL scripts
├── outputs/                       # Generated CSVs and charts
├── Performance_Analytics.ipynb    # Main analytics notebook
├── bluestock_mf_dashboard.pbix    # Power BI dashboard
├── Final_Report.pdf               # Full capstone report
├── Bluestock_MF_Presentation.pptx # 12-slide summary deck
└── README.md
```