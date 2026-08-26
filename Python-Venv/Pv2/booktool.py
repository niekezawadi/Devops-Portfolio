#!/usr/bin/env python3
"""
Pv2 - het projectje dat gedeployed wordt

Klein hulpprogramma dat de School Library API bevraagt. Het hangt af van
één externe library (requests) -- en dat is precies waarom het een venv nodig
heeft: zonder die library werkt het niet, en met de verkeerde versie mogelijk
ook niet.

Gebruik:
    python3 booktool.py aantal
    python3 booktool.py zoek <auteur>
    python3 booktool.py versies
"""

import sys

import requests

APIHOST = "http://library.demo.local"


def alle_boeken():
    r = requests.get(
        f"{APIHOST}/api/v1/books",
        params={"includeISBN": "true"},
        headers={"accept": "application/json"},
        timeout=5,
    )
    r.raise_for_status()
    return r.json()


def cmd_aantal():
    boeken = alle_boeken()
    print(f"{len(boeken)} boeken in de bibliotheek.")


def cmd_zoek(term):
    boeken = alle_boeken()
    treffers = [b for b in boeken if term.lower() in b.get("author", "").lower()]
    if not treffers:
        print(f"Geen boeken gevonden van een auteur met '{term}' in de naam.")
        return
    print(f"{len(treffers)} treffer(s) voor '{term}':")
    for b in treffers:
        print(f"  [{b['id']:>3}] {b['title']}  -  {b['author']}")


def cmd_versies():
    """Toont welke Python en welke requests-versie effectief gebruikt worden."""
    print(f"Python      : {sys.version.split()[0]}")
    print(f"Interpreter : {sys.executable}")
    print(f"requests    : {requests.__version__}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    commando = sys.argv[1]
    try:
        if commando == "aantal":
            cmd_aantal()
        elif commando == "zoek" and len(sys.argv) > 2:
            cmd_zoek(" ".join(sys.argv[2:]))
        elif commando == "versies":
            cmd_versies()
        else:
            print(__doc__)
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"FOUT: geen verbinding met {APIHOST}. Draait de School Library API?")
        sys.exit(1)


if __name__ == "__main__":
    main()
