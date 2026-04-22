from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

if __name__ == '__main__':
    app.run(debug=True)