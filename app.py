from flask import Flask, render_template, request
import random
import os
import requests
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime, timedelta
from ipaddress import ip_address

load_dotenv()

app = Flask(__name__)

# Spådommer (30 fotballrelaterte og 30 generelle)
fotball_spa = [
    "Glimt vinn serien, men det blir faen ikke pent!", "Saltnes blir solgt til Rosenborg, æ brekk mæ!", "Glimt tape mot et jævla OBOS-lag i cupen.", 
    "Pellegrino skår mål med ræva, og ælskes i media.", "Kjetil Knutsen legg opp og bli fiskar.", "Det blir faen meg snøstorm på kampdag.",
    "Dommeren e søring og Glimt får straff imot som vanlig.", "Bodø/Glimt rykke ned etter en historisk dårlig høstsesong.", 
    "Glimt kjøp en islending som heter noe ingen kan uttal.", "Zinkernagel kommer tebake og tar over hele jævla laget.", 
    "Bortefeltet på Lerkendal blir tomt – ingen gidde se på rævva fotball.", "Det blir 4–4 mot Sandefjord. Faen heller.", 
    "Keeperen sklit og score sjølmål. Herregud.", "Ulrik Saltnes få seg ny sveiseblind frisør. Krisemøte i Glimt.", 
    "TIL lede serien i en dag, så går det rett åt helvete.", "Mjøndalen bli Norges beste lag. Nei vent, det skjer aldri.", 
    "Molde og Rosenborg fusjonere – og kalle laget MØKK.", "Bodø/Glimt skår 10 mål, men det blir uavgjort.", 
    "Svenskene i Glimt glemme ka kamp e og møte opp i dress.", "Dommere innføre nytt regelverk: Glimt får aldri frispark.",
    "Ny stadion på Rognan, alle må pendle med jævla hurtigbåt.", "Bortekamper i Europa? Garantert flystreik!", 
    "Glimt bytt draktfarge til lilla for å 'skille sæ ut'.", "Hele Aspmyra bli stengt – for mye bannskap.", 
    "Spillerne streike for å få bedre kaffemaskin i garderoben.", "Supporterne boikotte stadion for at pølsan e lunka.", 
    "VAR innføres i Eliteserien og alt går til helvete.", "Ny Glimt-låt toppa Spotify, men e ræva.", 
    "Glimt kjøp spiss fra Færøyene. Blir toppscorer.", "Æ tar ikke feil – Glimt vinne med 7 mål mot Rosenborg!"
]

annet_spa = [
    "Du kommer til å søle kaffe i fanget i morra tidlig.", "Naboen din planlegge å begynne med trompet.", 
    "Mobilen din ramle i dass. Igjen.", "Du får plutselig lyst på leverpostei. Hva faen?", 
    "Noen du kjenne farge håret blått og mene det e 'en vibe'.", "Du blir oppringt av en svindler, og vurderer faktisk å høre på han.", 
    "Skoa dine blir spist av en hund. Ikke din hund.", "Du blir lurt med på yoga og fjerte høyt under stillhet.", 
    "Du glemme pin-koden og skjemme dæ ut i butikken.", "Noen roper navnet ditt, men det va ikke dæ. Pinlig.", 
    "Du får uventet besøk – og huset ser ut som et jævla katastrofeområde.", "Du spis taco tirsdag, onsdag og torsdag. Livet er godt.", 
    "Du blir sittende fast i heis med en som snakke om krystalla.", "Du blir forbanna på printeren – og det vise sæ å være din feil.", 
    "En måse stjel matpakka di. Naturen hate dæ.", "Du får plutselig lyst å løpe maraton. Det går over fort.", 
    "Du trør i bæsj. Igjen.", "Noen tagger bilen din med 'søt bil'. For en idiot.", 
    "Du bestille pakke – den havne i Hammerfest.", "Du sovne på sofaen og våkne 6 timer før vekkerklokka.", 
    "Du får melding fra eksen. Slett den.", "Du mister nettet midt i Netflix-finale. Livskrise.", 
    "Du drømme om at du e naken på jobb. Igjen.", "Du tråkke på legokloss. Barna dine flire.", 
    "Du begynne å høre på country. Ikke si det til nån.", "Du tenke å starte podcast. Ikke gjør det.", 
    "Kaffemaskinen streike. Kontoret går til helvete.", "Du få ny sveis og angre i det sekundet det e for seint.", 
    "Noen spør om du har gått ned i vekt. Du har ikke det.", "Du planlegg å rydde boden – men ser en serie i stedet."
]

# Enkel IP-rate limiter
ip_log = defaultdict(lambda: {"last_request": None, "last_result": None})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip_key = str(ip_address(user_ip))
        now = datetime.utcnow()

        last_entry = ip_log[ip_key]
        last_time = last_entry["last_request"]
        last_result = last_entry["last_result"]

        if last_time and (now - last_time) < timedelta(minutes=5):
            result = last_result
        else:
            result = random.choice(fotball_spa + annet_spa)
            ip_log[ip_key]["last_request"] = now
            ip_log[ip_key]["last_result"] = result

        return render_template("result.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
