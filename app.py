@app.route("/", methods=["GET", "POST"])
def troll_tove():
    spadom = ""
    intro_valg = ""
    sporsmal = ""

    if request.method == "POST":
        sporsmal = request.form["sporsmal"]
        intro_valg = random.choice(intro)
        spm = sporsmal.lower()

        if any(word in spm for word in ["glimt", "bodø/glimt", "fotball", "eliteserien", "rosenborg", "molde", "tromsø", "til", "rbk", "tottenham", "kamp"]):
            if any(x in spm for x in ["neste kamp", "hvem møter", "når", "spiller"]):
                spadom = neste_glimt_kamp()
            else:
                # Gi et spesifikt resultattips
                hjemmemål = random.randint(0, 4)
                bortemål = random.randint(0, 3)

                # Favoriser Glimt
                if "glimt" in spm or "bodø" in spm:
                    if hjemmemål <= bortemål:
                        hjemmemål = bortemål + 1

                resultat = f"Glimt vinn {hjemmemål}-{bortemål}. Jævlige tilstander for motstanderen – dem får psykolog etter kampen."
                spadom = resultat
        else:
            spadom = random.choice(spaadommer_random)

    return render_template("index.html", spadom=spadom, intro=intro_valg, sporsmal=sporsmal)
