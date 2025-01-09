from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    # Vulnerability: Unescaped user input directly rendered
    return render_template_string(f"<h1>Welcome, {name}!</h1>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)