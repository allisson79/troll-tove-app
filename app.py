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


# Load predictions from file with error handling
def load_predictions_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file_handle:
            predictions = [line.strip() for line in file_handle if line.strip()]
        if not predictions:
            logger.warning(f"No predictions found in {filename}")
            return ["Troll-Tove ser ingen ting i dag... Prøv igjen seinere."]
        return predictions
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return ["Troll-Tove har mista spådomsboka si... Kom tilbake seinere!"]
    except Exception as error:
        logger.error(f"Error reading {filename}: {error}")
        return ["Noko gikk gale... Troll-Tove e forvirra!"]


fotball_spaadommer = load_predictions_from_file("spaadommer_fotball.txt")
random_spaadommer = load_predictions_from_file("spaadommer_random.txt")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form.get("navn", "Du").strip()
        user_question = request.form.get("sporsmal", "").strip()

        # Validate input
        if not user_name or len(user_name) > 100:
            user_name = "Du"
        if len(user_question) > 500:
            user_question = user_question[:500]

        # Get and validate IP address
        try:
            user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            ip_key = str(ip_address(user_ip.split(",")[0].strip()))
        except (AddressValueError, ValueError, AttributeError) as error:
            logger.warning(f"Invalid IP address: {error}")
            ip_key = "unknown"

        # Check cache or generate new prediction
        prediction = ip_cache.get(ip_key)
        if not prediction:
            prediction = random.choice(fotball_spaadommer + random_spaadommer)
            ip_cache.set(ip_key, prediction)

        intro_message = f"Hør hør, {user_name}! Troll-Tove har kikka i kula si…"
        return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)

    return render_template("index.html")


@app.route("/glimtmodus", methods=["GET"])
def glimtmodus():
    user_name = "du jævel"
    user_question = "Hvordan går det med Glimt?"
    prediction = random.choice(fotball_spaadommer)
    intro_message = f"Hør hør, {user_name.title()}! Troll-Tove har sett lyset fra Aspmyra…"
    return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)


@app.route("/darkmodus", methods=["GET"])
def darkmodus():
    user_name = "kompis"
    user_question = "Hva bringer mørket?"
    prediction = random.choice(random_spaadommer)
    intro_message = f"Mørke skyer samler seg, {user_name}… Troll-Tove ser noe dystert i horisonten."
    return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)


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
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return render_template("500.html"), 500


if __name__ == "__main__":
    # Never use debug=True in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
