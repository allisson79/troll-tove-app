from flask import Flask, render_template, request
import random

app = Flask(__name__)

spaadommer_fotball = [
    "JA, Glimt vinn – og Rosenborg kan fette ta seg en bolle med surt trønderpiss.",
    "NEI, TIL vinn aldri mer. Tromsø e bare en jævla blaut flekk på kartet.",
    "Molde? Æ får mer underholdning av å se maling tørke i Alta.",
    "Glimt kjøre over alle. Neste motstander kan bare stille med prester og lykkeønska.",
    "Tromsø-forsvaret e like tett som en sil laga av papir og løgn.",
    "Rosenborg sin æra? Den forlot Lerkendal samtidig som VHS forsvant fra Elkjøp.",
    "Glimt tar gull, og æ føle det så sterkt at puppan mine vibrere.",
    "Neste kamp? Glimt vinn 4-0 og Pellegrino piss på keeperen."
]

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

intro = [
    "Hald kjeft litt, æ må inn i transe...",
    "Vent... æ smell snart i gang en visjon fra åndeverden...",
    "Å dæven, det her kjennes ut som det blir stygt...",
    "Kraftan e mørk i dag... akkurat som mor di sin kjøttsuppe."
]

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""
    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"]):
            spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
     Fix app = Flask(...)
    
