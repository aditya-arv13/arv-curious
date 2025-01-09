import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request

app = Flask(__name__)

# Securely store the password hash
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get("ADMIN_PASSWORD", "password123"))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        return "Welcome, admin!"
    return "Access Denied!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)