from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
import requests
from datetime import datetime
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

# Caching spådommer basert på IP
ip_cache = {}

# Ekte kampdata (API-Football)
API_KEY = os.getenv("API_FOOTBALL_KEY")
TEAM_ID = 5412  # Bodø/Glimt sitt ID i APIet
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

# 30 unike spådommer (15 fotball, 15 tull)
predictions = [
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
    "En supporter stormer banen og stjeler showet.",
    "Du kommer til å bli svett i ræva av å følge med.",
    "Spill ei tippekupong – men ikke stol på meg.",
    "Stjerna i dag blir en du aldri har hørt om før.",
    "Det blir VAR-helvete og 7 minutter tilleggstid.",
    "Sola skinner, men spillet blir grått som november.",
    "Du burde egentlig sett kampen hjemme med øl i handa.",
    "Motstanderen scorer selvmål. Karma, din jævel!",
    "Glimt vinner på overtid. Det blir hyl og skrik i stua.",
    "En ball går over taket på stadion. Den ser du aldri igjen.",
    "Bortefansen klikker og begynner å hive pølser på banen.",
    "Kommentatoren mister stemmen av rein begeistring.",
    "Kampen blir historisk – på godt eller vondt.",
    "Alle byttene til Glimt funker som faen. Magi.",
    "Du vinner ikke tippinga i dag, bare gi opp.",
    "En katt springer over banen og stopper spillet."
]

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_key = str(ip_address(user_ip.split(",")[0].strip()))

    if request.method == "POST":
        if ip_key in ip_cache:
            prediction = ip_cache[ip_key]
        else:
            prediction = random.choice(predictions)
            ip_cache[ip_key] = prediction

        return render_template("result.html", prediction=prediction)

    return render_template("index.html")
