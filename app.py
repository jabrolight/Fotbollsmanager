from flask import Flask, render_template
from backend import Liga


app = Flask(__name__)

premier_league = Liga("Lagen.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

# Detta startar själva webbservern
if __name__ == "__main__":
    # debug=True gör att servern startar om sig själv automatiskt när du sparar kodändringar!
    app.run(debug=True)