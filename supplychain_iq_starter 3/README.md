# SupplyChain IQ — Starter Project

## Goal
Build a portfolio project demonstrating supply-chain analytics with Python, SQL, data quality checks, dashboards, and a simple demand forecast.

## Dataset
All files in `data/raw/` are synthetic, generated for practice. They are not Philips data and do not represent a real company.

- `orders.csv`: 2,200 order records, dates, products, suppliers, quantities, prices, and delivery dates.
- `products.csv`: product categories, unit costs, and reorder levels.
- `suppliers.csv`: supplier regions and standard lead times.
- `inventory.csv`: stock snapshot for each product.

The orders file intentionally contains some missing values so you can practise data-quality checks. Do not claim results until you calculate them from your actual run.

## Recommended sequence
1. Inspect data and document data-quality issues in `notebooks/01_data_quality_and_eda.ipynb`.
2. Clean data and derive metrics such as order value, delivery delay, and on-time status.
3. Load clean tables into PostgreSQL and write analytical SQL queries.
4. Build a Power BI dashboard and basic DAX measures.
5. Forecast monthly demand with a simple baseline and evaluate the error.
6. Document limitations and business recommendations.

## Run
Install dependencies:
`python -m pip install pandas numpy matplotlib jupyter`

Start Jupyter:
`jupyter notebook`

Open the notebook under `notebooks/`.
