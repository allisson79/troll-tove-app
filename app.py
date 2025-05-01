import os
import random
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

app = Flask(__name__)

intro = [
    "Satan i hælvette... æ ser et tegn!",
    "Universet skrike – og æ høre det.",
    "Hold kjeften og lytt, offerlam...",
    "Æ føle det på rynkan mine... nå skjer det faenskap."
]

spaadommer_random = [
    "Torsdag blir en jævla dag. Hold deg unna folk med caps.",
    "Æ ser... æ ser... ingenting! Men æ føle en uggenhet i rumpa. Det e et tegn.",
    "Hvis du ikkje slutte å lyge... kjem ein ravn te å hakke øyan dine ut.",
    "Du kjem te å finne kjærligheten... bak Rema 1000... i en konteiner.",
    "Hold dæ unna IKEA neste uke. Det blir blod.",
]

spaadommer_fotball = [
    "RBK e ræv. Glimt kjøre over dem som en jævla dampveivals.",
    "Tromsø? Nei, det e som å spille mot en barnehage full av blinde unger.",
    "Glimt har form. Resten av Eliteserien har bare flaks og mødre som trur på dem.",
    "Æ ser 2 mål fra Glimt og en keeper som gråte i dusjen etterpå.",
    "Dommern prøve å saboter, men Glimt vinn læll. Karma, din jævel."
]

def neste_glimt_kamp():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "team": 2619,  # Bodø/Glimt
        "next": 1
    }

    response = requests.get(url, headers=headers, params=params)

    try:
        data = response.json()
        fixtures = data.get("response", [])
        if not fixtures:
            return "Ingen jævla kampdata funnet – kanskje API
