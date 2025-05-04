from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

# Caching spådommer basert på IP
ip_cache = {}

# Last inn spådommer fra filer
with open("spaadommer_fotball.txt", encoding="utf-8") as f:
    football_predictions = [line.strip() for line in f if line.strip()]

with open("spaadommer_random.txt", encoding="utf-8") as f:
    random_predictions = [line.strip() for line in f if line.strip()]

# Enkle fotballnøkkelord for å avgjøre type spørsmål
fotballord = ["glimt", "kamp", "score", "scorer", "mål", "saltnes", "spill", "fotball", "aspmyra"]

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_key = str(ip_address(user_ip.split(",")[0].strip()))

    if request.method == "POST":
        sporsmal = request.form.get("sporsmal", "")
        navn = request.form.get("navn", "Din idiot")

        if ip_key in ip_cache:
            prediction = ip_cache[ip_key]
        else:
            lavere_sporsmal = sporsmal.lower()
            if any(ord in lavere_sporsmal for ord in fotballord):
                prediction = random.choice(football_predictions)
            else:
                prediction = random.choice(random_predictions)
            ip_cache[ip_key] = prediction

        intro = f"Hør hør, {navn}! Troll-Tove har kikka i kula si…"
        return render_template("result.html", spadom=prediction, sporsmal=sporsmal, intro=intro)

    return render_template("index.html")
