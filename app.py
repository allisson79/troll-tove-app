from flask import Flask, render_template, request
import random
def neste_glimt_kamp():
    # Midlertidig hardkodet – bytt ut med ekte data senere
    hjemmelag = "Bodø/Glimt"
    bortelag = "Lillestrøm"
    dato = "Søndag 5. mai kl 18:00"
    
    glimt_hjemme = "glimt" in hjemmelag.lower()
if "kamp" in spm or "neste kamp" in spm or "lillestrøm" in spm:
    spadom = neste_glimt_kamp()

    if glimt_hjemme:
        resultat = "Glimt vinn 3–1. Pellegrino skyt så hardt at ballen eksplodere. Lillestrøm tar bussen heim i skam."
    else:
        resultat = "Borte mot Lillestrøm... det lukte 2–2, og en jævla hodeløs dommeravgjørelse."

    return f"Neste kamp: {hjemmelag} – {bortelag}, {dato}. {resultat}"


def hent_neste_glimt_kamp():
    url = "https://www.fotmob.com/teams/8651/fixtures/bod%C3%B8glimt"  # Bodø/Glimt sin kampoversikt
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Faen, æ fikk ikke tak i kampdata. Internett sug eller Fotmob blokkere mæ."

    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        kampseksjon = soup.find("a", href=True, text=lambda t: t and "Bodø" in t or "Glimt" in t)
        kampnavn = kampseksjon.text.strip()
        kampurl = kampseksjon["href"]
        kampinfo = kampnavn.replace("\n", " ")

        hjemmelag = kampinfo.split(" - ")[0]
        bortelag = kampinfo.split(" - ")[1]

        hvis_glimt_hjemme = "glimt" in hjemmelag.lower()

        if hvis_glimt_hjemme:
            resultat = f"Glimt vinn 3–1, og {bortelag} får rævkjøring med dobbel kraft og null sjanser."
        else:
            resultat = f"Borte mot {hjemmelag}? Glimt drar dit og stjæl med sæ poeng og ære – 2–2 med sinne."

        return f"Neste kamp: {kampinfo}. {resultat}"
    
    except Exception as e:
        return f"Det gikk til helvete å spå neste kamp. ({e

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
if "kamp" in spm or "neste kamp" in spm:
    spadom = hent_neste_glimt_kamp()
if request.method == "POST":
    sporsmal = request.form["sporsmal"]
    intro_valg = random.choice(intro)
    spm = sporsmal.lower()

    if "kamp" in spm or "neste kamp" in spm:
        spadom = hent_neste_glimt_kamp()
    elif any(word in spm for word in ["glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"]):
        spadom = random.choice(spaadommer_fotball)
    else:
        spadom = random.choice(spaadommer_random)


        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "bodø", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk"]):
            spadom = random.choice(spaadommer_fotball)
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
     Fix app = Flask(...)
    
