"""
BookKeep demo: load sample (or custom) journal + chart, validate double-entry, print reports.

Run from this directory:
  python main.py

Custom files:
  python main.py --journal path/to/journal.csv --chart path/to/chart_of_accounts.csv
"""
import sys

from ledger_report import run_cli


if __name__ == "__main__":
    raise SystemExit(run_cli())
