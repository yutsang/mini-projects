# Stock Ticking Algorithm & Inventory Optimization

A data-driven inventory management system that optimizes stock allocation using correlation analysis and algorithmic approaches for efficient order fulfillment.

## Project Overview

This project implements a stock ticking algorithm that analyzes order patterns, builds product correlation matrices, and optimizes inventory allocation across multiple storage racks. The system uses machine learning techniques to predict optimal stock placement and improve order fulfillment efficiency.

## Features

- **Order Processing**: Aggregates and processes order data with SKU-quantity mapping
- **Correlation Analysis**: Builds product correlation matrices based on order patterns
- **Rack Simulation**: Simulates multiple storage racks for inventory optimization
- **Algorithmic Optimization**: Uses correlation-based algorithms for stock placement
- **Performance Metrics**: Tracks fulfillment efficiency and optimization results
- **Data Visualization**: Provides insights through correlation matrices and performance charts

## Business Problem

The project addresses key inventory management challenges:
- **Efficient Stock Placement**: Optimize where to place products in storage
- **Order Fulfillment Speed**: Reduce time to fulfill orders by strategic placement
- **Inventory Correlation**: Leverage products that are frequently ordered together
- **Storage Optimization**: Maximize storage efficiency across multiple racks

## Project Structure

```
Stock Ticking/
├── stock-tick-algo.ipynb       # Main algorithm implementation
├── keepa.ipynb                 # Keepa API integration for pricing
├── Nov.xlsx                    # November order data
├── Nov-origin.xlsx             # Original November dataset
├── corr.csv                    # Correlation analysis results
├── correlation_matrix.csv      # Product correlation matrix
├── df_norm.csv                 # Normalized dataset
└── README.md                   # This file
```

## Algorithm Components

### 1. Order Data Processing
```python
# Aggregate orders by SKU and quantity
order_merged = pd.DataFrame(columns=['Ext Orderno', 'sku_qty', 'Status'])
```

### 2. Correlation Matrix Building
```python
# Build correlation matrix based on order patterns
size = len(product)
corr = [[0 for x in range(size)] for y in range(size)]
```

### 3. Rack Simulation
```python
# Simulate storage racks for optimization
rack_All = pd.DataFrame(index=range(500), columns=["Ext Orderno", "totalQty"])
```

### 4. Optimization Algorithm
- **Correlation-based Placement**: Products with high correlation are placed strategically
- **Frequency Analysis**: High-frequency products get priority placement
- **Distance Optimization**: Minimize travel time between correlated products

## Key Features

### Data Processing
- **Order Aggregation**: Combines multiple order lines into single order records
- **SKU Mapping**: Maps product codes to quantities and names
- **Status Tracking**: Monitors order fulfillment status

### Correlation Analysis
- **Co-occurrence Matrix**: Tracks which products are ordered together
- **Correlation Scoring**: Quantifies product relationships
- **Pattern Recognition**: Identifies frequently co-ordered product pairs

### Inventory Optimization
- **Rack Allocation**: Distributes inventory across multiple storage locations
- **Strategic Placement**: Places correlated products in proximity
- **Capacity Management**: Optimizes storage capacity utilization

## Requirements

```python
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
openpyxl>=3.0.0
keepa>=1.3.0  # For price tracking integration
```

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Open Jupyter notebooks to run the analysis

## Usage

### Main Algorithm
```python
# Run the stock ticking algorithm
jupyter notebook stock-tick-algo.ipynb
```

### Price Integration
```python
# Integrate with Keepa for price data
jupyter notebook keepa.ipynb
```

## Algorithm Workflow

1. **Data Loading**: Load order data from Excel files
2. **Order Processing**: Aggregate orders by SKU and quantity
3. **Correlation Building**: Create product correlation matrix
4. **Optimization**: Apply correlation-based placement algorithm
5. **Rack Simulation**: Simulate inventory placement across racks
6. **Performance Evaluation**: Measure optimization effectiveness

## Key Metrics

- **Correlation Strength**: Measures product co-occurrence patterns
- **Fulfillment Efficiency**: Time to complete orders
- **Storage Utilization**: Percentage of storage capacity used
- **Travel Distance**: Distance between correlated products

## Data Sources

- **Order Data**: Excel files with order details and SKU information
- **Product Catalog**: SKU codes and product names
- **Keepa API**: Real-time pricing data for additional analysis

## Technical Implementation

### Data Structures
- **Order DataFrame**: Structured order data with SKU quantities
- **Correlation Matrix**: 2D array representing product relationships
- **Rack Simulation**: DataFrame representing storage locations

### Algorithms
- **Correlation Calculation**: Frequency-based correlation scoring
- **Optimization**: Greedy algorithm for rack placement
- **Performance Metrics**: Efficiency calculation algorithms

## Current Status

⚠️ **Note**: The project contains deprecated pandas methods (`.append()`) that should be updated to use `pd.concat()` for better performance and future compatibility.

## Future Enhancements

- [ ] Update deprecated pandas methods
- [ ] Add real-time inventory tracking
- [ ] Implement machine learning for demand forecasting
- [ ] Add interactive dashboard for monitoring
- [ ] Integrate with warehouse management systems
- [ ] Add multi-warehouse support
- [ ] Implement A/B testing for optimization strategies

## Language & Tools

- **Primary Language**: Python
- **Libraries**: pandas, numpy, matplotlib, seaborn
- **Environment**: Jupyter Notebook
- **Data Formats**: Excel, CSV
- **APIs**: Keepa (for pricing data)

## Performance Considerations

- **Scalability**: Handles large datasets with efficient algorithms
- **Memory Management**: Optimized data structures for large correlation matrices
- **Processing Speed**: Vectorized operations for faster computation

## License

This project is for educational and research purposes in inventory management and operations research. 