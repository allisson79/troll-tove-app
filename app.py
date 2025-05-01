from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        # Hvis spørsmålet handler om seier til Glimt
        if "glimt" in spm and "vinn" in spm:
            spadom = (
                "Glimt vinn faen meg 2–1, og motstanderen får ræva parkert i fjæra med pukk i sokkan. "
                "Pellegrino bøtte inn mål og får en forsvarsspiller til å grine på direkten."
            )

        # Neste kamp
        elif "kamp" in spm or "neste kamp" in spm or "lillestrøm" in spm:
            spadom = neste_glimt_kamp()

        # Generelle fotballspørsmål
        elif any(word in spm for word in [
            "glimt", "fotball", "eliteserien", "rosenborg", "til", "tromsø", "molde", "tottenham"
        ]):
            spadom = random.choice(spaadommer_fotball)

        # Alt annet – random galskap
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
