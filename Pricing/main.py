"""
Run a short PCA pipeline on bundled iPhone.csv (KNN imputation → scale → PCA).

From this folder:
  pip install -r requirements.txt
  python main.py
"""
from __future__ import annotations

import os
from pathlib import Path

# Non-interactive plots if analysis imports matplotlib later
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

_ROOT = Path(__file__).resolve().parent


def run_analysis(csv_name: str = "iPhone.csv") -> int:
    path = _ROOT / csv_name
    if not path.is_file():
        print(f"Missing data file: {path}")
        return 1

    df = pd.read_csv(path, index_col=0)
    numeric = df.apply(pd.to_numeric, errors="coerce")
    # Drop rows that are entirely NaN
    numeric = numeric.dropna(how="all")
    if numeric.shape[0] < 3 or numeric.shape[1] < 2:
        print("Not enough numeric data after load.")
        return 1

    imputer = KNNImputer(n_neighbors=min(5, numeric.shape[0] - 1))
    X = imputer.fit_transform(numeric)
    X = StandardScaler().fit_transform(X)

    pca = PCA()
    pca.fit(X)
    evr = pca.explained_variance_ratio_
    cum = np.cumsum(evr)

    print(f"Rows (after drop-all-NaN): {numeric.shape[0]}, features: {numeric.shape[1]}")
    print("Explained variance ratio (first 5 PCs):")
    for i in range(min(5, len(evr))):
        print(f"  PC{i + 1}: {evr[i]:.4f} (cumulative {cum[i]:.4f})")
    print(f"\nFull notebooks: Analysis.ipynb, PCA_assignment.ipynb")
    return 0


def main() -> int:
    return run_analysis()


if __name__ == "__main__":
    raise SystemExit(main())
