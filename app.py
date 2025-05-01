import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

app = Flask(__name__)

intro = [
    "Satan i hælvette... æ ser et tegn!",
    "Universet skrike – og æ høre det.",
    "Hold kjeften og lytt, offerlam...",
    "Æ føle det på rynkan mine... nå skjer det faenskap."
]

spaadommer_random = [
    "Torsdag blir en jævla dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

spaadommer_fotball = [
    "RBK e ræv. Glimt kjøre over dem som en jævla dampveivals.",
    "Tromsø? Nei, det e som å spille mot en barnehage full av blinde unger.",
    "Glimt har form. Resten av Eliteserien har bare flaks og mødre som trur på dem.",
    "Æ ser 2 mål fra Glimt og en keeper som gråte i dusjen etterpå.",
    "Dommern prøve å saboter, men Glimt vinn læll. Karma, din jævel."
]

def neste_glimt_kamp():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "team": 2619,  # Bodø/Glimt
        "next": 1
    }

    response = requests.get(url, headers=headers, params=params)

    try:
        data = response.json()
        fixtures = data.get("response", [])
        if not fixtures:
            return "Ingen jævla kampdata funnet – kanskje APIet e drita, eller Glimt tar pause for å spare på kreftan."

        kamp = fixtures[0]
        hjemmelag = kamp["teams"]["home"]["name"]
        bortelag = kamp["teams"]["away"]["name"]
        dato = kamp["fixture"]["date"]

        glimt_hjemme = "Bodø/Glimt" in hjemmelag
        if glimt_hjemme:
            resultat = "Glimt vinn 3–1. Pellegrino skyt så hardt at bortelaget får PTSD."
        else:
            resultat = "Borte? Det bli 2–2 og dommern e føkka i høvet som vanlig."

        return f"Neste kamp: {hjemmelag} – {bortelag}, {dato[:10]}. {resultat}"

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

        if any(word in spm for word in ["glimt", "kamp", "neste kamp", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk", "tottenham"]):
            if "neste kamp" in spm or "når" in spm or "møter" in spm:
                spadom = neste_glimt_kamp()
            else:
                spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
