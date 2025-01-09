import sqlite3
from flask import Flask, request

app = Flask(__name__)

def query_db(query, args=()):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query, args)  # Secure parameterized query
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/users', methods=['GET'])
def users():
    username = request.args.get('username')
    query = "SELECT * FROM users WHERE username = ?"
    results = query_db(query, (username,))
    return {"results": results}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)