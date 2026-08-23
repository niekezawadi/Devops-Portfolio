#!/usr/bin/env python3
"""
Ap3 - Eigen API-experiment (Python)

Gebaseerd op lab 4.9.2, waar een Python-applicatie twee REST-API's aan elkaar
knoopt: eerst een locatie omzetten naar coordinaten, dan die coordinaten
gebruiken voor een tweede call.

Hier doe ik hetzelfde patroon met andere API's:
  1. Open-Meteo Geocoding  -> plaatsnaam wordt breedte- en lengtegraad
  2. Open-Meteo Forecast   -> die coordinaten worden het actuele weer

Geen API-sleutel nodig, in tegenstelling tot GraphHopper.

Uitvoeren:  python3 ap3_weerapplicatie.py
Stoppen:    typ q of quit
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10


# ---------------------------------------------------------------- geocoding
def geocoding(location):
    """
    Zet een plaatsnaam om naar coordinaten.
    Geeft terug: (status, lat, lon, volledige_naam)

    Zelfde opzet als de geocoding-functie uit lab 4.9.2: blijft vragen zolang
    er niets ingevuld is, en geeft "null" terug als het misloopt.
    """
    while location == "":
        location = input("Geef opnieuw een plaats: ")

    reply = requests.get(
        GEOCODE_URL,
        params={"name": location, "count": 1, "language": "nl", "format": "json"},
        timeout=TIMEOUT,
    )
    status = reply.status_code
    data = reply.json()

    print(f"\nGeocoding API URL voor {location}:")
    print(reply.url)

    # Let op: bij een onbekende plaats is de status 200, maar ontbreekt
    # de sleutel "results" volledig. Dat is dezelfde valkuil als de lege
    # hits-lijst in lab 4.9.2.
    if status == 200 and data.get("results"):
        plaats = data["results"][0]
        lat = plaats["latitude"]
        lon = plaats["longitude"]

        naam = plaats["name"]
        land = plaats.get("country", "")
        streek = plaats.get("admin1", "")

        if streek and land:
            volledig = f"{naam}, {streek}, {land}"
        elif land:
            volledig = f"{naam}, {land}"
        else:
            volledig = naam

        return status, lat, lon, volledig

    if status != 200:
        print(f"Geocoding gaf status {status} terug.")
    else:
        print(f"Geen plaats gevonden met de naam '{location}'.")

    return status, "null", "null", location


# ------------------------------------------------------------------- weer
def weer(lat, lon):
    """
    Haalt het actuele weer en de voorspelling voor vandaag op.
    Geeft terug: (status, dictionary met de gegevens of None)
    """
    reply = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
        },
        timeout=TIMEOUT,
    )
    print("\nForecast API URL:")
    print(reply.url)

    if reply.status_code != 200:
        return reply.status_code, None

    return reply.status_code, reply.json()


# ----------------------------------------------------------- weercode uitleg
WEERCODES = {
    0: "helder", 1: "grotendeels helder", 2: "half bewolkt", 3: "bewolkt",
    45: "mist", 48: "aanvriezende mist",
    51: "lichte motregen", 53: "motregen", 55: "dichte motregen",
    61: "lichte regen", 63: "regen", 65: "zware regen",
    71: "lichte sneeuw", 73: "sneeuw", 75: "zware sneeuw",
    80: "buien", 81: "stevige buien", 82: "hevige buien",
    95: "onweer", 96: "onweer met hagel", 99: "zwaar onweer met hagel",
}


def toon(volledig, data):
    huidig = data.get("current", {})
    eenheden = data.get("current_units", {})
    dag = data.get("daily", {})

    code = huidig.get("weather_code")
    omschrijving = WEERCODES.get(code, "onbekend")

    print("=" * 55)
    print(f"Het weer in {volledig}")
    print("=" * 55)
    print(f"Toestand      : {omschrijving}")
    print(f"Temperatuur   : {huidig.get('temperature_2m')}{eenheden.get('temperature_2m', '')}")
    print(f"Luchtvochtig. : {huidig.get('relative_humidity_2m')}{eenheden.get('relative_humidity_2m', '')}")
    print(f"Wind          : {huidig.get('wind_speed_10m')}{eenheden.get('wind_speed_10m', '')}")

    maxima = dag.get("temperature_2m_max") or []
    minima = dag.get("temperature_2m_min") or []
    if maxima and minima:
        print(f"Vandaag       : min {minima[0]}  /  max {maxima[0]}")

    print(f"Tijdzone      : {data.get('timezone')}")
    print("=" * 55)


# -------------------------------------------------------------------- main
def main():
    print("Weerapplicatie - typ q of quit om te stoppen\n")

    while True:
        try:
            plaats = input("Plaats: ")

            if plaats in ("q", "quit"):
                print("Tot ziens.")
                break

            status, lat, lon, volledig = geocoding(plaats)

            if lat == "null":
                print("Probeer een andere plaatsnaam.\n")
                continue

            print(f"Coordinaten   : {lat}, {lon}")

            status, data = weer(lat, lon)

            if data is None:
                print(f"De weer-API gaf status {status} terug.\n")
                continue

            print()
            toon(volledig, data)
            print()

        except requests.exceptions.ConnectionError:
            print("FOUT: geen internetverbinding.\n")
        except requests.exceptions.Timeout:
            print(f"FOUT: de server antwoordde niet binnen {TIMEOUT} seconden.\n")
        except KeyboardInterrupt:
            print("\nAfgebroken.")
            break


if __name__ == "__main__":
    main()