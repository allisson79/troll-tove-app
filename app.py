from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
from datetime import datetime
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

ip_cache = {}
API_KEY = os.getenv("API_FOOTBALL_KEY")
TEAM_ID = 5412
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

# Last inn spådommer fra fil
def load_predictions(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return []

fotball_spaadommer = load_predictions("spaadommer_fotball.txt")
tull_spaadommer = load_predictions("spaadommer_random.txt")
alle_spaadommer = fotball_spaadommer + tull_spaadommer

def generate_prediction(sporsmal):
    sporsmal = sporsmal.lower()

    if "glimt" in sporsmal or "kamp" in sporsmal:
        if fotball_spaadommer:
            return random.choice(fotball_spaadommer)
    return random.choice(alle_spaadommer) if alle_spaadommer else "Æ har faen ikke noe å si te dæ akkurat no."

@app.route("/", methods=["GET", "POST"])
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_key = str(ip_address(user_ip.split(",")[0].strip()))

    if request.method == "POST":
        navn = request.form.get("navn", "ukjent tosk")
        sporsmal = request.form.get("sporsmal", "").strip()

        if ip_key in ip_cache:
            spadom = ip_cache[ip_key]
        else:
            spadom = generate_prediction(sporsmal)
            ip_cache[ip_key] = spadom

        intro = f"Hør hør, {navn}! Troll-Tove har kikka i kula si…"

        return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

    return render_template("index.html")

