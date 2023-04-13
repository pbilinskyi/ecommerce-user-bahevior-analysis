# User Activity Analysis

Requirements: [requirements.in](requirements.in)

## How to set up the data

Run the following scripts:
```
python upload_data.py
python missing_values_imputation.py
python anomaly_removal.py
python create_additional_tables.py
```

It will upload data to the local DuckDB database, which will be created automatically. It will also clean the data and create some additional tables for the analysis.

## Analysis

### Plan

1. **Data preparation and EDA**
    - [x] Upload data to DuckDB for storage.
    - [x] Handle missing values.
    - [x] Remove anomalies.

2. **[WIP ]Describe user behavior**.
    - [x] User Funnel with conversions.
    - [x] User Retention and cohorts.
    - [ ] User LTV.

4. **[WIP] User Segmentation**. Come up with different user features, which can be used for further analysis.
    - [ ] Behavioral segmentation.
    - [x] Segmentation by purchase.


5. **[WIP] Insights searching**. Find the potential _customer problems_. First of all, chose metric for measuring user success. Then compare segments of users by success metrics and find weak segments, or compare to some benchmark of the industry.
### Tech stack

- Python libraries:
    - Data Wrangling: `numpy`, `pandas`
    - Data Visualization: `seaborn`, `plotly`
    - `pip-tools` for human-readable pinning of dependencies.
- Jupyter Notebook for interactive analysis.
    -  [JupySQL](https://github.com/ploomber/jupysql) plugin for SQL queries
- [DuckDB](https://duckdb.org/) - for data storage and fast analytical computations.

