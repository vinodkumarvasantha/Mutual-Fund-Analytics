"""
run_pipeline.py

Master execution script for the Bluestock Mutual Fund Analytics capstone.
Runs the full pipeline end-to-end.
"""

import argparse
import sys

import data_inspection
import fetch_live_nav


def main() -> None:
    """Parse CLI args and run each pipeline stage in order."""
    parser = argparse.ArgumentParser(description="Run the Bluestock MF Analytics pipeline.")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip the live NAV fetch step.")
    args = parser.parse_args()

    print("STEP 1: DATA INSPECTION & QUALITY CHECKS")
    try:
        data_inspection.main()
    except FileNotFoundError as exc:
        print(f"Data inspection failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.skip_fetch:
        print("STEP 2: LIVE NAV FETCH")
        try:
            fetch_live_nav.main()
        except Exception as exc:
            print(f"Live NAV fetch failed (continuing anyway): {exc}", file=sys.stderr)
    else:
        print("Skipping live NAV fetch.")

    print("STEP 3: PERFORMANCE ANALYTICS")
    print("Run Performance_Analytics.ipynb to compute the full analysis.")
    print("Pipeline complete.")


if __name__ == "__main__":
    main()