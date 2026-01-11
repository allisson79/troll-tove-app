from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import random
from ipaddress import ip_address, AddressValueError
import logging
from collections import OrderedDict
import time

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get SECRET_KEY from environment or generate a random one for development
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    if os.getenv('FLASK_DEBUG', 'False').lower() == 'true':
        # Generate a random key for development
        import secrets
        secret_key = secrets.token_hex(32)
        logger.warning("Using randomly generated SECRET_KEY for development. Set SECRET_KEY in .env for production!")
    else:
        raise ValueError("SECRET_KEY must be set in production. Add it to your .env file.")

app.config['SECRET_KEY'] = secret_key

# LRU Cache for IP-based predictions with timeout
class PredictionCache:
    def __init__(self, max_size=1000, timeout=3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.timeout = timeout  # 1 hour default
    
    def get(self, ip):
        if ip in self.cache:
            prediction, timestamp = self.cache[ip]
            # Check if cache entry is still valid
            if time.time() - timestamp < self.timeout:
                # Move to end (most recently used)
                self.cache.move_to_end(ip)
                return prediction
            else:
                # Remove expired entry
                del self.cache[ip]
        return None
    
    def set(self, ip, prediction):
        if ip in self.cache:
            self.cache.move_to_end(ip)
        self.cache[ip] = (prediction, time.time())
        # Remove oldest if max size exceeded
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

ip_cache = PredictionCache()

# Last spådommer fra filer med error handling
def last_spaadommer(filnavn):
    try:
        with open(filnavn, "r", encoding="utf-8") as f:
            predictions = [linje.strip() for linje in f if linje.strip()]
        if not predictions:
            logger.warning(f"No predictions found in {filnavn}")
            return ["Troll-Tove ser ingen ting i dag... Prøv igjen seinere."]
        return predictions
    except FileNotFoundError:
        logger.error(f"File not found: {filnavn}")
        return ["Troll-Tove har mista spådomsboka si... Kom tilbake seinere!"]
    except Exception as e:
        logger.error(f"Error reading {filnavn}: {e}")
        return ["Noko gikk gale... Troll-Tove e forvirra!"]

fotball_spaadommer = last_spaadommer("spaadommer_fotball.txt")
random_spaadommer = last_spaadommer("spaadommer_random.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        navn = request.form.get("navn", "Du").strip()
        sporsmal = request.form.get("sporsmal", "").strip()
        
        # Validate input
        if not navn or len(navn) > 100:
            navn = "Du"
        if len(sporsmal) > 500:
            sporsmal = sporsmal[:500]
        
        # Get and validate IP address
        try:
            user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            ip_key = str(ip_address(user_ip.split(",")[0].strip()))
        except (AddressValueError, ValueError, AttributeError) as e:
            logger.warning(f"Invalid IP address: {e}")
            ip_key = "unknown"

        # Check cache or generate new prediction
        spadom = ip_cache.get(ip_key)
        if not spadom:
            spadom = random.choice(fotball_spaadommer + random_spaadommer)
            ip_cache.set(ip_key, spadom)

        intro = f"Hør hør, {navn}! Troll-Tove har kikka i kula si…"
        return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

    return render_template("index.html")

@app.route("/glimtmodus", methods=["GET"])
def glimtmodus():
    navn = "du jævel"
    sporsmal = "Hvordan går det med Glimt?"
    spadom = random.choice(fotball_spaadommer)
    intro = f"Hør hør, {navn.title()}! Troll-Tove har sett lyset fra Aspmyra…"
    return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

@app.route("/darkmodus", methods=["GET"])
def darkmodus():
    navn = "kompis"
    sporsmal = "Hva bringer mørket?"
    spadom = random.choice(random_spaadommer)
    intro = f"Mørke skyer samler seg, {navn}… Troll-Tove ser noe dystert i horisonten."
    return render_template("result.html", sporsmal=sporsmal, spadom=spadom, intro=intro)

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "fotball_predictions": len(fotball_spaadommer),
        "random_predictions": len(random_spaadommer),
        "cache_size": len(ip_cache.cache)
    }), 200

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal error: {e}")
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Never use debug=True in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
