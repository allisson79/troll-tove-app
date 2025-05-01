@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if    request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if    "kamp" in spm or "neste kamp" in spm or "lillestrøm" in spm:
            spadom = neste_glimt_kamp()

        elif    any(word in spm for word in [
            "glimt", "bodø", "fotball", "eliteserien", "rosenborg",
            "molde", "tromsø", "til", "rbk"
        ]):
            spadom = random.choice(spaadommer_fotball)

        else:    
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
