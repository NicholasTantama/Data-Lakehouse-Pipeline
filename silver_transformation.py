import pandas as pd
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

# Load bronze data
sales_df = pd.read_parquet(
    "bronze/sales_raw.parquet"
)

inventory_df = pd.read_parquet(
    "bronze/inventory_raw.parquet"
)

finance_df = pd.read_parquet(
    "bronze/finance_raw.parquet"
)

print("Bronze data loaded")


# standardize customer column
sales_df.rename(columns={
    "cust_id": "customer_id"
}, inplace=True)

inventory_df.rename(columns={
    "customer_code": "customer_id"
}, inplace=True)

finance_df.rename(columns={
    "client_id": "customer_id"
}, inplace=True)


# standardize date column
sales_df.rename(columns={
    "order_date": "transaction_date"
}, inplace=True)

inventory_df.rename(columns={
    "transaction_timestamp": "transaction_date"
}, inplace=True)

finance_df.rename(columns={
    "payment_date": "transaction_date"
}, inplace=True)


# standardize amount column
sales_df.rename(columns={
    "total_price": "amount"
}, inplace=True)

inventory_df.rename(columns={
    "product_cost": "amount"
}, inplace=True)

finance_df.rename(columns={
    "revenue_amount": "amount"
}, inplace=True)


# convert dates
sales_df["transaction_date"] = pd.to_datetime(
    sales_df["transaction_date"]
)

inventory_df["transaction_date"] = pd.to_datetime(
    inventory_df["transaction_date"],
    dayfirst=True
)

finance_df["transaction_date"] = pd.to_datetime(
    finance_df["transaction_date"]
)


# convert amount to numeric
sales_df["amount"] = pd.to_numeric(
    sales_df["amount"]
)

inventory_df["amount"] = pd.to_numeric(
    inventory_df["amount"]
)

finance_df["amount"] = pd.to_numeric(
    finance_df["amount"]
)


# source tracking
sales_df["data_sources"] = "sales_erp"

inventory_df["data_sources"] = "inventory_erp"

finance_df["data_sources"] = "finance_erp"


# remove duplicate data
sales_df.drop_duplicates(inplace=True)

inventory_df.drop_duplicates(inplace=True)

finance_df.drop_duplicates(inplace=True)


# remove nulls
sales_df.dropna(inplace=True)

inventory_df.dropna(inplace=True)

finance_df.dropna(inplace=True)


# create unified record_id
sales_df.rename(columns={
    "order_id": "record_id"
}, inplace=True)

inventory_df.rename(columns={
    "transaction_id": "record_id"
}, inplace=True)

finance_df.rename(columns={
    "payment_ref": "record_id"
}, inplace=True)


# keep only standardize columns
sales_df = sales_df[[
    "record_id",
    "customer_id",
    "transaction_date",
    "amount",
    "data_sources"
]]

inventory_df = inventory_df[[
    "record_id",
    "customer_id",
    "transaction_date",
    "amount",
    "data_sources"
]]

finance_df = finance_df[[
    "record_id",
    "customer_id",
    "transaction_date",
    "amount",
    "data_sources"
]]


# combine datasets
master_df = pd.concat([
    sales_df,
    inventory_df,
    finance_df
], ignore_index=True)

print("Unified dataset created")


# save silver parquet and upload to minIO
master_df.to_parquet(
    "silver/unified_transactions.parquet",
    index=False
)

client.fput_object(
    "silver",
    "unified_transactions.parquet",
    "silver/unified_transactions.parquet"
)

print("Silver layer uploaded")