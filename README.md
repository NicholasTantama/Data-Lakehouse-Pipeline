# Data-Lakehouse-Pipeline
Data sources:
- finance_erp.db
- inventory_erp.db
- sales_erp.db

docker-compose.yml: Create container for project environment

Scripts
- generate_fake_erps.py: Only used once in the beginning to generate data using faker
- bronze_ingestion.py: For ingesting raw data into bronze layer
- silver_transformation.py: For data cleaning and then storing in silver layer
- gold_aggregation.py: aggregate data to until ready for business usage and then stored in gold layer
- query_engine.py: querying data from gold layer in minIO
- pipeline.py: run this file to automatically run pipeline from "bronze_ingestion.py" until "query_engine.py"
- dashboard.py: dashboard creation using streamlit
