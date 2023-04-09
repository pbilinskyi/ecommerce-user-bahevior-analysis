# User Activity Analysis

## Introduction

### Plan

1. **Data preparation and EDA**
    1. Upload data to DuckDB for storage.
    2. Handle missing values.
    3. Remove anomalies.

2. **Describe user behavior**.
    1. User Funnel with conversions.
    2. User Retention and cohorts.
    3. User LTV.

4. **User Segmentation**. Come up with different user features, which can be used for further analysis.
    1. Behavioral segmentation.
    2. Segmentation by purchase.
    3. Other.

5. **Insights searching**. Find the potential _customer problems_. First of all, chose metric for measuring user success. Then compare segments of users by success metrics and find weak segments, or compare to some benchmark of the industry.

### Tech stack

- Python libraries:
    - Data Wrangling: `numpy`, `pandas`
    - Data Visualization: `seaborn`
    - `lifelines` used to find key factors, that influence User Retention
    - `pip-tools` for human-readable pinning of dependencies.
- Jupyter Notebook for interactive analysis.
    -  [JupySQL](https://github.com/ploomber/jupysql) plugin for SQL queries
- [DuckDB](https://duckdb.org/) - for data storage and fast analytical computations.

