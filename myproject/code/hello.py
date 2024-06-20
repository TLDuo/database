from flask import Flask,request,render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello/<name>")
def hello(name):
    return render_template("profile.html", name=name)

@app.route("/hello")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/hi")
def hi():
    return "<h1>hi hi!</h1>"

if __name__ == "__main__":
    app.run(debug=True)