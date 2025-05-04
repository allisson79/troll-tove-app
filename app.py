from flask import Flask, render_template, request
import os
import random
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "v3.football.api-sports.io"

intro = [
    "Universet skrike – og æ høre det.",
    "Det lukta svette og faenskap... det blir et svar nu.",
    "Æ føle mørke krefter røre på seg – og dem rope om fotball.",
    "Det e kamp i lufta, og æ kjenne lukta av seier... eller faen og tap."
]

spaadommer_fotball = [
    "Glimt har form. Resten av Eliteserien har bare flaks og mødre som trur på dem.",
    "Rosenborg? Hah! Glimt vinn som vanlig. Det e faen meg ikke kamp, det e slakt.",
    "Tromsø kjem med håp, men går heim med ræva full av skam.",
    "Molde prøvde. Glimt svarte med mål og banning."
]

spaadommer_random = [
    "Æ ser at du burde hold dæ inne på torsdag. Dårlig karma og dårlig vær.",
    "Det blir en jævlig dag, men du overleve – trur æ.",
    "Hvis du møte en med caps bakfram – spring.",
    "Spis potetgull. Det e kanskje det eneste som går bra i dag."
]

def hent_neste_glimt_kamp():
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {
            "x-apisports-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }
        params = {
            "team": 271,  # Bodø/Glimt sin ID i APIet
            "next": 1
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        kamp = data["response"][0]["fixture"]
        hjemmelag = data["response"][0]["teams"]["home"]["name"]
        bortelag = data["response"][0]["teams"]["away"]["name"]
        tidspunkt = kamp["date"][:16].replace("T", " ")

        glimt_hjemme = hjemmelag.lower() == "bodø / glimt" or "glimt" in hjemmelag.lower()

        if glimt_hjemme:
            resultat = "3–1 te Glimt. Dem skyt så hardt at målet må repareres."
        else:
            resultat = "2–2. Dommeren e fette blind, og Glimt blir rana."

        return f"Neste kamp: {hjemmelag} – {bortelag}, {tidspunkt}. {resultat}"

    except Exception as e:
        return f"Faen, æ fekk ikkje tak i kampdata: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""
    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "bodø", "kamp", "neste kamp", "fotball", "eliteserien"]):
            spadom = hent_neste_glimt_kamp()
        elif any(word in spm for word in ["rosenborg", "rbk", "molde", "tromsø", "til"]):
            spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
