"""
# Vulnerable Flask App - Security Testing Guide

## 1. SQL Injection Testing
   - **Login Bypass** (Submit in username field, leave password blank):
     ```
     ' OR '1'='1
     ```
   - **Extract Users from Database** (Submit in search bar):
     ```
     ' UNION SELECT username, password FROM users--
     ```
   - **Login as Admin without Password:**
     ```
     admin' -- 
     ```
   - **Delete Users Table** (DANGEROUS: Do not run on a real system):
     ```
     '; DROP TABLE users; --
     ```

## 2. Cross-Site Scripting (XSS) Testing
   - Submit this payload in the comment box:
     ```html
     <script>alert('XSS Attack!')</script>
     ```
   - After submission, visit `/posts`, and you should see an alert pop up.

## 3. Insecure File Upload Testing
   - Upload a **malicious Python or PHP script** (`malware.py` or `shell.php`).
   - Try accessing it via `http://127.0.0.1:5000/uploads/malware.py`.
   - If executed, this could lead to **Remote Code Execution (RCE)**.

## 4. Debugging & Exploitation
   - Check **SQL queries printed in the terminal** (`print("[DEBUG] Query:", query)`).
   - Try **different attack variations** to see how the app behaves.

!!! WARNING: This application is INTENTIONALLY VULNERABLE and should NEVER be used in production !!!
"""

from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# **Vulnerable File Uploads Directory**
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# **Database Initialization**
DB_FILE = "users.db"

def init_db():
    """ Creates database and tables if they do not exist. """
    if not os.path.exists(DB_FILE):  # Check if DB file exists
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # **Create Tables**
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, content TEXT)")

        # **Insert Default User (for SQL Injection Testing)**
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

init_db()  # Run this function when the app starts

# **Home Page**
@app.route("/")
def home():
    return render_template("index.html")

# **Vulnerable Login - SQL Injection**
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # **SQL Injection Vulnerable Query**
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[DEBUG] Query:", query)

    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"Welcome {username}!"
    else:
        return "Invalid Credentials!"

# **Vulnerable Search - SQL Injection**
@app.route("/search", methods=["GET"])
def search():
    term = request.args.get("q", "")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username LIKE '%{term}%'"
    print("[DEBUG] Query:", query)

    c.execute(query)
    results = c.fetchall()
    conn.close()

    return f"Search Results: {results}"

# **Vulnerable XSS Submission**
@app.route("/submit", methods=["POST"])
def submit():
    content = request.form["content"]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("INSERT INTO posts (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

    return "Post Submitted!"

# **Display Posts (XSS Reflection)**
@app.route("/posts")
def posts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("SELECT content FROM posts")
    posts = c.fetchall()
    conn.close()
    
    return "<br>".join(post[0] for post in posts)

# **Vulnerable File Upload**
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return f"File uploaded: {filepath}"

# **Run the Flask Server**
if __name__ == "__main__":
    app.run(debug=True)