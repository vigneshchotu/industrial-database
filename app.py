from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🟢 AUTO LOAD DATA (VERY IMPORTANT FOR DEPLOYMENT)
def load_data():
    conn = sqlite3.connect("industry.db")

    for file in os.listdir():
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(file)

                table_name = file.replace(".csv", "").replace(" ", "_").lower()
                df.to_sql(table_name, conn, if_exists="replace", index=False)

                print(f"Loaded {file} → {table_name}")

            except Exception as e:
                print(f"Error loading {file}: {e}")

    conn.close()

# 🔴 Call this when app starts
load_data()


# Connect to DB
def get_connection():
    conn = sqlite3.connect("industry.db")
    conn.row_factory = sqlite3.Row
    return conn


# Get all table names
@app.route('/tables')
def get_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return jsonify(tables)


# Get data from any table
@app.route('/data/<table_name>')
def get_data(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
    except Exception as e:
        result = {"error": str(e)}

    conn.close()
    return jsonify(result)


# Home
@app.route('/')
def home():
    return "Dynamic API running 🚀"


# 🔥 IMPORTANT FOR RENDER DEPLOYMENT
if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))    