from flask import Flask, request

app = Flask(__name__)

# Vulnerability: Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return "Welcome, admin!"
    return "Access Denied!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)