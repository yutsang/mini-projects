# iPhone price analysis (PCA & ML)

Notebooks analyze iPhone model prices (Keepa / CSV data): KNN imputation, scaling, PCA, correlation, and regression.

## Quick run (no Jupyter)

```bash
cd Pricing
pip install -r requirements.txt
python main.py
```

Loads `iPhone.csv`, applies KNN imputation (5 neighbors), standardizes, fits PCA, and prints explained variance for the first principal components.

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `Analysis.ipynb` | Main analysis |
| `PCA_assignment.ipynb` | PCA focus |
| `data.ipynb` | Data prep |

```bash
jupyter notebook Analysis.ipynb
```

## Data

Bundled CSVs include `iPhone.csv` (wide format: rows = observations, columns = model prices). Other CSVs in the folder are intermediate/assignment outputs.

## Requirements

See `requirements.txt` (pandas, scikit-learn, matplotlib, seaborn, openpyxl, jupyter, …).

## License

Educational and research use.
