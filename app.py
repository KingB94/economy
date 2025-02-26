from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")

@app.route("/countries")
def countries():
    return render_template("countries.html")

@app.route("/comparative")
def comparative():
    return render_template("comparative.html")

if __name__ == "__main__":
    app.run(debug=True)
