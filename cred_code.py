from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerability: Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# HTML template for login page
LOGIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
</head>
<body>
    <h1>Login</h1>
    <form action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return "Welcome, admin!"
    return "Access Denied!"

# Route to render the login page
@app.route('/')
def login_page():
    return render_template_string(LOGIN_PAGE_HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
