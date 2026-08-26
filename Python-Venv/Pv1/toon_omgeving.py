#!/usr/bin/env python3
"""
Pv1 - klein hulpprogramma om te tonen in welke omgeving je zit.

Draai dit binnen en buiten de virtuele omgeving en vergelijk de uitvoer.
Dat is het hele punt van het experiment.
"""

import sys

print("Python-versie :", sys.version.split()[0])
print("Interpreter   :", sys.executable)
print("Zoekpad       :")
for pad in sys.path:
    if pad:
        print("   ", pad)

try:
    import requests
    print("requests      :", requests.__version__)
    print("               ", requests.__file__)
except ImportError:
    print("requests      : niet geinstalleerd in deze omgeving")
