import pandas as pd
import sqlite3
import random

from faker import Faker

fake = Faker()

# Create SALES erp
sales_data = []

for i in range(5000):

    sales_data.append({
        "order_id": i + 1,
        "cust_id": random.randint(1000, 2000),
        "order_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        ).strftime("%Y-%m-%d"),
        "total_price": round(
            random.uniform(50, 5000),
            2
        )
    })

sales_df = pd.DataFrame(sales_data)


# Create Inventory erp
inventory_data = []

for i in range(5000):

    inventory_data.append({
        "transaction_id": i + 1,
        "customer_code": random.randint(1000, 2000),
        "transaction_timestamp": fake.date_between(
            start_date="-2y",
            end_date="today"
        ).strftime("%d/%m/%Y"),
        "product_cost": round(
            random.uniform(10, 3000),
            2
        )
    })

inventory_df = pd.DataFrame(inventory_data)


# create Finance erp
finance_data = []

for i in range(5000):

    finance_data.append({
        "payment_ref": i + 1,
        "client_id": random.randint(1000, 2000),
        "payment_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        ).strftime("%m-%d-%Y"),
        "revenue_amount": round(
            random.uniform(100, 10000),
            2
        )
    })

finance_df = pd.DataFrame(finance_data)

# SQLite connection
sales_conn = sqlite3.connect(
    "data_sources/sales_erp.db"
)

inventory_conn = sqlite3.connect(
    "data_sources/inventory_erp.db"
)

finance_conn = sqlite3.connect(
    "data_sources/finance_erp.db"
)

#save data into sqlite
sales_df.to_sql(
    "orders",
    sales_conn,
    if_exists="replace",
    index=False
)

inventory_df.to_sql(
    "inventory_transactions",
    inventory_conn,
    if_exists="replace",
    index=False
)

finance_df.to_sql(
    "finance_payments",
    finance_conn,
    if_exists="replace",
    index=False
)

# close sqlite connection
sales_conn.close()
inventory_conn.close()
finance_conn.close()

print("Fake ERP systems created")