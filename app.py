from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import random
import logging

# Import from troll_tove package
from troll_tove import (
    load_predictions_from_file,
    PredictionSelector,
    ToneFormatter,
    PredictionCache,
    IPValidator,
    OpenAIGenerator
)

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

# Initialize cache for IP-based predictions
ip_cache = PredictionCache()

# Load predictions
fotball_spaadommer = load_predictions_from_file("spaadommer_fotball.txt")
random_spaadommer = load_predictions_from_file("spaadommer_random.txt")

# Initialize prediction selector
prediction_selector = PredictionSelector(fotball_spaadommer, random_spaadommer)

# Initialize tone formatter
tone_formatter = ToneFormatter()

# Initialize OpenAI generator
openai_generator = OpenAIGenerator()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = tone_formatter.sanitize_user_name(request.form.get("navn", "Du"))
        user_question = tone_formatter.sanitize_question(request.form.get("sporsmal", ""))

        # Get and validate IP address
        ip_key = IPValidator.extract_and_validate(
            request.headers.get("X-Forwarded-For"),
            request.remote_addr
        )

        # Check cache or generate new prediction
        prediction = ip_cache.get(ip_key)
        if not prediction:
            # Try OpenAI first, fallback to file-based
            def fallback_prediction():
                return random.choice(prediction_selector.get_all_predictions())
            
            prediction = openai_generator.generate_prediction(
                mode="standard",
                user_name=user_name,
                user_question=user_question,
                fallback=fallback_prediction
            )
            ip_cache.set(ip_key, prediction)

        intro_message = tone_formatter.format_standard_intro(user_name)
        return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)

    return render_template("index.html")


@app.route("/glimtmodus", methods=["GET"])
def glimtmodus():
    user_name = "du jævel"
    user_question = "Hvordan går det med Glimt?"
    
    # Try OpenAI first, fallback to file-based
    def fallback_prediction():
        return random.choice(prediction_selector.get_fotball_prediction())
    
    prediction = openai_generator.generate_prediction(
        mode="glimt",
        user_name=user_name,
        user_question=user_question,
        fallback=fallback_prediction
    )
    
    intro_message = tone_formatter.format_glimt_intro(user_name)
    return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)


@app.route("/darkmodus", methods=["GET"])
def darkmodus():
    user_name = "kompis"
    user_question = "Hva bringer mørket?"
    
    # Try OpenAI first, fallback to file-based
    def fallback_prediction():
        return random.choice(prediction_selector.get_random_prediction())
    
    prediction = openai_generator.generate_prediction(
        mode="dark",
        user_name=user_name,
        user_question=user_question,
        fallback=fallback_prediction
    )
    
    intro_message = tone_formatter.format_dark_intro(user_name)
    return render_template("result.html", sporsmal=user_question, spadom=prediction, intro=intro_message)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for monitoring"""
    counts = prediction_selector.count_predictions()
    return jsonify({
        "status": "healthy",
        "fotball_predictions": counts["fotball"],
        "random_predictions": counts["random"],
        "cache_size": ip_cache.size()
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
