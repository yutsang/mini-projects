# BookKeep — ledger CSV demo

A small Python demo that reads a **chart of accounts** and **journal** from CSV, checks that each transaction (`ref`) is balanced (debits = credits), then prints a **trial balance**, a simple **income statement**, and a **balance sheet** check (assets vs liabilities + equity including net income).

This is an educational starter, not a full accounting system.

## Requirements

- Python 3.10+ recommended

## Setup

```bash
cd bookkeep
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Uses default files under `data/`:

- `data/chart_of_accounts.csv`
- `data/sample_journal.csv`

### Custom CSV paths

```bash
python main.py --chart path/to/chart_of_accounts.csv --journal path/to/journal.csv
```

## CSV formats

### Chart of accounts

| Column | Description |
|--------|-------------|
| `account_code` | Account id (string, e.g. `1000`) |
| `account_name` | Display name |
| `account_type` | One of: `asset`, `liability`, `equity`, `revenue`, `expense` |

### Journal

| Column | Description |
|--------|-------------|
| `date` | Transaction date (informational) |
| `ref` | Transaction id; lines sharing the same `ref` must sum to equal debits and credits |
| `account_code` | Must exist in chart of accounts |
| `debit` | Debit amount (use `0` if none) |
| `credit` | Credit amount (use `0` if none) |
| `memo` | Description |

Rules:

- Each row must have **either** debit **or** credit nonzero (not both, not neither).
- For each `ref`, total debits must equal total credits.

## Project layout

```
bookkeep/
├── main.py                 # Entry: python main.py
├── ledger_report.py        # Load, validate, report
├── requirements.txt
├── data/
│   ├── chart_of_accounts.csv
│   └── sample_journal.csv
├── LICENSE
└── README.md
```

## Roadmap (ideas)

- Period filters, CSV/PDF export, and richer statements  
- Optional SQLite storage and a small web UI  

## Disclaimer

Educational use only. For production accounting, use qualified professionals and proper systems.

## License

See [LICENSE](LICENSE).
