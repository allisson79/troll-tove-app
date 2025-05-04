from flask import Flask, render\_template, request
import random
import requests
import os
from datetime import datetime

app = Flask(**name**)

# Glimt-spillere (kun fornavn)

spillere\_glimt = \[
"Julian", "Nikita", "Magnus",
"Villads", "Odin", "Haitam", "Jostein", "Fredrik", "Brede", "Sjøvold",
"Patrick", "Sondre", "Ulrik", "Fet", "Håkon", "Jeppe",
"Kasper", "Jens", "Ole", "Andreas", "Daniel", "Isak", "Sondre", "Mikkel"
]

# Spådommer for fotballkamper med formatert spillerplass

spaadommer\_fotball = \[
"{spiller} smell inn to mål og sende motstanderen heim i bleie.",
"{spiller} skyt så hardt at ballen må hentes på Rønvikjordene.",
"{spiller} fære i strupen på hele forsvaret og score hat-trick.",
"{spiller} knuse drømman te Rosenborg-supporteran med en hælspark i krysset.",
"{spiller} e så varm at stadion ta fyr – 2 mål og assist.",
"{spiller} dribla halve laget og legg inn til seg sjøl for scoring."
]

# Spådommer for annet

spaadommer\_random = \[
"Du kommer tell å trø på en Lego i natt.",
"Nån plan du har kommer tell å gå rett vest.",
"Hold kjeften din lukka i morra – ellers blir det bråk.",
"Pengene dine flyg som løvetannfrø i vinden.",
"Du får uventa besøk... og det lukta svette sokka."
]

intro = \[
"Satan i hælvette... æ ser et tegn!",
"Hmm... la mæ føle litt på kraftan...",
"Det lukta svette og faenskap... det blir et svar nu.",
"Ååå dæven... kortan mine danse.",
"Universet skrike – og æ høre det."
]

def hent\_neste\_glimt\_kamp():
url = "[https://v3.football.api-sports.io/fixtures](https://v3.football.api-sports.io/fixtures)"
headers = {"x-apisports-key": os.getenv("API\_FOOTBALL\_KEY")}
params = {
"team": 327,  # Bodø/Glimt sin ID
"next": 1
}

```
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data["response"]:
        return "⚠️ Klarte ikke å hente kampdata – det ser ut som det ikke er noen kommende kamper."

    kamp = data['response'][0]
    hjemmelag = kamp['teams']['home']['name']
    bortelag = kamp['teams']['away']['name']
    dato_str = kamp['fixture']['date']
    dato = datetime.fromisoformat(dato_str.replace("Z", "+00:00")).strftime("%A %d. %B kl %H:%M")

    glimt_hjemme = hjemmelag.lower() == "bodø/glimt"
    tilfeldig_spiller = random.choice(spillere_glimt)
    base = random.choice(spaadommer_fotball).format(spiller=tilfeldig_spiller)

    return f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {base}"

except Exception as e:
    return f"💀 Faen, æ fekk ikkje tak i kampdata: {str(e)} 💀"
```

@app.route("/", methods=\["GET", "POST"])
def troll\_tove():
spadom = ""
intro\_valg = ""
sporsmal = ""

```
if request.method == "POST":
    sporsmal = request.form["sporsmal"]
    intro_valg = random.choice(intro)
    spm = sporsmal.lower()

    if any(word in spm for word in ["kamp", "neste kamp", "score", "spiller", "glimt", "resultat"]):
        spadom = hent_neste_glimt_kamp()
    elif any(word in spm for word in ["glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"]):
        spiller = random.choice(spillere_glimt)
        spadom = random.choice(spaadommer_fotball).format(spiller=spiller)
    else:
        spadom = random.choice(spaadommer_random)

return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
```

if **name** == "**main**":
app.run(debug=True)
