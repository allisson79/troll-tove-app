import os
import random
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)

# Midlertidig cache for IP og forrige svar
ip_cache = {}

API_KEY = os.getenv("FOOTBALL_API_KEY")
TEAM_ID = 327  # Bodø/Glimt sin ID i API-FOOTBALL

spillere_glimt = [
    "Julian", "Nikita", "Magnus", "Villads", "Odin", "Haitam", "Jostein",
    "Fredrik", "Brede", "Patrick", "Sondre", "Ulrik", "Håkon", "Jeppe",
    "Kasper", "Jens", "Ole", "Andreas", "Daniel", "Isak", "Sondre", "Mikkel"
]

spaadommer_fotball = [
    "{spiller} smell inn en suser fra 25 meter – keeperen renn heim til mora si.",
    "{spiller} blir matchvinner – og hele jævla Tromsø hyle i skam.",
    "Rosenborg ryke som vanlig, {spiller} danse på ruinan deres.",
    "{spiller} score hat-trick – og dommeren besvime av ærefrykt.",
    "Molde får smake ræv – {spiller} ordne opp som vanlig.",
    "{spiller} smell inn vinnermålet på overtid. Publikum gå amok."
]

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

intro = [
    "Hmm... la mæ føle litt på kraftan...",
    "Vent no litt... æ må ta inn energian...",
    "Oooh... det her kjennes mørkt ut...",
    "Troll-Tove føle noe... skummelt..."
]


def hent_neste_glimt_kamp():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {
        "team": TEAM_ID,
        "next": 1
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    kamp = data['response'][0]
    hjemmelag = kamp['teams']['home']['name']
    bortelag = kamp['teams']['away']['name']
    dato_str = kamp['fixture']['date']
    dato = datetime.fromisoformat(dato_str.replace("Z", "+00:00")).strftime("%A %d. %B kl %H:%M")

    glimt_hjemme = hjemmelag.lower() == "bodø/glimt"
    tilfeldig_spiller = random.choice(spillere_glimt)
    base = random.choice(spaadommer_fotball).format(spiller=tilfeldig_spiller)

    resultat = f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {base}"
    return resultat


def hent_unikt_spadom(ip, sporsmal):
    if any(ord in sporsmal.lower() for ord in ["glimt", "kamp", "eliteserien", "score"]):
        kandidat = hent_neste_glimt_kamp()
    else:
        kandidat = random.choice(spaadommer_random)

    forrige = ip_cache.get(ip)
    while kandidat == forrige:
        kandidat = random.choice(spaadommer_random)

    ip_cache[ip] = kandidat
    return kandidat


@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        ip = request.remote_addr
        intro_valg = random.choice(intro)

        try:
            spadom = hent_unikt_spadom(ip, sporsmal)
        except Exception as e:
            spadom = f"Faen, æ fekk ikkje tak i kampdata: {str(e)}"

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)


if __name__ == "__main__":
    app.run(debug=True)
