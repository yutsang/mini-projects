"""
Download a snapshot of the UN Security Council Consolidated List page (HTML).

The list is served as an HTML page (use browser “Print to PDF” for a PDF). Older
scripts that saved this URL as .pdf were incorrect. This saves the HTML for
archival/automation; use Part 2 notebooks/PDF tooling for extraction.

Usage (from repo root):
  python main.py
or:
  python download_sanction_list_from_internet_and_store_in_location.py
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import requests

CONSOLIDATED_URL = "https://scsanctions.un.org/consolidated/"
_APP_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_DIR = _APP_DIR / "downloads"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def download_consolidated_html(
    url: str = CONSOLIDATED_URL,
    out_dir: Optional[Path] = None,
    filename_prefix: str = "UN_consolidated_list",
) -> Path:
    out_dir = out_dir or DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{filename_prefix}_{date.today().isoformat()}.html"

    r = requests.get(url, headers=HEADERS, timeout=120)
    r.raise_for_status()
    text = r.text
    if len(text) < 500:
        raise RuntimeError("Response too short; site may have blocked the request.")

    dest.write_text(text, encoding="utf-8")
    return dest


def main() -> int:
    try:
        path = download_consolidated_html()
    except requests.RequestException as e:
        print(f"Download failed (network): {e}")
        return 1
    except OSError as e:
        print(f"Could not write file: {e}")
        return 1
    except RuntimeError as e:
        print(e)
        return 1
    print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
