import sqlite3

conn = sqlite3.connect("industry.db")
cursor = conn.cursor()

# Show tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in DB:")
for table in tables:
    print("-", table[0])

print("\nSample Data:\n")

# Show 3 rows from each table
for table in tables:
    table_name = table[0]
    print(f"--- {table_name} ---")

    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    except Exception as e:
        print("Error:", e)

    print("\n")

conn.close()