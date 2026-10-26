# SupplyChain IQ — Supply Chain Performance Dashboard

A data analytics project built using **Power BI, DAX, and Python** to analyze supply chain performance, order fulfillment, supplier reliability, and inventory levels.

## Project Overview

SupplyChain IQ is an interactive business intelligence dashboard designed to turn supply chain data into actionable insights. It helps users monitor order performance, identify delivery delays, compare supplier reliability, and highlight inventory that may require replenishment.

The project uses **synthetic data for demonstration and portfolio purposes**. It is not based on actual Philips company data.

## Objectives

- Monitor overall order value and order volume.
- Measure on-time delivery performance.
- Identify cancelled orders and delivery delays.
- Compare on-time delivery rates across suppliers.
- Monitor inventory stock against reorder levels.
- Identify products with the highest order value.
- Analyze order value trends over time.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Power BI Desktop | Dashboard development and data visualization |
| DAX | KPI calculations and analytical measures |
| Python | Data preparation and ETL pipeline |
| CSV | Source datasets |
| GitHub | Project version control and portfolio hosting |

## Dashboard KPIs

The dashboard includes six key performance indicators:

1. **Total Order Value** — Total value of eligible orders included in the calculation.
2. **On-Time Delivery Rate** — Percentage of delivered orders that arrived on or before the promised delivery date.
3. **Low Stock Products** — Number of products with stock below their reorder level.
4. **Total Orders** — Distinct count of order IDs.
5. **Cancelled Orders** — Number of distinct orders marked as cancelled.
6. **Average Delivery Delay (Days)** — Average difference between actual and promised delivery dates for delivered orders. Early deliveries can contribute negative values.

## Dashboard Visualizations

The report contains the following analytical visuals:

- Orders by Status
- Order Status Distribution
- Supplier On-Time Delivery Rate
- Monthly Order Value Trend
- Inventory Stock vs Reorder Level
- Top 10 Products by Order Value
- On-Time vs Late Deliveries

Together, these visuals provide an overview of order fulfillment, supplier performance, delivery reliability, product value, and inventory conditions.

## Dataset

The project uses four synthetic CSV datasets:

| File | Description |
|---|---|
| `orders.csv` | Order IDs, product and supplier references, order status, dates, quantity, and unit price |
| `products.csv` | Product details and reorder levels |
| `suppliers.csv` | Supplier information |
| `inventory.csv` | Product stock levels |

The dataset contains approximately **2,200 orders**. The data is intended for learning, demonstration, and portfolio use.

## Project Structure

```text
SupplyChain-IQ/
├── data/
│   ├── raw/
│   │   ├── orders.csv
│   │   ├── products.csv
│   │   ├── suppliers.csv
│   │   └── inventory.csv
│   └── processed/
├── etl_pipeline.py
├── SupplyChain_IQ_Dashboard.pbix
├── README.md
└── .gitignore
```

*The structure above represents the intended repository layout. Adjust filenames and folders to match the files actually uploaded.*

## Key Insights

The current dashboard highlights several areas for investigation:

- On-time delivery performance is below 50% in the current dataset.
- Supplier on-time delivery rates vary, making supplier comparison useful.
- Cancelled orders represent a separate category of order outcomes.
- Inventory comparisons can identify products whose stock is below reorder thresholds.
- Product-level order value analysis helps identify products contributing the most order value.

These are observations from synthetic data and should not be interpreted as real-world company performance.

## How to Use

1. Clone or download this repository.
2. Open `SupplyChain_IQ_Dashboard.pbix` using Power BI Desktop.
3. If Power BI prompts for data sources, update the paths to the CSV files in the repository.
4. Refresh the data if required.
5. Explore the KPI cards, charts, and filters in the report.

## Future Improvements

- Add interactive date, supplier, and product slicers.
- Improve inventory risk highlighting for products below reorder levels.
- Add additional delivery-delay and supplier performance analysis.
- Validate all KPI calculations against the source data.
- Publish an interactive online version where account permissions allow.

## Disclaimer

This is an educational portfolio project using synthetic data. It is not affiliated with, endorsed by, or based on confidential information from Philips or any other company.

## Author

**Aarnit Nair**

Aspiring Data Analyst | Power BI | Python | SQL | Data Visualization

