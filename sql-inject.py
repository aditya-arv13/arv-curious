import sqlite3
import os
from flask import Flask, request

# Initialize the Flask app
app = Flask(__name__)

# Function to create the database and table if they don't exist
def initialize_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # Create the users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL
        )
        """)
        
        # Insert some sample data
        cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("john_doe", "john@example.com"))
        cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("jane_doe", "jane@example.com"))
        
        conn.commit()
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists.")

# Function to query the database
def query_db(query):
    conn = sqlite3.connect("C:\\Users\\MC-Agartala-ARV\\Desktop\\IMD-Work\\Dev\\database.db")
    cur = conn.cursor()
    cur.execute(query)  # Vulnerability: Unsanitized input
    rows = cur.fetchall()
    conn.close()
    return rows

# Flask route to fetch users
@app.route('/users', methods=['GET'])
def users():
    username = request.args.get('username')
    if username:
        query = f"SELECT * FROM users WHERE username = '{username}'"
        results = query_db(query)
        return {"results": results}
    else:
        return {"error": "Username parameter is required"}, 400

if __name__ == "__main__":
    initialize_db()  # Ensure the database is initialized before starting the app
    app.run(host="0.0.0.0", port=5000)

#ttps://www.example.com/index.php?username=1'%20or%20'1'%20=%20'1&amp;password=1'%20or%20'1'%20=%20'1