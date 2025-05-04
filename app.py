from flask import Flask, render\_template, request
import random
import requests
import os
from datetime import datetime
from dotenv import load\_dotenv

load\_dotenv()

app = Flask(**name**)

API\_KEY = os.getenv("API\_FOOTBALL\_KEY")
TEAM\_ID = 327

spillere\_glimt = \[
"Nikita", "Marius", "Fredrik", "Omar", "Brede", "Albert", "Patrick",
"Ulrik", "Runar", "Daniel", "Nino", "Lucas", "Sondre", "Ola",
"Noah", "Bjørkan", "Faris", "Jens", "Amahl", "Isak"
]

spaadommer\_fotball = \[
"⚽️ Det lukta mål av {spiller} – han smell inn to i krysset!",
"🔥 {spiller} e i fyr og flamme – hat-trick coming up!",
"💩 Tja... {spiller} bomme på åpent mål, men score gjør han!",
"🧙 {spiller} har sett inn i kula – og der va det mål!",
"💀 Ingen tvil, {spiller} ordne biffen – én i nota minst!",
"🤯 {spiller} skal visst stå i mål... men scora gjør han lell!",
"💫 Det blir en magisk kveld for {spiller} – mål og målgivende!",
"👟 {spiller} skyt fra 40 meter – og den går inn!",
"🟡⚫️ {spiller} e Glimt sin frelser – mål i 89. minutt!",
"🐙 {spiller} dukke opp overalt – og selvfølgelig score han og!"
]

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
```

@app.route("/")
def index():
return render\_template("index.html")

@app.route("/glimt", methods=\["POST"])
def glimt():
try:
melding = hent\_neste\_glimt\_kamp()
except Exception as e:
melding = f"💀 Faen, æ fekk ikkje tak i kampdata: {e} 💀"
return render\_template("index.html", svar=melding)

if **name** == "**main**":
app.run(debug=True)
