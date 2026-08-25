#!/usr/bin/env python3
"""
Ap4 - Eigen API-experiment 2 (Python, webforms)

Dezelfde weerapplicatie als Ap3, maar nu achter een HTML-formulier in plaats
van in de terminal. De logica blijft identiek; alleen de bron van de invoer
verandert:

    Ap3:  plaats = input("Plaats: ")
    Ap4:  plaats = request.form.get("plaats")

Het formulier heeft drie soorten velden om te tonen hoe Flask ze uitleest:
een tekstveld, een keuzelijst en een aankruisvakje.

Starten:  python3 ap4_app.py     ->  http://127.0.0.1:5000
"""

import requests
from flask import Flask, render_template, request

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10

app = Flask(__name__)

WEERCODES = {
    0: "helder", 1: "grotendeels helder", 2: "half bewolkt", 3: "bewolkt",
    45: "mist", 48: "aanvriezende mist",
    51: "lichte motregen", 53: "motregen", 55: "dichte motregen",
    61: "lichte regen", 63: "regen", 65: "zware regen",
    71: "lichte sneeuw", 73: "sneeuw", 75: "zware sneeuw",
    80: "buien", 81: "stevige buien", 82: "hevige buien",
    95: "onweer", 96: "onweer met hagel", 99: "zwaar onweer met hagel",
}


def geocoding(location):
    """Plaatsnaam -> (lat, lon, volledige naam). Geeft None bij geen treffer."""
    reply = requests.get(
        GEOCODE_URL,
        params={"name": location, "count": 1, "language": "nl", "format": "json"},
        timeout=TIMEOUT,
    )
    reply.raise_for_status()
    data = reply.json()

    if not data.get("results"):
        return None

    plaats = data["results"][0]
    naam = plaats["name"]
    land = plaats.get("country", "")
    streek = plaats.get("admin1", "")

    if streek and land:
        volledig = f"{naam}, {streek}, {land}"
    elif land:
        volledig = f"{naam}, {land}"
    else:
        volledig = naam

    return plaats["latitude"], plaats["longitude"], volledig


def weer(lat, lon, eenheid, met_voorspelling):
    """Haalt het weer op. eenheid is 'celsius' of 'fahrenheit'."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "temperature_unit": eenheid,
        "timezone": "auto",
    }
    if met_voorspelling:
        params["daily"] = "temperature_2m_max,temperature_2m_min,weather_code"
        params["forecast_days"] = 7

    reply = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT)
    reply.raise_for_status()
    return reply.json()


@app.route("/", methods=["GET", "POST"])
def index():
    resultaat = None
    fout = None

    # Bij een GET tonen we alleen het lege formulier.
    # Bij een POST is het formulier ingediend en zit de invoer in request.form.
    if request.method == "POST":
        plaats = request.form.get("plaats", "").strip()
        eenheid = request.form.get("eenheid", "celsius")
        voorspelling = request.form.get("voorspelling") == "ja"

        if not plaats:
            fout = "Vul een plaatsnaam in."
        else:
            try:
                gevonden = geocoding(plaats)

                if gevonden is None:
                    fout = f"Geen plaats gevonden met de naam '{plaats}'."
                else:
                    lat, lon, volledig = gevonden
                    data = weer(lat, lon, eenheid, voorspelling)

                    huidig = data.get("current", {})
                    eenheden = data.get("current_units", {})
                    dagen = data.get("daily")

                    voorspellingen = []
                    if dagen:
                        for i, datum in enumerate(dagen.get("time", [])):
                            voorspellingen.append({
                                "datum": datum,
                                "min": dagen["temperature_2m_min"][i],
                                "max": dagen["temperature_2m_max"][i],
                                "omschrijving": WEERCODES.get(
                                    dagen["weather_code"][i], "onbekend"),
                            })

                    resultaat = {
                        "plaats": volledig,
                        "lat": lat,
                        "lon": lon,
                        "omschrijving": WEERCODES.get(huidig.get("weather_code"), "onbekend"),
                        "temperatuur": f"{huidig.get('temperature_2m')}{eenheden.get('temperature_2m', '')}",
                        "vochtigheid": f"{huidig.get('relative_humidity_2m')}{eenheden.get('relative_humidity_2m', '')}",
                        "wind": f"{huidig.get('wind_speed_10m')}{eenheden.get('wind_speed_10m', '')}",
                        "tijdzone": data.get("timezone"),
                        "voorspellingen": voorspellingen,
                    }

            except requests.exceptions.ConnectionError:
                fout = "Geen verbinding met de weerdienst."
            except requests.exceptions.Timeout:
                fout = f"De weerdienst antwoordde niet binnen {TIMEOUT} seconden."
            except requests.exceptions.HTTPError as e:
                fout = f"De weerdienst gaf een foutcode terug: {e}"

    # request.form bewaren zodat de ingevulde waarden blijven staan na verzenden
    return render_template("index.html", resultaat=resultaat, fout=fout,
                           ingevuld=request.form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
