import os
import json
import random
import hashlib
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
TEAM_ID = 327
USED_PREDICTIONS_FILE = "used_predictions.json"

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

spaadommer_fotball = [
    "Glimt maler ned motstand som møkk under skoen – det blir 3-1.",
    "Det her e en kamp Glimt bare SKAL vinne – 2-0 og heim med skam for motstanderen.",
    "Dommern kommer te å være blind, men Glimt vinn 1-0 likevel.",
    "Æ ser mål... masse mål... og Glimt vinn 4-2."
]

spillere_glimt = [
    "Julian Faye Lund", "Nikita Haikin", "Magnus Brøndbo", "Villads Nielsen",
    "Odin Bjørtuft", "Haitam Aleesami", "Jostein Gundersen", "Fredrik Bjørkan",
    "Brede Moe", "Fredrik Sjøvold", "Patrick Berg", "Sondre Auklend",
    "Ulrik Saltnes", "Sondre Fet", "Håkon Evjen", "Jeppe Kjær",
    "Kasper Høgh", "Jens Petter Hauge", "Ole Didrik Blomberg",
    "Andreas Helmersen", "Daniel Bassi", "Isak Määttä", "Sondre Sørli",
    "Mikkel Hansen"
]

intro = [
    "Hmm... la mæ føle litt på kraftan...",
    "Vent no litt... æ må ta inn energian...",
    "Oooh... det her kjennes mørkt ut...",
    "Troll-Tove føle noe... skummelt..."
]

def get_user_hash(ip, question):
    return hashlib.sha256(f"{ip}-{question}".encode()).hexdigest()

def load_used_predictions():
    if os.path.exists(USED_PREDICTIONS_FILE):
        with open(USED_PREDICTIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_used_predictions(data):
    with open(USED_PREDICTIONS_FILE, 'w') as f:
        json.dump(data, f)

def get_unique_prediction(category_list, user_hash, used_data):
    used = used_data.get(user_hash, [])
    unused = [s for s in category_list if s not in used]
    if not unused:
        used_data[user_hash] = []
        unused = category_list.copy()
    choice = random.choice(unused)
    used_data.setdefault(user_hash, []).append(choice)
    return choice

def hent_neste_glimt_kamp():
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?team={TEAM_ID}&next=1"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        kamp = data['response'][0]['fixture']
        motstander = data['response'][0]['teams']['away']['name'] if data['response'][0]['teams']['home']['id'] == TEAM_ID else data['response'][0]['teams']['home']['name']
        hjemme = data['response'][0]['teams']['home']['id'] == TEAM_ID
        dato = kamp['date'][:10]
        resultat = random.choice(["2-1", "3-1", "4-2", "1-0", "3-2", "5-1"])
        målscorer = random.choice(spillere_glimt)
        sidekommentar = random.choice([
            "dommern e faen ikkje edru.",
            "supporteran til motstanderan går heim i stillhet.",
            "æ ser rødt kort og banning.",
            "det blir drama og jævelskap."
        ])
        return f"Neste kamp mot {motstander} ({'hjemme' if hjemme else 'borte'}) {dato}. Glimt vinn {resultat} – og {målscorer} banka inn minst ett. Og {sidekommentar}"
    except Exception as e:
        return f"Faen, æ fekk ikkje tak i kampdata: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = random.choice(intro)
    sporsmal = ""
    used_data = load_used_predictions()

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        user_ip = request.remote_addr or "anon"
        user_hash = get_user_hash(user_ip, sporsmal)
        spm = sporsmal.lower()

        if any(word in spm for word in ["kamp", "glimt", "score", "mål", "vinner"]):
            if "neste kamp" in spm or "hvem møter" in spm:
                spadom = hent_neste_glimt_kamp()
            else:
                spadom = get_unique_prediction(spaadommer_fotball, user_hash, used_data)
        else:
            spadom = get_unique_prediction(spaadommer_random, user_hash, used_data)

        save_used_predictions(used_data)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
