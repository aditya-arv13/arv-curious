import sqlite3
from flask import Flask, request

app = Flask(__name__)

def query_db(query):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query)  # Vulnerability: Unsanitized input
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/users', methods=['GET'])
def users():
    username = request.args.get('username')
    query = f"SELECT * FROM users WHERE username = '{username}'"
    results = query_db(query)
    return {"results": results}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)