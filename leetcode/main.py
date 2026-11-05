"""
LeetCode mini-repo entrypoint.

  python main.py              # offline stats from leetcode_submissions.csv
  python main.py sync         # run Selenium scraper (needs config.cfg + Chrome)
  python main.py update-problems  # refresh leetcode_problems.csv via API script
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def cmd_stats() -> int:
    import csv

    sub_path = _ROOT / "leetcode_submissions.csv"
    prob_path = _ROOT / "leetcode_problems.csv"
    if not sub_path.is_file():
        print(
            "Missing leetcode_submissions.csv.\n"
            "  • Run `python main.py sync` after adding config.cfg (Chrome + GitHub login), or\n"
            "  • Add your own CSV with columns matching the scraper output."
        )
        return 1
    with open(sub_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    accepted = sum(1 for r in rows if r.get("Status") == "Accepted") if rows else 0
    print(f"Submissions rows: {n} (Accepted: {accepted})")
    if prob_path.is_file():
        with open(prob_path, newline="", encoding="utf-8") as f:
            prob_n = sum(1 for _ in csv.DictReader(f))
        print(f"leetcode_problems.csv rows: {prob_n}")
    else:
        print("No leetcode_problems.csv — run: python main.py update-problems")
    return 0


def cmd_sync() -> int:
    cfg = _ROOT / "config.cfg"
    if not cfg.is_file():
        print(
            f"Missing {_ROOT / 'config.cfg'}.\n"
            "Copy config_sample.cfg to config.cfg and set GitHub + LeetCode login fields."
        )
        return 1
    prob = _ROOT / "leetcode_problems.csv"
    if not prob.is_file():
        print("Missing leetcode_problems.csv — run first: python main.py update-problems")
        return 1
    os.chdir(_ROOT)
    import autoleetcode

    autoleetcode.main()
    return 0


def cmd_update_problems() -> int:
    script = _ROOT / "leetcode_problems.py"
    r = subprocess.run([sys.executable, str(script)], cwd=str(_ROOT))
    return int(r.returncode or 0)


def main() -> int:
    p = argparse.ArgumentParser(description="LeetCode automation helpers")
    p.add_argument(
        "command",
        nargs="?",
        default="stats",
        choices=["stats", "sync", "update-problems"],
        help="stats (default): summarize CSVs; sync: Selenium scraper; update-problems: fetch problem list",
    )
    args = p.parse_args()
    if args.command == "stats":
        return cmd_stats()
    if args.command == "sync":
        return cmd_sync()
    return cmd_update_problems()


if __name__ == "__main__":
    raise SystemExit(main())
