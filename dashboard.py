import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="Modern Lakehouse Dashboard",
    layout="wide"
)

st.title("Modern Data Lakehouse Dashboard")

# DuckDB connection
con = duckdb.connect("lakehouse.duckdb")

# MinIO configuration
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

# Load data
daily_df = con.sql("""
SELECT *
FROM daily_revenue_view
""").df()

monthly_df = con.sql("""
SELECT *
FROM monthly_revenue_view
""").df()

source_df = con.sql("""
SELECT *
FROM source_summary_view
""").df()

customer_df = con.sql("""
SELECT *
FROM customer_summary_view
""").df()

# KPI metrics
total_revenue = source_df["total_revenue"].sum()

total_transactions = source_df[
    "transaction_count"
].sum()

total_customers = customer_df[
    "customer_id"
].nunique()

# KPI cards
st.header("Executive Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col3.metric(
    "Total Customers",
    f"{total_customers:,}"
)

st.divider()

# Revenue Analytics
st.header("Revenue Analytics")

left, right = st.columns(2)

with left:

    daily_chart = px.line(
        daily_df,
        x="transaction_date",
        y="daily_revenue",
        title="Daily Revenue Trend"
    )

    st.plotly_chart(
        daily_chart,
        width="stretch"
    )

with right:

    monthly_chart = px.bar(
        monthly_df,
        x="month",
        y="monthly_revenue",
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(
        monthly_chart,
        width="stretch"
    )

st.divider()

# ERP Analytics
st.header("ERP Analytics")

left, right = st.columns(2)

with left:

    erp_pie = px.pie(
        source_df,
        names="data_sources",
        values="total_revenue",
        title="Revenue Contribution by ERP"
    )

    st.plotly_chart(
        erp_pie,
        width="stretch"
    )

with right:

    erp_bar = px.bar(
        source_df,
        x="data_sources",
        y="total_revenue",
        title="ERP Revenue Comparison"
    )

    st.plotly_chart(
        erp_bar,
        width="stretch"
    )

st.divider()

# Customer Analytics
st.header("Customer Analytics")

top_customers = customer_df.sort_values(
    by="total_spent",
    ascending=False
).head(10)

customer_chart = px.bar(
    top_customers,
    x="customer_id",
    y="total_spent",
    title="Top 10 Customers"
)

st.plotly_chart(
    customer_chart,
    width="stretch"
)

st.dataframe(
    top_customers,
    width="stretch"
)

st.divider()

# Data Quality Section
st.header("Data Quality Overview")

dq1, dq2, dq3 = st.columns(3)

dq1.metric(
    "Records Processed",
    f"{total_transactions:,}"
)

dq2.metric(
    "ERP Sources",
    f"{source_df['data_sources'].nunique()}"
)

dq3.metric(
    "Unique Customers",
    f"{total_customers:,}"
)

con.close()