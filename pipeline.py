import subprocess
import sys

steps = [

    "scripts/bronze_ingestion.py",

    "scripts/silver_transformation.py",

    "scripts/gold_aggregation.py",

    "scripts/query_engine.py"

]

for step in steps:

    print(f"\nRunning {step}")
    
    subprocess.run(
        [sys.executable, step],
        check=True
    )

print("\nPipeline complete")
