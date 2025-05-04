from flask import Flask, render\_template, request
import random
import requests
from datetime import datetime
from dotenv import load\_dotenv
import os

load\_dotenv()

app = Flask(**name**)

API\_KEY = os.getenv("API\_KEY")
TEAM\_ID = 327

spillere\_glimt = \[
"Julian", "Nikita", "Magnus", "Villads", "Odin", "Haitam", "Jostein", "Fredrik", "Brede", "Sjøvold",
"Patrick", "Sondre", "Ulrik", "Fet", "Håkon", "Jeppe", "Kasper", "Jens", "Ole", "Andreas", "Daniel", "Isak", "Sondre", "Mikkel"
]

spaadommer\_ekte = \[
"Det ser mørkt ut for deg, kompis.",
"Æ ser en storm i horisonten – hold deg fast!",
"Kjærligheta di går snart på ræva, dessverre.",
"Peng har du aldri hatt, og det blir ikke bedre.",
"Du kjem tel å vinne i Lotto... hvis du faktisk leverer kupong.",
"Nån kjem tel å irritere dæ kraftig i dag – mest sannsynlig en tromsøværing.",
"Du må slutte å spørre dumt – æ e spåkone, ikke psykolog.",
"Æ føle en energi... men det e bare kaffegruten som bobla.",
"Det blir en ræva dag, sånn e det bare.",
"Stol ikke på folk som hete Ronny i dag."
]

spaadommer\_fotball = \[
"{spiller} smell inn en rakett i krysset!",
"Det blir selvmål av {spiller}, men Glimt vinn likevel!",
"{spiller} får rødt kort for å sparke en tromsøværing i skrittet.",
"To mål av {spiller} og ett fra dommern – Glimt vinn!",
"{spiller} bomme på straffe, men scora i det 89. minutt.",
"Et innlegg fra {spiller} går rett i mål. Ingen skjønne ka som skjedde.",
"{spiller} heade inn vinnermålet med ræva.",
"Dommeren blåse feil vei, men {spiller} tar saken i egne hender.",
"{spiller} scora hat-trick – og æ så det komme!",
"Kampens helt? {spiller}, uten tvil.",
"{spiller} tar et brassespark som får Aspmyra til å eksplodere.",
"Det blir 5-0, og {spiller} står bak alt.",
"{spiller} spelle som om det sto om livet – og det gjør det jo nesten.",
"Ingen forstår hvordan {spiller} gjorde det, men målet sto det.",
"Glimt tar seieren, takket være {spiller} sin magi.",
"Et frispark fra {spiller} går rett i nettet – rett og slett nydelig.",
"{spiller} gjør det ingen trodde var mulig.",
"Kampen blir avgjort av et hælspark fra {spiller}.",
"{spiller} løpe som et udyr og får betalt for det.",
"Selv Tottenham skjelv når {spiller} nærme sæ sekstenmeteren."
]

ip\_logg = {}

@app.route("/", methods=\["GET", "POST"])
def index():
spadom = None
sporsmal = None
ip = request.remote\_addr

```
if request.method == "POST":
    navn = request.form["navn"].strip().lower()
    sporsmal = request.form["sporsmal"].strip().lower()

    if ip in ip_logg and ip_logg[ip] == sporsmal:
        spadom = "Du har allerede spurt om det der, din gjøk. Prøv noe nytt."
    else:
        if "glimt" in sporsmal or "score" in sporsmal:
            spadom = hent_neste_glimt_kamp()
        elif any(ord in sporsmal for ord in ["vinne", "dø", "kone", "jobb", "barn", "vær", "sex", "pæng", "tromsø"]):
            spadom = random.choice(spaadommer_ekte)
        else:
            spadom = "Æ har sett mye rart, men det der gir mæ hodepine. Prøv igjen."
        ip_logg[ip] = sporsmal

return render_template("index.html", spadom=spadom, sporsmal=sporsmal)
```

def hent\_neste\_glimt\_kamp():
url = "[https://v3.football.api-sports.io/fixtures](https://v3.football.api-sports.io/fixtures)"
headers = {"x-apisports-key": API\_KEY}
params = {
"team": TEAM\_ID,
"next": 1
}
try:
response = requests.get(url, headers=headers, params=params)
data = response.json()
kamp = data\['response']\[0]

```
    hjemmelag = kamp['teams']['home']['name']
    bortelag = kamp['teams']['away']['name']
    dato_str = kamp['fixture']['date']
    dato = datetime.fromisoformat(dato_str.replace("Z", "+00:00")).strftime("%A %d. %B kl %H:%M")

    tilfeldig_spiller = random.choice(spillere_glimt)
    base = random.choice(spaadommer_fotball).format(spiller=tilfeldig_spiller)

    resultat = f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {base}"
    return resultat
except Exception as e:
    return f"Faen, æ fekk ikkje tak i kampdata: {e}"
```

if **name** == "**main**":
app.run(debug=True)
