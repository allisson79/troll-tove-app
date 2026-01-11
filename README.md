# Troll-Tove Spåkone App 🔮

En norsk spåkone-app med humor, spesielt for Bodø/Glimt-fans! Troll-Tove gir spådommer om fotball og livet generelt.

## Funksjoner

- **Hovedmodus**: Spør Troll-Tove om hva som helst
- **Glimt-modus**: Få spådommer om Bodø/Glimt
- **Dark-modus**: Dystere spådommer om framtida
- **IP-basert caching**: Samme IP får samme spådom i en time
- **Health check endpoint**: Overvåk appens helse

## Teknologi

- Python 3.9+
- Flask 2.3.2
- Gunicorn for produksjon

## Installasjon

1. Klon repositoryet:
```bash
git clone https://github.com/allisson79/troll-tove-app.git
cd troll-tove-app
```

2. Installer avhengigheter:
```bash
pip install -r requirements.txt
```

3. Kopier `.env.example` til `.env` og oppdater verdiene:
```bash
cp .env.example .env
```

4. Kjør appen lokalt:
```bash
python app.py
```

Appen vil kjøre på `http://localhost:5000`

## Produksjonsoppsett

For produksjon, bruk Gunicorn:

```bash
gunicorn app:app
```

Eller med flere workers:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Miljøvariabler

- `SECRET_KEY`: Flask secret key (viktig i produksjon!)
- `FLASK_DEBUG`: Sett til `true` kun i utvikling
- `API_FOOTBALL_KEY`: API-nøkkel (for fremtidig bruk)

## Endpoints

- `/` - Hovedside med skjema
- `/glimtmodus` - Glimt-spesifikke spådommer
- `/darkmodus` - Mørke spådommer
- `/health` - Health check for monitoring

## Sikkerhet

- IP-validering med error handling
- Input sanitering (maks lengde på navn og spørsmål)
- LRU cache med timeout for å unngå minnelekkasje
- Debug mode er disabled i produksjon
- Secret key for Flask sessions

## Testing

Kjør GitHub Actions workflow eller test lokalt:

```bash
python -c "import app; print('App imports successfully')"
```

Test health endpoint:
```bash
curl http://localhost:5000/health
```

## Lisens

Dette er et hobbyprosjekt for moro skyld! 🎉
