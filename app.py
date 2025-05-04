from flask import Flask, render_template, request
import random
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

load_dotenv()

app = Flask(__name__)

brukerhistorikk = defaultdict(list)

spaadommer_random = [
    "Hvis du ikkje slutte å syt, så kjem en ravn og skit på jakka di.",
    "Du kjem te å finne lykken... i bunnpris-køa bak en som lukta svette og anger.",
    "En fremmed vil tilby dæ pølse. Si nei. Det e ikke kjøtt.",
    "Hold dæ unna IKEA i helga. Det e kaos, skriking og skilsmisser på gang.",
    "Du får snart en telefon... men det e bare mora di igjen.",
    "Torsdag blir en drittdag. Akkurat som forrige.",
    "Naboen din planlegg noe. Lås døra.",
    "Æ føle at strømregninga blir høyere enn lønna.",
    "Neste gang du går ut – se opp. Ikke spør hvorfor.",
    "Du får en pakke i posten. Du har ikke bestilt den. Ligg unna."
]

spaadommer_fotball = [
    "Glimt vinn 2-0. RBK kan gå og legg seg.",
    "Det bli 3-1 te Glimt. Tromsø får rødt kort og våte buksa.",
    "1-1, men det e faen så urettferdig. Dommeren e blind.",
    "4-0 Glimt. Motstanderen vurderer å legge ned laget.",
    "2-2 – og treneren te motstanderen får hjerteflimmer.",
    "5-1 Glimt. Pellegrino skyt så hardt at ballen går i bane rundt jorda.",
    "0-1 tap. Men det e fordi Glimt still med juniorlaget og dommeren e fra Trøndelag.",
    "3-2 Glimt. Publikum må få hjertestarter.",
    "2-0 Glimt. Tromsø får PTSD."
]

aktive_glimt_spillere = [
    "Julian Rekdahl Faye Lund", "Nikita Haikin", "Magnus Brøndbo",
    "Villads Schmidt Nielsen", "Odin Luraas Bjørtuft", "Haitam Aleesami",
    "Jostein Maurstad Gundersen", "Fredrik André Bjørkan", "Brede Mathias Moe",
    "Fredrik Sjøvold", "Patrick Berg", "Sondre Auklend", "Ulrik Saltnes",
    "Sondre Brunstad Fet", "Håkon Evjen", "Jeppe Kjær Jensen",
    "Kasper Waarts Thenza Høgh", "Jens Petter Hauge", "Ole Didrik Blomberg",
    "Andreas Klausen Helmersen", "Daniel Joshua Bassi Jakobsen", "Isak Dybvik Määttä",
    "Sondre Sørli", "Mikkel Bro Hansen"
]

intro = [
    "Hmm... la mæ føle litt på kraftan...",
    "Vent litt... æ må ta inn energian...",
    "Oooh... det her kjennes mørkt ut...",
    "Troll-Tove føle noe... skummelt..."
]

# Funksjon for å hente neste Glimt-kamp fra API

def hent_neste_glimt_kamp():
    try:
        api_key = os.getenv("API_FOOTBALL_KEY")
        headers = {"x-apisports-key": api_key}
        url = "https://v3.football.api-sports.io/fixtures?team=630&next=1"
        response = requests.get(url, headers=headers)
        data = response.json()

        kamp = data["response"][0]
        hjemmelag = kamp["teams"]["home"]["name"]
        bortelag = kamp["teams"]["away"]["name"]
        dato = kamp["fixture"]["date"]
        kamp_tid = datetime.strptime(dato, "%Y-%m-%dT%H:%M:%S%z")
        dato_str = kamp_tid.strftime("%A %d. %B kl %H:%M")

        glimt_hjemme = "Bodø/Glimt" in hjemmelag

        if glimt_hjemme:
            resultat = "3-1. Pellegrino skyt så hardt at ballen eksplodere. Motstanderen piss i shortsen."
        else:
            resultat = "2-2. Glimt e bedre, men dommeren har mørkeblå truse og dømme alt feil."

        return f"Neste kamp: {hjemmelag} – {bortelag}, {dato_str}. Resultattips: {resultat}"
    except Exception as e:
        return f"Faen, æ fekk ikkje tak i kampdata: {e}"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    bruker_ip = request.remote_addr

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if "glimt" in spm or "kamp" in spm or "resultat" in spm:
            forslag = hent_neste_glimt_kamp()
            if forslag not in brukerhistorikk[bruker_ip]:
                spadom = forslag
            else:
                spadom = random.choice(spaadommer_fotball)
        elif "fotball" in spm or "eliteserien" in spm:
            forslag = random.choice(spaadommer_fotball)
            if forslag not in brukerhistorikk[bruker_ip]:
                spadom = forslag
            else:
                spadom = random.choice(spaadommer_fotball)
        else:
            forslag = random.choice(spaadommer_random)
            if forslag not in brukerhistorikk[bruker_ip]:
                spadom = forslag
            else:
                spadom = random.choice(spaadommer_random)

        brukerhistorikk[bruker_ip].append(spadom)
        if len(brukerhistorikk[bruker_ip]) > 10:
            brukerhistorikk[bruker_ip] = brukerhistorikk[bruker_ip][-10:]

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
