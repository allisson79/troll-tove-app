import os
import random
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
TEAM_ID_GLIMT = 327

# Spådommer
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
    "Glimt vinn 2–1. Dommeren prøve å fucke det opp, men Pelle fikse biffen.",
    "Det blir 1–1. En jævla dommertabbe og et mål av Evjen redda æra.",
    "Faen ta, det her e kamp med krig. Glimt dreg det i land 3–2.",
    "0–0. Ingen mål, bare spark og banning. Tromsø burde fått rødt kort alle sammen."
]

glimt_spillere = [
    "Pellegrino", "Berg", "Saltnes", "Hauge", "Evjen", "Sjøvold", "Sørli", "Helmersen", "Haikin", "Bjørkan"
]


def neste_glimt_kamp():
    try:
        url = f"https://v3.football.api-sports.io/fixtures?team={TEAM_ID_GLIMT}&next=1"
        headers = {"x-apisports-key": API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        fixture = data["response"][0]["fixture"]
        teams = data["response"][0]["teams"]
        hjemmelag = teams["home"]["name"]
        bortelag = teams["away"]["name"]
        dato = fixture["date"][:10]  # YYYY-MM-DD

        glimt_hjemme = teams["home"]["id"] == TEAM_ID_GLIMT

        resultat = random.choice([
            "2–1", "3–2", "1–1", "4–0", "0–0", "2–2", "3–1", "1–0"
        ])
        målscorer = random.choice(glimt_spillere)

        svar = (
            f"Neste kamp: {hjemmelag} – {bortelag} ({dato}).\n"
            f"Troll-Tove spår resultatet blir {resultat}. Og {målscorer} smell inn ett som får publikum te å skrik av ekstase."
        )

        if not glimt_hjemme:
            svar += "\nDet blir krig på bortebane – men Glimt står han av."

        return svar
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

        if any(word in spm for word in ["kamp", "neste kamp", "glimt", "fotball", "score", "mål"]):
            spadom = neste_glimt_kamp()
        elif any(word in spm for word in ["kjærlighet", "elske", "forhold"]):
            spadom = random.choice(spaadommer_random)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)


if __name__ == "__main__":
    app.run(debug=True)
