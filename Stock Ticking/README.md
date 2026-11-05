# Stock ticking — co-occurrence / inventory ideas

Notebooks (`stock-tick-algo.ipynb`) walk through order aggregation, correlation-style co-occurrence, and rack-style simulations using Excel order data (`Nov.xlsx` when available).

## Quick run (CLI demo)

```bash
cd "Stock Ticking"
pip install -r requirements.txt
python main.py
```

Uses a **built-in tiny order table**, counts how often SKU pairs appear in the same order, prints the top pairs, and writes `cooccurrence_demo.csv`.

With your own workbook (columns `Ext Orderno`, `Skucode`, `totalQty`):

```bash
python main.py --excel Nov.xlsx
```

## Notebooks

- `stock-tick-algo.ipynb` — main pipeline  
- `keepa.ipynb` — Keepa / pricing (optional API key)

## Requirements

`pandas`, `numpy`, `openpyxl`, `matplotlib`, `seaborn`, `scipy`; `keepa` only if you use the Keepa notebook.

## License

Educational and research use.
