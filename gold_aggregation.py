import pandas as pd
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)


# load silver data
df = pd.read_parquet(
    "silver/unified_transactions.parquet"
)

print("Silver data loaded")


# daily revenue summary
daily_revenue = (
    df.groupby("transaction_date")
    .agg({
        "amount": "sum"
    })
    .reset_index()
)

daily_revenue.rename(columns={
    "amount": "daily_revenue"
}, inplace=True)

print("Daily revenue summary created")


# monthly revenue summary
df["month"] = df["transaction_date"].dt.to_period("M")

monthly_revenue = (
    df.groupby("month")
    .agg({
        "amount": "sum"
    })
    .reset_index()
)

monthly_revenue.rename(columns={
    "amount": "monthly_revenue"
}, inplace=True)

print("Monthly revenue summary created")


# create ERP performance summary
source_summary = (
    df.groupby("data_sources")
    .agg({
        "amount": ["sum", "mean", "count"]
    })
)

source_summary.columns = [
    "total_revenue",
    "average_transaction",
    "transaction_count"
]

source_summary = source_summary.reset_index()

print("ERP summary created")


# Customer summary
customer_summary = (
    df.groupby("customer_id")
    .agg({
        "amount": ["sum", "count"]
    })
)

customer_summary.columns = [
    "total_spent",
    "transaction_count"
]

customer_summary = customer_summary.reset_index()
print("customer summary created")


# save everything
daily_revenue.to_parquet(
    "gold/daily_revenue.parquet",
    index=False
)

monthly_revenue.to_parquet(
    "gold/monthly_revenue.parquet",
    index=False
)

source_summary.to_parquet(
    "gold/source_summary.parquet",
    index=False
)

customer_summary.to_parquet(
    "gold/customer_summary.parquet",
    index=False
)


# upload all to minIO
client.fput_object(
    "gold",
    "daily_revenue.parquet",
    "gold/daily_revenue.parquet"
)

client.fput_object(
    "gold",
    "monthly_revenue.parquet",
    "gold/monthly_revenue.parquet"
)

client.fput_object(
    "gold",
    "source_summary.parquet",
    "gold/source_summary.parquet"
)

client.fput_object(
    "gold",
    "customer_summary.parquet",
    "gold/customer_summary.parquet"
)

print("Gold layer uploaded")