from flask import Flask, render_template, request
import random
import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Spådombanker
spaadommer_fotball = [
    "Glimt vinn 2–1. Hauge legg opp, og Høgh banka inn vinnermålet med ræva.",
    "3–0 te Glimt. Keeperen tel motstanderlaget begynne å grine. Heile laget gir opp og begynne å søke NAV.",
    "Det blir 1–1. Dommeren e fra Trøndelag, så det blir jævla urettferdig.",
    "2–2. Saltnes skrik på dommeren, men det hjelpe faen ikkje. Motstanderen får straffe uten grunn.",
    "4–1 te Glimt. Pellegrino skyt så hardt at ballen går gjennom nettet og treff en supporter i trynet. Han takke for opplevelsen."
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

# Sti til fil for spådommer som allerede er gitt
USED_PREDICTIONS_FILE = "used_predictions.json"

def get_client_ip():
    return request.remote_addr or "unknown"

def load_used_predictions():
    if os.path.exists(USED_PREDICTIONS_FILE):
        with open(USED_PREDICTIONS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_used_predictions(data):
    with open(USED_PREDICTIONS_FILE, "w") as file:
        json.dump(data, file)

def get_unique_prediction(ip, predictions):
    used = load_used_predictions()
    user_used = used.get(ip, [])
    available = [p for p in predictions if p not in user_used]

    if not available:
        # Hvis alt er brukt, start på nytt
        available = predictions
        user_used = []

    prediction = random.choice(available)
    user_used.append(prediction)
    used[ip] = user_used
    save_used_predictions(used)
    return prediction

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""
    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        ip = get_client_ip()
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "fotball", "kamp", "score", "mål", "eliteserien"]):
            spadom = get_unique_prediction(ip, spaadommer_fotball)
        else:
            spadom = get_unique_prediction(ip, spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
