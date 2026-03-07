from flask import Flask, render_template
from backend import Liga


app = Flask(__name__)

premier_league = Liga("Lagen.db") #här skapar premier league

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

@app.route("/demotabell")
def demotabell():
    #premier_league.fylla_dict_med_objekt()
    tabell= premier_league.dict_med_lag
    return render_template("demo_tabell.html", demo_tabell= tabell)

@app.route("/dokumentera")
def dokumentera_match():
    return render_template("dokumentera_match.html")
if __name__ == "__main__":
    # debug=True gör att servern startar om sig själv automatiskt när du sparar kodändringar!
    app.run(debug=True)