# Eksempel på oppdatert app.py med IP-logging og unike spådommer
from flask import Flask, render_template, request
import random
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Last IP-logg
ip_logg_fil = "ip_logg.json"
if os.path.exists(ip_logg_fil):
    with open(ip_logg_fil, "r") as f:
        ip_logg = json.load(f)
else:
    ip_logg = {}

# Eksempelspådommer
spaandommer_fotball = [
    "Glimt knuse dritten ut av motstanderen. 3–0, og det med ei hand bak ryggen.",
    "Det blir 2‒1 te Glimt. Dommeren grine seg hjem."
]

spaandommer_random = [
    "IKEA blir å gi deg traumer på tirsdag. Hold deg unna flatpakka."
]

# Logg spådom for IP

def logg_spadom(ip, spadom):
    if ip not in ip_logg:
        ip_logg[ip] = []
    if spadom not in ip_logg[ip]:
        ip_logg[ip].append(spadom)
        with open(ip_logg_fil, "w") as f:
            json.dump(ip_logg, f)

# Finn en unik spådom

def unik_spadom(ip, spadomliste):
    tidligere = set(ip_logg.get(ip, []))
    valg = [s for s in spadomliste if s not in tidligere]
    return random.choice(valg) if valg else random.choice(spadomliste)

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    sporsmal = ""
    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        ip = request.remote_addr
        spm = sporsmal.lower()

        if "glimt" in spm or "kamp" in spm or "fotball" in spm:
            spadom = unik_spadom(ip, spaandommer_fotball)
        else:
            spadom = unik_spadom(ip, spaandommer_random)

        logg_spadom(ip, spadom)

    return render_template("index.html", spadom=spadom, sporsmal=sporsmal)

if __name__ == "__main__":
    app.run(debug=True)
