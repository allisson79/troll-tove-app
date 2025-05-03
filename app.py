def neste_glimt_kamp():
    import requests
    import os

    api_key = os.getenv("API_FOOTBALL_KEY")
    headers = {
        "x-apisports-key": api_key
    }

    # Bodø/Glimt sin lag-ID i API-Football
    team_id = 195  # Dette er riktig for Eliteserien
    url = f"https://v3.football.api-sports.io/fixtures?team={team_id}&next=1"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # Sjekk om vi faktisk fikk kamper
        if "response" not in data or not data["response"]:
            return "Helvete heller, æ fekk ikkje tak i neste kamp. Kanskje universet skjule den for mæ."

        kamp = data["response"][0]
        hjemmelag = kamp["teams"]["home"]["name"]
        bortelag = kamp["teams"]["away"]["name"]
        dato = kamp["fixture"]["date"][:10]
        glimt_hjemme = hjemmelag.lower() == "bodø / glimt"

        if glimt_hjemme:
            resultat = "Glimt vinn 3–1. Motstanderan kjem med nerver og fær heim med tårer og prolaps."
        else:
            resultat = "2–2. Glimt lede, men dommern har pengeproblema og gi bort en straffe på slutten."

        return f"Neste kamp: {hjemmelag} – {bortelag} ({dato}). {resultat}"

    except Exception as e:
        return f"💀 Faen, æ fekk ikkje tak i kampdata: {e} 💀"
