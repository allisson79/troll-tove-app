from flask import Flask, render\_template, request
from dotenv import load\_dotenv
import os
import random
import requests
from datetime import datetime
from collections import defaultdict

load\_dotenv()

app = Flask(**name**)

API\_KEY = os.getenv("API\_KEY")
TEAM\_ID = 327  # Bodø/Glimt sin ID

spillere\_glimt = \[
"Julian", "Nikita", "Magnus", "Villads", "Odin", "Haitam", "Jostein",
"Fredrik", "Brede", "Patrick", "Sondre", "Ulrik", "Jeppe", "Håkon",
"Kasper", "Jens", "Ole", "Andreas", "Daniel", "Isak", "Mikkel"
]

spaadommer\_fotball = \[
"{spiller} smell inn et mål fra 30 meter.",
"{spiller} sklitakle ballen i mål – og dommern dømme straffe!",
"{spiller} score me ræva, men mål e mål.",
"Det e klart som faen – {spiller} sett den i krysset.",
"{spiller} bombe, men så kommer returen og da e det ingen nåde.",
"{spiller} står rett – og bare prikke inn seiersmålet.",
"{spiller} e i fyr og flamme – minst to mål!",
"Publikum rope på {spiller} – og han levere."
]

spaadommer\_annet = \[
"Du burde hold kjeft neste møte – universet advare.",
"Kjærligheta blomstre... men kanskje ikke for dæ.",
"Peng får du, men regningan spring fortere.",
"Du vinne i Lotto – men miste lappen samme uka.",
"Hold dæ unna fisk idag, det blir bare bein.",
"Nån sladre om dæ. Kanskje ho Linda fra regnskap?",
"Det blir en dag med motvind. I alle retninga.",
"Gammel flamme tar kontakt. Bruk brannslukkingsapparat."
]

ip\_logg = defaultdict(set)

def hent\_neste\_glimt\_kamp():
url = "[https://v3.football.api-sports.io/fixtures](https://v3.football.api-sports.io/fixtures)"
headers = {"x-apisports-key": API\_KEY}
params = {
"team": TEAM\_ID,
"next": 1
}
response = requests.get(url, headers=headers, params=params)
data = response.json()

```
try:
    kamp = data['response'][0]
    hjemmelag = kamp['teams']['home']['name']
    bortelag = kamp['teams']['away']['name']
    dato_str = kamp['fixture']['date']
    dato = datetime.fromisoformat(dato_str.replace("Z", "+00:00")).strftime("%A %d. %B kl %H:%M")

    glimt_hjemme = hjemmelag.lower() == "bodø/glimt"
    tilfeldig_spiller = random.choice(spillere_glimt)
    base = random.choice(spaadommer_fotball).format(spiller=tilfeldig_spiller)

    resultat = f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {base}"
    return resultat

except (IndexError, KeyError):
    return "Faen, æ fekk ikkje tak i kampdata: list index out of range"
```

def generer\_spaadom(sporsmal, bruker\_ip):
sporsmal\_lower = sporsmal.lower()

```
if bruker_ip in ip_logg and sporsmal in ip_logg[bruker_ip]:
    return "Du har spurt det der før, din nysgjerrige jævel. Prøv på nytt med nåkka annet."

ip_logg[bruker_ip].add(sporsmal)

if any(ord for ord in ["glimt", "bodø", "score", "mål", "kamp"] if ord in sporsmal_lower):
    return hent_neste_glimt_kamp()
else:
    return random.choice(spaadommer_annet)
```

@app.route('/', methods=\['GET', 'POST'])
def index():
spadom = None
sporsmal = None
if request.method == 'POST':
navn = request.form\['navn']
sporsmal = request.form\['sporsmal']
bruker\_ip = request.remote\_addr
spadom = generer\_spaadom(sporsmal, bruker\_ip)
return render\_template('index.html', spadom=spadom, sporsmal=sporsmal)

if **name** == '**main**':
app.run(debug=True)
