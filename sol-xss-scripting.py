from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    # Flask's template rendering escapes user input by default
    return render_template_string("<h1>Welcome, {{ name|e }}!</h1>", name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)