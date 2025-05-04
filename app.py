import os
import random
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Oppdatert liste over Glimt-spillere
glimt_spillere = [
    "Julian Rekdahl Faye Lund", "Nikita Haikin", "Magnus Brøndbo",
    "Villads Schmidt Nielsen", "Odin Luraas Bjørtuft", "Haitam Aleesami",
    "Jostein Maurstad Gundersen", "Fredrik André Bjørkan", "Brede Mathias Moe",
    "Fredrik Sjøvold", "Patrick Berg", "Sondre Auklend", "Ulrik Saltnes",
    "Sondre Brunstad Fet", "Håkon Evjen", "Jeppe Kjær Jensen",
    "Kasper Waarts Thenza Høgh", "Jens Petter Hauge", "Ole Didrik Blomberg",
    "Andreas Klausen Helmersen", "Daniel Joshua Bassi Jakobsen",
    "Isak Dybvik Määttä", "Sondre Sørli", "Mikkel Bro Hansen"
]

intro = [
    "Hmm... la mæ føle litt på kraftan...",
    "Vent no litt... æ må ta inn energian...",
    "Oooh... det her kjennes mørkt ut...",
    "Troll-Tove føle noe... skummelt..."
]

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

spaadommer_fotball = [
    "Glimt knuse dritten ut av motstanderen, som vanlig.",
    "Rosenborg? Pfft. Som en flat pakke med sørpe.",
    "Det blir 2-1 te Glimt, og publikum skrik som besatt.",
    "Dommeren blir å fuck opp, men Glimt vinn lell.",
    "Glimt-spilleran e på krigsstien. Det luktar 3-0.",
    "Tilskuera skal få valuta førr penga: 4-2 og fyrverkeri baklengs.",
    "Brann ryke i flammå - bokstavelig talt. Glimt 5-1.",
    "Tromsø? Dem still med rullator. Glimt slakte dem."
]

def hent_neste_glimt_kamp():
    api_key = os.getenv("FOOTBALL_API_KEY")
    if not api_key:
        return "API-nøkkel mangla. Faen."

    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": api_key
    }
    params = {
        "team": 971,  # Bodø/Glimt sin ID hos API-Football
        "next": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        fixture = data["response"][0]
        hjemmelag = fixture["teams"]["home"]["name"]
        bortelag = fixture["teams"]["away"]["name"]
        dato = fixture["fixture"]["date"][:10]

        glimt_hjemme = hjemmelag.lower() == "bodø/limt"
        resultat = ""

        if glimt_hjemme:
            resultat = f"{hjemmelag} vinn 3-1. {random.choice(glimt_spillere)} skyt så hardt at ballen eksplodere. {bortelag} tar bussen heim i skam."
        else:
            resultat = f"{bortelag} lede i pauså, men Glimt kjøre over dem i 2. omgang. Det ende 2-2 fordi dommeren va blind."

        return f"Neste kamp: {hjemmelag} mot {bortelag} ({dato}). {resultat}"

    except Exception as e:
        return f"Faen, æ fekk ikkje tak i kampdata: {e}"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""
    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(kw in spm for kw in ["kamp", "glimt", "fotball", "eliteserien", "rosenborg", "tromsø"]):
            if "neste" in spm or "resultat" in spm:
                spadom = hent_neste_glimt_kamp()
            else:
                spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
