"""
KYC/AML helper — Part 1: download UN consolidated list HTML snapshot.

  cd side-sanction-list-checking
  pip install -r requirements.txt
  python main.py

PDF parsing and fuzzy matching live in the Part_2-3 folder / notebooks.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PART1 = _ROOT / "Part_1_Download_Sanction_List_from_the_Internet"


def main() -> int:
    sys.path.insert(0, str(_PART1))
    import download_sanction_list_from_internet_and_store_in_location as dl

    return dl.main()


if __name__ == "__main__":
    raise SystemExit(main())
