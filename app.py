from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Intro-fraser fra Troll-Tove
intro = [
    "Hmm... la mæ føle litt på kraftan...",
    "Vent no litt... æ må ta inn energian...",
    "Oooh... det her kjennes mørkt ut...",
    "Troll-Tove føle noe... skummelt...",
    "Kaffen har sagt sitt... og det lukte trøbbel..."
]

# Spådommer for ulike kategorier
spaadommer_fotball = [
    "Rosenborg? Gå hjem og legg dokker. Det blir tap og tåra i dusjen.",
    "Tromsø vinne kanskje på FIFA, men ikkje i virkeligheta. Glimt køyrer over dem.",
    "Molde e som ei fiskekake uten salt – smakløs og blaut.",
    "Glimt stille med lyn og helvete. Motstanderen har ikkje sjans.",
    "Det blir 4-0 tell Glimt. Resten e bare å beklage til motstanderen sin familie."
]

spaadommer_random = [
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Torsdag blir en jævlig dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "En fremmed vil tilby dæ potetgull... Si ja. Det e skjebnen som snakke.",
    "Hold dæ unna IKEA neste uke. Det blir blod."
]

def neste_glimt_kamp():
    # Midlertidig hardkodet – bytt ut med ekte data senere
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

        # Hvis spørsmålet handler om Glimt og seier
        if "glimt" in spm and "vinn" in spm:
            spadom = (
                "Glimt vinn faen meg 2–1, og motstanderen får ræva parkert i fjæra med pukk i sokkan. "
                "Pellegrino bøtte inn mål og får en forsvarsspiller til å grine på direkten."
            )

        elif "kamp" in spm or "neste kamp" in spm or "lillestrøm" in spm:
            spadom = neste_glimt_kamp()

        elif any(word in spm for word in [
            "glimt", "fotball", "eliteserien", "rosenborg", "til", "tromsø", "molde", "tottenham"
        ]):
            spadom = random.choice(spaadommer_fotball)

        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
