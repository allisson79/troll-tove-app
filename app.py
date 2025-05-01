import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

app = Flask(__name__)

intro = [
    "Universet skrike – og æ høre det.",
    "Æ riste runene og slår i bordet – no kommer det.",
    "Faen steike... æ må konsentrere mæ. Spør igjen.",
    "Det lukta svette og faenskap... det blir et svar nu."
]

spaadommer_random = [
    "Du kjem te å få regning i posten og en ravn i hagen. Tegn e tegn.",
    "Hold dæ unna IKEA i helga. Det blir blod og flatpakka sorg.",
    "Æ ser en fremmed med potetgull... Si ja. Det e skjebnen som snakke.",
    "Hvis du går med caps på torsdag, så e du føkt."
]

def neste_glimt_kamp():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "team": 2669,  # Bodø/Glimt
        "next": 1
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        kamp = data["response"][0]
        hjemmelag = kamp["teams"]["home"]["name"]
        bortelag = kamp["teams"]["away"]["name"]
        dato = kamp["fixture"]["date"][:10]  # YYYY-MM-DD

        glimt_hjemme = "glimt" in hjemmelag.lower()

        if glimt_hjemme:
            resultat = "Glimt vinn 3–1. Pellegrino skyt så hardt at ballen eksplodere. Motstanderen reise heim i stillhet."
        else:
            resultat = "Borte mot %s... det lukte 2–2 og en dommer som burde vært på NAV." % bortelag

        return f"Neste kamp: {hjemmelag} – {bortelag}, {dato}. {resultat}"

    except Exception as e:
        return f"💀 Faen, æ fekk ikkje tak i kampdata: {e} 💀"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "bodø/glimt", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk", "tottenham", "kamp"]):
            if any(x in spm for x in ["neste kamp", "hvem møter", "når", "spiller"]):
                spadom = neste_glimt_kamp()
            else:
                hjemmemål = random.randint(1, 4)
                bortemål = random.randint(0, hjemmemål - 1)
                spadom = f"Glimt vinn {hjemmemål}-{bortemål}. Jævlige tilstander for motstanderen – dem får psykolog etter kampen."
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
