from flask import Flask, render_template, request
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_FOOTBALL_KEY")

def neste_glimt_kamp():
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    url = "https://v3.football.api-sports.io/fixtures?team=971&next=1"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        kamp = data["response"][0]

        hjemmelag = kamp["teams"]["home"]["name"]
        bortelag = kamp["teams"]["away"]["name"]
        dato = kamp["fixture"]["date"][:10]

        glimt_hjemme = hjemmelag.lower() == "bodø/glimt"

        if glimt_hjemme:
            resultat = "Glimt vinn 3–1. Tottenham kan pelle sæ tilbake te puben med halen mellom beina."
        else:
            resultat = "Borte? Jada, 2–2. Men bare fordi dommeren e fette blind og TIL hadde flaks."

        return f"Neste kamp: {hjemmelag} – {bortelag}, {dato}. {resultat}"

    except Exception as e:
        return f"Faen, æ fekk ikkje tak i kampdata: {e}"

intro = [
    "La mæ føle på universet, din stakkars jævel...",
    "Hold kjeften din – æ må konsentrere mæ...",
    "Troll-Tove kjenne mørke energia – og flatfyll i lufta...",
    "Satan i hælvette... æ ser et tegn!"
]

spaadommer_random = [
    "Det kjem til å gå til helvete. Men det e greit.",
    "IKEA neste uke? Hold dæ unna, det blir kaos og blod.",
    "Du møte en idiot med caps. Styr unna. Det blir bråk.",
    "Æ ser... ingenting. Og det e faktisk et faresignal."
]

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if "glimt" in spm or "kamp" in spm or "neste kamp" in spm or "tromsø" in spm or "rosenborg" in spm:
            spadom = neste_glimt_kamp()
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
