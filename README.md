# Troll-Tove Spåkone App 🔮

En norsk spåkone-app med humor, spesielt for Bodø/Glimt-fans! Troll-Tove gir spådommer om fotball og livet generelt.

## 🚀 Publish Online (Quick Start)

**Want to publish online in 5 minutes?** → See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

**Need detailed guide for other platforms?** → See [DEPLOYMENT.md](DEPLOYMENT.md)

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

### Quick Start (Anbefalt)

**Linux/macOS:**
```bash
git clone https://github.com/allisson79/troll-tove-app.git
cd troll-tove-app
./start.sh
```

**Windows:**
```cmd
git clone https://github.com/allisson79/troll-tove-app.git
cd troll-tove-app
start.bat
```

Scriptet vil automatisk:
- Opprette `.env` fil med tilfeldig SECRET_KEY
- Sette opp virtuelt miljø
- Installere avhengigheter
- Starte appen på `http://localhost:5000`

### Manuell Installasjon

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
- **VIKTIG**: `.env` filen er tracked i repo for convenience, men ALDRI commit ekte secrets! I produksjon:
  - Bruk environment variabler eller en secrets manager
  - Generer en sterk SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
  - Bruk en ekte API-nøkkel hvis du trenger den

## Testing

Kjør GitHub Actions workflow eller test lokalt:

```bash
python -c "import app; print('App imports successfully')"
```

Test health endpoint:
```bash
curl http://localhost:5000/health
```

## Publisering / Deployment 🚀

Vil du publisere Troll-Tove på internett? Vi har laget en komplett guide!

### Quick Start - Render.com (Anbefalt)

Den enkleste måten å publisere appen:

1. Opprett gratis konto på [render.com](https://render.com)
2. Klikk "New +" → "Web Service"
3. Koble til dette GitHub-repositoryet
4. Render vil automatisk bruke `render.yaml` konfigurasjon
5. Sett miljøvariabel `SECRET_KEY` (Render kan generere dette)
6. Klikk "Create Web Service"
7. Din app er nå live på internett! 🎉

### Andre Plattformer

Appen kan også publiseres på:
- **Heroku** (etablert plattform, mange add-ons)
- **Railway.app** (moderne, god utvikleropplevelse)
- **Vercel** (serverless, edge deployment)

### Detaljert Guide

Se [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Steg-for-steg instruksjoner for alle plattformer
- Miljøvariabel-oppsett
- Feilsøking
- Kostnadssammenligning
- Post-deployment sjekkliste

### Nødvendige Miljøvariabler

For produksjon, sett disse:
- `SECRET_KEY` - Generer med: `python -c "import secrets; print(secrets.token_hex(32))"`
- `FLASK_DEBUG` - Sett til `false`

## Lisens

Dette er et hobbyprosjekt for moro skyld! 🎉
