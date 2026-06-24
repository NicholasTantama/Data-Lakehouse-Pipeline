import duckdb

# connect to DuckDB
con = duckdb.connect("lakehouse.duckdb")

# enable MinIO (S3) access
con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

con.execute("""
SET s3_endpoint='localhost:9000';
""")

con.execute("""
SET s3_access_key_id='admin';
""")

con.execute("""
SET s3_secret_access_key='password123';
""")

con.execute("""
SET s3_use_ssl=false;
""")

con.execute("""
SET s3_url_style='path';
""")

print("DuckDB connected")

# DAILY REVENUE VIEW
con.execute("""
CREATE OR REPLACE VIEW daily_revenue_view AS
SELECT *
FROM read_parquet(
    's3://gold/daily_revenue.parquet'
)
""")

print("Daily revenue view created")

# MONTHLY REVENUE VIEW
con.execute("""
CREATE OR REPLACE VIEW monthly_revenue_view AS
SELECT *
FROM read_parquet(
    's3://gold/monthly_revenue.parquet'
)
""")

print("Monthly revenue view created")

# ERP SUMMARY VIEW
con.execute("""
CREATE OR REPLACE VIEW source_summary_view AS
SELECT *
FROM read_parquet(
    's3://gold/source_summary.parquet'
)
""")

print("ERP summary view created")

# CUSTOMER SUMMARY VIEW
con.execute("""
CREATE OR REPLACE VIEW customer_summary_view AS
SELECT *
FROM read_parquet(
    's3://gold/customer_summary.parquet'
)
""")

print("Customer summary view created")


# close connection
con.close()

print("\nDuckDB session closed")

# query testing
#result = con.sql("""

#SELECT *
#FROM monthly_revenue_view
#LIMIT 5

#""").df()

#print(result)