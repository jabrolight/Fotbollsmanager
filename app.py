from flask import Flask, render_template, redirect, flash, url_for
from backend import Liga
from flask import request

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


# Vi tillåter BÅDE GET (hämta sidan) och POST (skicka formulär)
@app.route("/dokumentera", methods=["GET", "POST"])
def dokumentera():
    
    # 1. OM ANVÄNDAREN HAR KLICKAT PÅ "SPARA MATCH" (POST)
    if request.method == "POST":
        # Hämta datan från formuläret
        hemma = request.form.get("hemmalag")
        borta = request.form.get("bortalag")
        h_mal = int(request.form.get("hemmamal"))
        b_mal = int(request.form.get("bortamal"))
        
        # Spara i SQL via din backend!
        premier_league.dokumentera_match2(hemma, borta, h_mal, b_mal)
        

    # 2. DETTA KÖRS ALLTID (Oavsett GET eller POST)
    # Hämta den allra senaste datan från databasen
    premier_league.fylla_dict_med_objekt()
    lagen= premier_league.dict_med_lag
    senaste_historiken = premier_league.hämta_historik()
    
    # Rendera SAMMA sida igen, nu med uppdaterad historik!
    return render_template("dokumentera_match.html", 
                           lagnamn=lagen, 
                           historik=senaste_historiken)


@app.route("/radera_match/<int:match_id>", methods=["POST"])
def radera_match_route(match_id):
    # 1. Anropa din skottsäkra backend-metod för att uppdatera databasen
    premier_league.radera_match(match_id)
    
    # 2. Skapa ett flash-meddelande som bekräftar raderingen
    # Om du vill att rutan ska vara röd kan du byta "success" mot "fel"
    #flash("Matchen har raderats från historiken och poängen är återställd.", "success")
    
    # 3. Skicka tillbaka användaren till exakt samma sida!
    return redirect(url_for('dokumentera'))

if __name__ == "__main__":
    # debug=True gör att servern startar om sig själv automatiskt när du sparar kodändringar!
    app.run(debug=True)