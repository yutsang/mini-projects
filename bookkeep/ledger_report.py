"""
Load chart of accounts + journal CSVs, validate double-entry, print trial balance and simple statements.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

_APP_DIR = Path(__file__).resolve().parent
DATA_DIR = _APP_DIR / "data"

DEBIT_NORMAL = {"asset", "expense"}
CREDIT_NORMAL = {"liability", "equity", "revenue"}


def load_chart(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"account_code": str})
    df["account_code"] = df["account_code"].str.strip()
    df["account_type"] = df["account_type"].str.strip().str.lower()
    invalid = set(df["account_type"]) - DEBIT_NORMAL - CREDIT_NORMAL
    if invalid:
        raise ValueError(f"Unknown account_type values: {invalid}")
    return df


def load_journal(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"account_code": str, "ref": str})
    df["account_code"] = df["account_code"].str.strip()
    for col in ("debit", "credit"):
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df


def validate_double_entry(journal: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    for ref, g in journal.groupby("ref", sort=False):
        d, c = float(g["debit"].sum()), float(g["credit"].sum())
        if round(d - c, 2) != 0:
            errors.append(f"ref '{ref}': debits {d:.2f} != credits {c:.2f}")
    codes_ok = (journal["debit"] >= 0).all() and (journal["credit"] >= 0).all()
    if not codes_ok:
        errors.append("Negative debit or credit amounts are not allowed.")
    both = (journal["debit"] > 0) & (journal["credit"] > 0)
    if both.any():
        errors.append("Rows with both debit and credit set are not supported.")
    neither = (journal["debit"] == 0) & (journal["credit"] == 0)
    if neither.any():
        errors.append("Each row must have either debit or credit (not both zero).")
    return errors


def merge_chart_journal(chart: pd.DataFrame, journal: pd.DataFrame) -> pd.DataFrame:
    merged = journal.merge(chart, on="account_code", how="left")
    missing = merged[merged["account_name"].isna()]["account_code"].unique().tolist()
    if missing:
        raise ValueError(f"Journal references unknown account_code(s): {missing}")
    return merged


def posting_totals(merged: pd.DataFrame) -> pd.DataFrame:
    g = merged.groupby(["account_code", "account_name", "account_type"], as_index=False).agg(
        total_debit=("debit", "sum"),
        total_credit=("credit", "sum"),
    )
    return g


def signed_balance(row: pd.Series) -> float:
    t = row["account_type"]
    deb, cred = row["total_debit"], row["total_credit"]
    if t in DEBIT_NORMAL:
        return deb - cred
    return cred - deb


def trial_balance(postings: pd.DataFrame) -> pd.DataFrame:
    tb = postings.copy()
    tb["balance"] = tb.apply(signed_balance, axis=1)
    return tb


def income_statement(tb: pd.DataFrame) -> Tuple[float, float, float]:
    rev = tb.loc[tb["account_type"] == "revenue", "balance"].sum()
    exp = tb.loc[tb["account_type"] == "expense", "balance"].sum()
    # revenue has credit normal -> positive balance means revenue; expense positive means expense
    net = rev - exp
    return float(rev), float(exp), float(net)


def balance_sheet(tb: pd.DataFrame, net_income: float) -> dict[str, float]:
    assets = tb.loc[tb["account_type"] == "asset", "balance"].sum()
    liabilities = tb.loc[tb["account_type"] == "liability", "balance"].sum()
    equity = tb.loc[tb["account_type"] == "equity", "balance"].sum()
    equity_incl = equity + net_income
    return {
        "assets": float(assets),
        "liabilities": float(liabilities),
        "equity": float(equity),
        "equity_including_net_income": float(equity_incl),
        "net_income": float(net_income),
    }


def format_money(x: float) -> str:
    return f"{x:,.2f}"


def run_report(
    chart_path: Path | None = None,
    journal_path: Path | None = None,
) -> int:
    chart_path = chart_path or DATA_DIR / "chart_of_accounts.csv"
    journal_path = journal_path or DATA_DIR / "sample_journal.csv"

    if not chart_path.is_file():
        print(f"Missing chart of accounts: {chart_path}", flush=True)
        return 1
    if not journal_path.is_file():
        print(f"Missing journal file: {journal_path}", flush=True)
        return 1

    chart = load_chart(chart_path)
    journal = load_journal(journal_path)

    errs = validate_double_entry(journal)
    if errs:
        print("Journal validation failed:", flush=True)
        for e in errs:
            print(f"  - {e}", flush=True)
        return 1

    merged = merge_chart_journal(chart, journal)
    postings = posting_totals(merged)
    tb = trial_balance(postings)

    print("Trial balance (normal balances)", flush=True)
    print(tb.to_string(index=False, formatters={"total_debit": format_money, "total_credit": format_money, "balance": format_money}), flush=True)

    rev, exp, net = income_statement(tb)
    print("\nIncome statement (simple)", flush=True)
    print(f"  Revenue:   {format_money(rev)}", flush=True)
    print(f"  Expenses:  {format_money(exp)}", flush=True)
    print(f"  Net income:{format_money(net)}", flush=True)

    bs = balance_sheet(tb, net)
    print("\nBalance sheet (equity includes current net income)", flush=True)
    print(f"  Assets:                  {format_money(bs['assets'])}", flush=True)
    print(f"  Liabilities:             {format_money(bs['liabilities'])}", flush=True)
    print(f"  Equity (contributions):{format_money(bs['equity'])}", flush=True)
    print(f"  Equity + net income:    {format_money(bs['equity_including_net_income'])}", flush=True)
    print(f"  Liabilities + equity:   {format_money(bs['liabilities'] + bs['equity_including_net_income'])}", flush=True)

    check = abs(bs["assets"] - (bs["liabilities"] + bs["equity_including_net_income"]))
    if check > 0.02:
        print(f"\nWarning: accounting equation off by {check:.2f} (rounding or period logic).", flush=True)
        return 0
    print("\nAccounting equation: Assets = Liabilities + Equity (OK)", flush=True)
    return 0


def run_cli(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="BookKeep: ledger CSV → trial balance & statements")
    p.add_argument("--chart", type=Path, help="Chart of accounts CSV")
    p.add_argument("--journal", type=Path, help="Journal CSV")
    args = p.parse_args(argv)
    return run_report(chart_path=args.chart, journal_path=args.journal)
