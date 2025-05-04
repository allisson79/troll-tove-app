from flask import Flask, render_template, request
import random
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load\_dotenv()

app = Flask(**name**)

API\_KEY = os.getenv("API\_FOOTBALL\_KEY")
TEAM\_ID = 327  # Bodø/Glimt

spillere\_glimt = \[
"Julian", "Nikita", "Magnus", "Villads", "Odin", "Haitam", "Jostein",
"Fredrik", "Brede", "Fredrik", "Patrick", "Sondre", "Ulrik", "Sondre",
"Håkon", "Jeppe", "Kasper", "Jens", "Ole", "Andreas", "Daniel", "Isak",
"Sondre", "Mikkel"
]

spaaprosaver = \[
"{spiller} smell inn to mål før pause og setter fyr på Aspmyra.",
"{spiller} klinke inn vinnermålet i det 89. minuttet – og publikum eksplodere!",
"{spiller} skyt så hardt at keeperen må sy syv sting bak øret.",
"Det blir 2–1, og {spiller} e helten som vanlig.",
"1–1, men {spiller} redder poeng med en frekk lobb.",
"3–2 te Glimt – {spiller} score hattrick og tar æra aleina.",
"{spiller} starta på benken men byttes inn og avgjør. Helt Texas!",
"{spiller} scorer fra midtbanen. Kommentatoren klikker.",
"0–0, men {spiller} gjør en tunnel så frekk at hele benken blir rød i trynet.",
"2–0, og {spiller} feire med å hoppe opp på taket av kiosken."
]

spaaprosatull = \[
"Du får ikke svaret nu – æ høre på radio.",
"Ligg unna sånne spørsmål, dæm bringe ulykke.",
"Æ ser bare tåke... og en Rosenborg-supporter som gråte.",
"Det blir enten seier, tap, eller uavgjort – æ e ikke Gud!",
"Kaffesumpen min eksploderte akkurat – still spørsmålet på nytt.",
"Æ kan spå kjærlighet og død – men ikke odds.",
"Må æ virkelig spå fotball heile tia? Skaff dæ et liv.",
"Du spør om Glimt, men æ ser bare Molde sine tårer.",
"Dommeren avgjør – som vanlig – og æ ser fusk i horisonten.",
"En fuggel viska mæ i øret: Glimt vinne, men æ trur han ljug.",
"Du e for utålmodig. Kom tebake når du har ofra en wienerpølse."
]

introtekster = \[
"Oooh... la mæ føle litt på kraftan...",
"Det lukta svette og faenskap... det blir et svar nu.",
"Æ rope ut i evigheta... og noe rope tilbake.",
"Kaffen koka, runene blinke... no skjer det.",
"Universet rasle – Troll-Tove lytte.",
"Hold kjeft og hør – æ har kontakt med mørket.",
"Noe kommer... det e sterkt... det e frekt... det e svar!"
]

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

    glimt_hjemme = hjemmelag.lower() == "bodø/glimt"
    tilfeldig_spiller = random.choice(spillere_glimt)
    base = random.choice(spaaprosaver).format(spiller=tilfeldig_spiller)

    resultat = f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {base}"
    return resultat

except Exception as e:
    return f"Faen, æ fekk ikkje tak i kampdata: {str(e)}"
```

@app.route("/", methods=\["GET", "POST"])
def troll\_tove():
spadom = ""
intro\_valg = ""
sporsmal = ""

```
if request.method == "POST":
    sporsmal = request.form.get("sporsmal", "")
    intro_valg = random.choice(introtekster)
    spm = sporsmal.lower()

    if "kamp" in spm or "neste kamp" in spm or "score" in spm:
        spadom = hent_neste_glimt_kamp()
    elif any(word in spm for word in ["glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"]):
        spiller = random.choice(spillere_glimt)
        spadom = random.choice(spaaprosaver).format(spiller=spiller)
    else:
        spadom = random.choice(spaaprosatull)

return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
```
