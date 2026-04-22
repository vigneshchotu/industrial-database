import pandas as pd
import sqlite3
import os

# Connect to DB
conn = sqlite3.connect("industry.db")

# Get all CSV files in folder
files = [f for f in os.listdir() if f.endswith(".csv")]

print("Found CSV files:", files)

for file in files:
    try:
        df = pd.read_csv(file)

        # Clean table name (remove spaces & .csv)
        table_name = file.replace(".csv", "").replace(" ", "_").lower()

        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {file} → table: {table_name}")

    except Exception as e:
        print(f"Error loading {file}:", e)

conn.commit()
conn.close()

print("All datasets loaded successfully 🚀")