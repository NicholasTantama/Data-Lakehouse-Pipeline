import pandas as pd
import sqlite3
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)


# sales ERP ingestion
sales_conn = sqlite3.connect(
    "data_sources/sales_erp.db"
)

sales_df = pd.read_sql(
    "SELECT * FROM orders",
    sales_conn
)

sales_df = sales_df.astype(str)

sales_df.to_parquet(
    "bronze/sales_raw.parquet",
    index=False
)

client.fput_object(
    "bronze",
    "sales_raw.parquet",
    "bronze/sales_raw.parquet"
)

sales_conn.close()

print("Sales ERP ingested")

# inventory erp ingestion
inventory_conn = sqlite3.connect(
    "data_sources/inventory_erp.db"
)

inventory_df = pd.read_sql(
    "SELECT * FROM inventory_transactions",
    inventory_conn
)

inventory_df = inventory_df.astype(str)

inventory_df.to_parquet(
    "bronze/inventory_raw.parquet",
    index=False
)

client.fput_object(
    "bronze",
    "inventory_raw.parquet",
    "bronze/inventory_raw.parquet"
)

inventory_conn.close()

print("Inventory ERP ingested")

# finance erp ingestion
finance_conn = sqlite3.connect(
    "data_sources/finance_erp.db"
)

finance_df = pd.read_sql(
    "SELECT * FROM finance_payments",
    finance_conn
)

finance_df = finance_df.astype(str)

finance_df.to_parquet(
    "bronze/finance_raw.parquet",
    index=False
)

client.fput_object(
    "bronze",
    "finance_raw.parquet",
    "bronze/finance_raw.parquet"
)

finance_conn.close()

print("Finance ERP ingested")