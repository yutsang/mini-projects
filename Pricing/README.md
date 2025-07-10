# iPhone Price Analysis & Machine Learning

A comprehensive data analysis project that performs price analysis on iPhone models using principal component analysis (PCA) and machine learning techniques.

## Project Overview

This project analyzes iPhone pricing data across multiple models and timeframes, applying dimensionality reduction and machine learning algorithms to understand price patterns and relationships between different iPhone models.

## Features

- **Data Preprocessing**: Missing value handling using listwise deletion and KNN imputation
- **Normalization**: Data standardization for consistent analysis
- **Principal Component Analysis (PCA)**: Dimensionality reduction and feature extraction
- **Correlation Analysis**: Cross-model price correlation over time
- **Machine Learning**: Linear regression modeling for price prediction
- **Visualization**: Data visualization using matplotlib and seaborn

## Dataset

The project analyzes pricing data for various iPhone models including:
- iPhone 8
- iPhone X
- iPhone XS
- iPhone 11
- iPhone 12
- iPhone 13

Data sources include:
- **Keepa**: Amazon price tracking data
- **Custom datasets**: Various iPhone pricing datasets in CSV and Excel formats

## Project Structure

```
Pricing/
├── Analysis.ipynb              # Main analysis notebook
├── PCA_assignment.ipynb        # PCA-specific assignment
├── data.ipynb                  # Data preprocessing notebook
├── keepa.ipynb                 # Keepa API integration
├── iPhone.csv                  # Main iPhone dataset
├── iPhone.xlsx                 # Excel format dataset
├── iPhone KNN 5 processed.csv  # KNN processed data
├── all_data.csv               # Combined dataset
├── correlation_matrix.csv      # Correlation analysis results
├── df_norm.csv                # Normalized dataset
├── Nov.xlsx                   # November data
├── Nov-origin.xlsx            # Original November data
└── README.md                  # This file
```

## Key Analysis Components

### 1. Data Preprocessing
- **Missing Value Treatment**: Listwise deletion and KNN imputation
- **Data Normalization**: Standardization using sklearn preprocessing
- **Feature Engineering**: Time-based feature extraction

### 2. Principal Component Analysis
- **Variance Analysis**: Eigenvalues and eigenvectors computation
- **Dimensionality Reduction**: Optimal component selection
- **Cumulative Variance**: Variance preservation analysis

### 3. Machine Learning Models
- **Linear Regression**: Price prediction modeling
- **Cross-Validation**: Model performance evaluation
- **Feature Selection**: Optimal feature subset identification

### 4. Correlation Analysis
- **Cross-Model Correlation**: Price relationship between iPhone models
- **Time Series Analysis**: Price trend analysis over time
- **Market Insights**: Price pattern identification

## Requirements

```python
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
openpyxl>=3.0.0
missingno>=0.5.0
```

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Open Jupyter notebooks to run the analysis

## Usage

### Main Analysis
```python
# Load and run the main analysis
jupyter notebook Analysis.ipynb
```

### PCA Assignment
```python
# Run PCA-specific analysis
jupyter notebook PCA_assignment.ipynb
```

### Data Processing
```python
# Process and clean data
jupyter notebook data.ipynb
```

## Key Findings

1. **High Correlation**: iPhone models show strong price correlations (0.86-0.93)
2. **PCA Insights**: First principal component captures 91-96% of variance
3. **Price Patterns**: Consistent pricing relationships across models
4. **Temporal Trends**: Price stability with seasonal variations

## Machine Learning Results

- **Linear Regression**: Successfully predicts price trends
- **Cross-Validation**: Robust model performance across folds
- **Feature Importance**: Day and model features show high predictive power

## Data Sources

- **Keepa API**: Real-time Amazon price tracking
- **Manual Collection**: Historical pricing data
- **Public Datasets**: iPhone specifications and market data

## Language & Tools

- **Primary Language**: Python
- **Libraries**: pandas, numpy, scikit-learn, matplotlib, seaborn
- **Environment**: Jupyter Notebook
- **Data Formats**: CSV, Excel, JSON

## Future Enhancements

- [ ] Add more iPhone models (iPhone 14, 15)
- [ ] Implement time series forecasting
- [ ] Add market sentiment analysis
- [ ] Create interactive visualizations
- [ ] Deploy as web application

## License

This project is for educational and research purposes. 