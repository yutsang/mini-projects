"""
Inventory co-occurrence demo (same idea as stock-tick-algo.ipynb).

  python main.py              # built-in tiny order table
  python main.py --excel Nov.xlsx   # real workbook if you add it

Requires: pandas, openpyxl (for .xlsx)
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parent


def _demo_orders() -> pd.DataFrame:
    """Small synthetic order lines (Ext Orderno, Skucode, totalQty)."""
    return pd.DataFrame(
        {
            "Ext Orderno": [1001, 1001, 1001, 1002, 1002, 1003, 1003, 1003, 1004, 1004],
            "Skucode": [10, 11, 12, 10, 12, 11, 12, 13, 10, 13],
            "totalQty": [1, 2, 1, 1, 2, 1, 1, 3, 2, 1],
        }
    )


def load_orders(excel_path: Path | None) -> pd.DataFrame:
    if excel_path is None:
        return _demo_orders()
    if not excel_path.is_file():
        raise FileNotFoundError(excel_path)
    data = pd.read_excel(excel_path).sort_values(by=["Ext Orderno"]).reset_index(drop=True)
    data["Ext Orderno"] = data["Ext Orderno"].astype(int)
    data["Skucode"] = data["Skucode"].astype(int)
    data["totalQty"] = data["totalQty"].astype(int)
    return data[["Ext Orderno", "Skucode", "totalQty"]]


def cooccurrence_pairs(order: pd.DataFrame) -> pd.DataFrame:
    """Count unordered SKU pairs that appear in the same order."""
    counts: dict[tuple[int, int], int] = defaultdict(int)
    for _, g in order.groupby("Ext Orderno"):
        skus = sorted(g["Skucode"].unique().tolist())
        for a, b in combinations(skus, 2):
            counts[(a, b)] += 1
    if not counts:
        return pd.DataFrame(columns=["sku_a", "sku_b", "co_orders"])
    rows = [(a, b, c) for (a, b), c in sorted(counts.items(), key=lambda x: -x[1])]
    return pd.DataFrame(rows, columns=["sku_a", "sku_b", "co_orders"])


def main() -> int:
    p = argparse.ArgumentParser(description="SKU co-occurrence from order lines")
    p.add_argument(
        "--excel",
        type=Path,
        default=None,
        help="Path to Nov.xlsx-style file (columns Ext Orderno, Skucode, totalQty)",
    )
    args = p.parse_args()
    try:
        path = args.excel
        if path is not None and not path.is_absolute():
            path = _ROOT / path
        order = load_orders(path)
    except FileNotFoundError as e:
        print(f"{e}\nPlace Nov.xlsx in this folder or pass --excel path.")
        return 1
    except Exception as e:
        print(f"Failed to load orders: {e}")
        return 1

    pairs = cooccurrence_pairs(order)
    out = _ROOT / "cooccurrence_demo.csv"
    pairs.to_csv(out, index=False)

    print(f"Order lines: {len(order)}, unique orders: {order['Ext Orderno'].nunique()}")
    print("Top co-occurring SKU pairs:")
    print(pairs.head(10).to_string(index=False))
    print(f"\nWrote {out}")
    print("Full workflow: stock-tick-algo.ipynb")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
