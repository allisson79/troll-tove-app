from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
import requests
from datetime import datetime
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

# Caching spådommer basert på IP og modus
ip_cache = {}

# Ekte kampdata (API-Football)
API_KEY = os.getenv("API_FOOTBALL_KEY")
TEAM_ID = 5412  # Bodø/Glimt sitt ID i APIet
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

# 30 unike spådommer (15 fotball, 15 tull)
fotball_spaadommer = [
    "Glimt vinner 3-1, og Saltnes scorer fra 30 meter!",
    "Det blir tap i dag, 2-0. Dårlig dag på jobben.",
    "Kampen blir avlyst. For mye vind på Aspmyra.",
    "Glimt knuser motstanderen 5-0. Helvete heller!",
    "En eller annen idiot får rødt kort – ikke bli overraska.",
    "3-3 og et latterlig straffedrama på slutten.",
    "Kampen blir 0-0. Folk går hjem og angrer på billetten.",
    "Dommeren ødelegger alt. Som vanlig.",
    "Glimt scorer i første minutt og parkerer bussen etterpå.",
    "Salvesen putter hat-trick, alle på hodet.",
    "Motstanderen får mål annullert – og det blir ramaskrik.",
    "Keeperen gjør en tabbe. Du kommer til å banne høyt.",
    "Ulrik Saltnes blir banens beste, selv om han starter på benken.",
    "Glimt bommer på straffe. Igjen.",
    "En supporter stormer banen og stjeler showet."
]

random_spaadommer = [
    "Du kommer til å søle kaffe på skjorta rett før et viktig møte.",
    "Snart skjer det noe som får dæ til å rope «FAEN I HELVETTE» – på et kjøpesenter.",
    "Hold deg unna diskusjoner i dag – spesielt med svigermor.",
    "Internett ditt kommer til å kollapse akkurat når du trenger det.",
    "Noen kommer til å spørre deg om noe idiotisk, og du må smile.",
    "Du finner igjen noe du har lett etter i ukesvis – i lomma.",
    "Dagen starter rævva, men ender med kake. Helt sant.",
    "Noen prøver å imponere deg, og feiler spektakulært.",
    "Du burde ikke stole på Google Maps i dag.",
    "Du kommer til å si noe kleint i et møte – og angre i evighet.",
    "Du får en ny idé som enten blir genial – eller full krise.",
    "Gjør deg klar for en uventa regnskur og dårlig hårdag.",
    "I dag er ikke dagen for å satse på lotto – stol på Tove.",
    "En fremmed kommer til å gi deg et blikk du aldri glemmer.",
    "En liten ting i dag blir mye større enn den burde – hold kjeft og smil."
]

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_key = str(ip_address(user_ip.split(",")[0].strip()))
    modus = None
    prediction = None

    if request.method == "POST":
        modus = request.form.get("modus")

        if ip_key in ip_cache and ip_cache[ip_key].get(modus):
            prediction = ip_cache[ip_key][modus]
        else:
            if modus == "glimt":
                prediction = random.choice(fotball_spaadommer)
            elif modus == "random":
                prediction = random.choice(random_spaadommer)
            else:
                prediction = random.choice(fotball_spaadommer + random_spaadommer)

            if ip_key not in ip_cache:
                ip_cache[ip_key] = {}
            ip_cache[ip_key][modus] = prediction

        navn = request.form.get("navn", "").strip()
        sporsmal = request.form.get("sporsmal", "").strip()

        return render_template(
            "result.html",
            prediction=prediction,
            navn=navn,
            sporsmal=sporsmal,
            intro="Hør hør, Thomas! Troll-Tove har kikka i kula si…",
            modus=modus
        )

    return render_template("index.html")
