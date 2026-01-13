# Troll-Tove Spåkone App 🔮

En norsk spåkone-app med humor, spesielt for Bodø/Glimt-fans! Troll-Tove gir spådommer om fotball og livet generelt.

## 🚀 Publish Online (Quick Start)

**Want to publish online in 5 minutes?** → See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

**Need detailed guide for other platforms?** → See [DEPLOYMENT.md](DEPLOYMENT.md)

## Funksjoner

- **Hovedmodus**: Spør Troll-Tove om hva som helst
- **Glimt-modus**: Få spådommer om Bodø/Glimt
- **Dark-modus**: Dystere spådommer om framtida
- **AI-genererte svar**: Bruk OpenAI for lengre, mer varierte spådommer (valgfritt)
- **IP-basert caching**: Samme IP får samme spådom i en time
- **Health check endpoint**: Overvåk appens helse

## ✨ AI-Genererte Spådommer (Nytt!)

Troll-Tove kan nå bruke OpenAI (ChatGPT) for å generere dynamiske spådommer på nordnorsk!

**Fordeler med AI-modus:**
- Lengre, mer detaljerte svar (2-4 setninger)
- Mindre repetisjon (smart anti-repeat system)
- Bevarer Nordnorsk "spåkone" tone
- Automatisk fallback til fil-baserte spådommer hvis API feiler

**Slik aktiverer du AI-modus:**

1. Få en OpenAI API-nøkkel: https://platform.openai.com/api-keys
2. Legg til i `.env` filen:
   ```bash
   OPENAI_API_KEY=your-api-key-here
   ```
3. Start appen - den bruker nå AI for spådommer!

**Kostnadskontroll:**
- Bruker `gpt-4o-mini` som standard (kostnadseffektivt)
- Maksimum 220 tokens per svar
- Konfigurerbar temperatur (0.8 standard)

**Valgfritt - appen fungerer helt fint uten API-nøkkel!** Den bruker da de forhåndsskrevne spådommene fra tekstfilene.

## Teknologi

- Python 3.9+
- Flask 2.3.2
- Gunicorn for produksjon
- OpenAI API (valgfritt, for AI-genererte svar)

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

### Påkrevd:
- `SECRET_KEY`: Flask secret key (viktig i produksjon!)
- `FLASK_DEBUG`: Sett til `true` kun i utvikling

### Valgfritt (OpenAI-integrasjon):
- `OPENAI_API_KEY`: OpenAI API-nøkkel for AI-genererte spådommer
- `OPENAI_MODEL`: Modell å bruke (standard: `gpt-4o-mini`)
- `OPENAI_MAX_TOKENS`: Maks tokens per svar (standard: 220)
- `OPENAI_TEMPERATURE`: Tilfeldighet 0-2 (standard: 0.8)
- `OPENAI_TIMEOUT`: API timeout i sekunder (standard: 30)

### Annet:
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

Kjør tester med pytest:

```bash
# Installer pytest hvis nødvendig
pip install -r requirements.txt

# Kjør alle tester
pytest tests/

# Kjør med verbose output
pytest tests/ -v
```

Test at appen starter:
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

For AI-genererte spådommer (valgfritt):
- `OPENAI_API_KEY` - Få fra https://platform.openai.com/api-keys

## Lisens

Dette er et hobbyprosjekt for moro skyld! 🎉
