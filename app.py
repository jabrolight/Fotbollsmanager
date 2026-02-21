from flask import Flask
from backend import Liga

app = Flask(__name__)

premier_league = Liga("Lagen.db")

@app.route("/")
def start_sida():
    premier_league.fylla_dict_med_objekt()
    alla_lag = premier_league.alla_lagnamn()
    
    # 2. Servera datan (Webbläsare förstår enkla HTML-taggar som <h1>)
    return f"<h1>Min Fotbollsliga</h1><p>Lagen i databasen är: {alla_lag}</p>"

# Detta startar själva webbservern
if __name__ == "__main__":
    # debug=True gör att servern startar om sig själv automatiskt när du sparar kodändringar!
    app.run(debug=True)