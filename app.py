from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

# Caching spådommer basert på IP
ip_cache = {}

# Last spådommer fra filer
def last_spaadommer(filnavn):
    with open(filnavn, "r", encoding="utf-8") as f:
        return [linje.strip() for linje in f if linje.strip()]

fotball_spaadommer = last_spaadommer("spaadommer_fotball.txt")
random_spaadommer = last_spaadommer("spaadommer_random.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        navn = request.form.get("navn", "Du")
        sporsmal = request.form.get("sporsmal", "")
        user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip_key = str(ip_address(user_ip.split(",")[0].strip()))

        if ip_key in ip_cache:
            spadom = ip_cache[ip_key]
        else:
            spadom = random.choice(fotball_spaadommer + random_spaadommer)
            ip_cache[ip_key] = spadom

        intro = f"Hør hør, {navn}! Troll-Tove har kikka i kula si…"
        return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

    return render_template("index.html")

@app.route("/glimtmodus", methods=["GET"])
def glimtmodus():
    navn = "du jævel"
    sporsmal = "Hvordan går det med Glimt?"
    spadom = random.choice(fotball_spaadommer)
    intro = f"Hør hør, {navn.title()}! Troll-Tove har sett lyset fra Aspmyra…"
    return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

@app.route("/darkmodus", methods=["GET"])
def darkmodus():
    navn = "kompis"
    sporsmal = "Hva bringer mørket?"
    spadom = random.choice(random_spaadommer)
    intro = f"Mørke skyer samler seg, {navn}… Troll-Tove ser noe dystert i horisonten."
    return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

if __name__ == "__main__":
    app.run(debug=True)
