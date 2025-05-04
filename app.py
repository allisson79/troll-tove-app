from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import random

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
API_HOST = os.getenv("FOOTBALL_API_HOST")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    question = request.form["question"]
    ip_address = request.remote_addr

    responses = [
        "Ja, for faen!",
        "Neppe, din fjott.",
        "Kanskje, om sola skinn i nord og sør samtidig.",
        "Det trur æ ikkje, men ka veit æ.",
        "Aldri i livet!",
        "Æ skal spør han Knutsen.",
        "Bodø/Glimt tar dæ uansett!",
        "Det va et rævva spørsmål.",
        "Hah! Det der kan du gløm!",
        "Kjør på, din gale jævel!",
    ]

    prediction = random.choice(responses)
    return render_template("result.html", prediction=prediction, question=question)

if __name__ == "__main__":
    app.run(debug=True)
