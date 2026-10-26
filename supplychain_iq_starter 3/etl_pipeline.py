
from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "supplychain.db"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. EXTRACT: READ RAW DATASETS
# ============================================================

def extract_data():
    """Load raw supply-chain CSV files."""

    required_files = [
        "orders.csv",
        "products.csv",
        "suppliers.csv",
        "inventory.csv",
    ]

    for filename in required_files:
        file_path = RAW_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required dataset not found: {file_path}"
            )

    orders = pd.read_csv(
        RAW_DIR / "orders.csv",
        parse_dates=[
            "order_date",
            "promised_delivery_date",
            "actual_delivery_date",
        ],
    )

    products = pd.read_csv(RAW_DIR / "products.csv")
    suppliers = pd.read_csv(RAW_DIR / "suppliers.csv")

    inventory = pd.read_csv(
        RAW_DIR / "inventory.csv",
        parse_dates=["snapshot_date"],
    )

    print("\nEXTRACTION SUMMARY")
    print("-" * 40)
    print(f"Orders: {len(orders)}")
    print(f"Products: {len(products)}")
    print(f"Suppliers: {len(suppliers)}")
    print(f"Inventory records: {len(inventory)}")

    return orders, products, suppliers, inventory


# ============================================================
# 3. DATA QUALITY VALIDATION
# ============================================================

def validate_data(orders, products, suppliers, inventory):
    """Identify missing values, duplicates and invalid records."""

    checks = {
        "Missing order IDs": orders["order_id"].isna().sum(),
        "Duplicate order IDs": orders["order_id"].duplicated().sum(),
        "Missing quantities": orders["quantity"].isna().sum(),
        "Missing supplier IDs": orders["supplier_id"].isna().sum(),
        "Zero or negative quantities": (
            orders["quantity"].notna()
            & (orders["quantity"] <= 0)
        ).sum(),
        "Missing product IDs": products["product_id"].isna().sum(),
        "Duplicate product IDs": products["product_id"].duplicated().sum(),
        "Missing supplier master IDs": suppliers["supplier_id"].isna().sum(),
        "Duplicate supplier master IDs": (
            suppliers["supplier_id"].duplicated().sum()
        ),
        "Missing inventory product IDs": (
            inventory["product_id"].isna().sum()
        ),
        "Duplicate inventory product IDs": (
            inventory["product_id"].duplicated().sum()
        ),
    }

    print("\nDATA QUALITY REPORT")
    print("-" * 40)

    for check, count in checks.items():
        print(f"{check}: {count}")

    return checks


# ============================================================
# 4. TRANSFORM: CLEAN AND ENRICH ORDERS
# ============================================================

def transform_orders(orders):
    """Clean order identifiers and create analytical fields."""

    orders = orders.copy()

    original_count = len(orders)

    # Remove records without a usable order identifier.
    orders = orders.dropna(subset=["order_id"])

    # Keep the first occurrence of each order ID.
    orders = orders.drop_duplicates(
        subset=["order_id"],
        keep="first",
    )

    # Calculate delivery delay in days.
    orders["delivery_delay_days"] = (
        orders["actual_delivery_date"]
        - orders["promised_delivery_date"]
    ).dt.days

    # Calculate order value only where quantity and price are known.
    orders["order_value"] = (
        orders["quantity"] * orders["unit_price"]
    )

    # On-time flag: 1 for on-time delivered orders, otherwise 0.
    # Missing delivery delay is treated as not verified on time.
    orders["on_time"] = (
        (orders["order_status"] == "Delivered")
        & orders["delivery_delay_days"].notna()
        & (orders["delivery_delay_days"] <= 0)
    ).astype(int)

    print("\nTRANSFORMATION SUMMARY")
    print("-" * 40)
    print(f"Rows before transformation: {original_count}")
    print(f"Rows after transformation: {len(orders)}")
    print(f"Rows removed: {original_count - len(orders)}")
    print(f"Missing order values: {orders['order_value'].isna().sum()}")

    return orders


# ============================================================
# 5. TRANSFORM: VALIDATE REFERENCE DATA
# ============================================================

def transform_reference_data(products, suppliers, inventory):
    """Remove rows missing primary identifiers and duplicate keys."""

    products = products.copy()
    suppliers = suppliers.copy()
    inventory = inventory.copy()

    products = products.dropna(subset=["product_id"])
    products = products.drop_duplicates(
        subset=["product_id"],
        keep="first",
    )

    suppliers = suppliers.dropna(subset=["supplier_id"])
    suppliers = suppliers.drop_duplicates(
        subset=["supplier_id"],
        keep="first",
    )

    inventory = inventory.dropna(subset=["product_id"])
    inventory = inventory.drop_duplicates(
        subset=["product_id"],
        keep="first",
    )

    return products, suppliers, inventory


# ============================================================
# 6. LOAD: SAVE PROCESSED DATA AND SQL TABLES
# ============================================================

def load_data(orders, products, suppliers, inventory):
    """Write processed CSVs and load SQLite tables."""

    orders.to_csv(
        OUTPUT_DIR / "orders_clean.csv",
        index=False,
    )

    products.to_csv(
        OUTPUT_DIR / "products.csv",
        index=False,
    )

    suppliers.to_csv(
        OUTPUT_DIR / "suppliers.csv",
        index=False,
    )

    inventory.to_csv(
        OUTPUT_DIR / "inventory.csv",
        index=False,
    )

    with sqlite3.connect(DB_PATH) as conn:
        orders.to_sql(
            "orders",
            conn,
            if_exists="replace",
            index=False,
        )

        products.to_sql(
            "products",
            conn,
            if_exists="replace",
            index=False,
        )

        suppliers.to_sql(
            "suppliers",
            conn,
            if_exists="replace",
            index=False,
        )

        inventory.to_sql(
            "inventory",
            conn,
            if_exists="replace",
            index=False,
        )

    print("\nLOAD SUMMARY")
    print("-" * 40)
    print(f"Processed files saved to: {OUTPUT_DIR}")
    print(f"SQLite database: {DB_PATH}")


# ============================================================
# 7. VERIFY LOADED DATABASE
# ============================================================

def verify_database():
    """Verify row counts and data quality in SQLite."""

    with sqlite3.connect(DB_PATH) as conn:
        order_count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM orders",
            conn,
        ).iloc[0]["total"]

        missing_quantities = pd.read_sql_query(
            """
            SELECT COUNT(*) AS total
            FROM orders
            WHERE quantity IS NULL
            """,
            conn,
        ).iloc[0]["total"]

        missing_suppliers = pd.read_sql_query(
            """
            SELECT COUNT(*) AS total
            FROM orders
            WHERE supplier_id IS NULL
            """,
            conn,
        ).iloc[0]["total"]

    print("\nDATABASE VERIFICATION")
    print("-" * 40)
    print(f"Orders loaded: {order_count}")
    print(f"Missing quantities retained: {missing_quantities}")
    print(f"Missing supplier IDs retained: {missing_suppliers}")

    if order_count == 0:
        raise ValueError("Database verification failed: no orders loaded.")


# ============================================================
# 8. MAIN ETL WORKFLOW
# ============================================================

def main():
    print("=" * 50)
    print("SUPPLYCHAIN IQ - ETL PIPELINE")
    print("=" * 50)

    try:
        # EXTRACT
        orders, products, suppliers, inventory = extract_data()

        # VALIDATE RAW DATA
        validate_data(orders, products, suppliers, inventory)

        # TRANSFORM
        orders_clean = transform_orders(orders)

        products_clean, suppliers_clean, inventory_clean = (
            transform_reference_data(
                products,
                suppliers,
                inventory,
            )
        )

        # LOAD
        load_data(
            orders_clean,
            products_clean,
            suppliers_clean,
            inventory_clean,
        )

        # VERIFY
        verify_database()

        print("\nETL PIPELINE COMPLETED SUCCESSFULLY.")

    except Exception as error:
        print(f"\nETL PIPELINE FAILED: {error}")
        raise


if __name__ == "__main__":
    main()
