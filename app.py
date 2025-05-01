from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Spådoms-lister
spaadommer_fotball = [
    "JA, Glimt vinn – og Rosenborg kan fette ta seg en bolle med surt trønderpiss.",
    "NEI, TIL vinn aldri mer. Tromsø e bare en jævla blaut flekk på kartet.",
    "Molde? Æ får mer underholdning av å se maling tørke i Alta.",
    "Glimt kjøre over alle. Neste motstander kan bare stille med prester og lykkeønska.",
]

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
]

intro = [
    "Hald kjeft litt, æ må inn i transe...",
    "Oooh... det her kjennes mørkt ut...",
    "Kraftan e mørk i dag... akkurat som mor di sin kjøttsuppe."
]

def neste_glimt_kamp():
    hjemmelag = "Bodø/Glimt"
    bortelag = "Lillestrøm"
    dato = "Søndag 5. mai kl 18:00"

    glimt_hjemme = "glimt" in hjemmelag.lower()

    if glimt_hjemme:
        resultat = "Glimt vinn 3–1. Pellegrino skyt så hardt at ballen eksplodere. Lillestrøm tar bussen heim i skam."
    else:
        resultat = "Borte mot Lillestrøm... det lukte 2–2, og en jævla hodeløs dommeravgjørelse."

    return f"Neste kamp: {hjemmelag} – {bortelag}, {dato}. {resultat}"

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if "kamp" in spm or "neste kamp" in spm or "lillestrøm" in spm:
            spadom = neste_glimt_kamp()
        elif any(word in spm for word in [
            "glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"
        ]):
            spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
