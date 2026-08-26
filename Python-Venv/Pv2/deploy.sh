#!/bin/bash
#
# Pv2 - Eigen venv-experiment: deployment
#
# Uitvoeren:  chmod +x deploy.sh && ./deploy.sh

set -e

DOEL="${1:-/tmp/booktool-deployment}"

echo "=== 1. Uitgangssituatie: welke Python gebruikt het systeem? ==="
which python3
python3 -c "import sys; print('interpreter:', sys.executable)"
echo
echo "Is requests globaal geinstalleerd?"
python3 -c "import requests; print('  ja, versie', requests.__version__)" 2>/dev/null \
  || echo "  nee - en dat is prima, daarvoor dient de venv"

echo
echo "=== 2. Project kopieren naar $DOEL (alsof het net binnenkwam) ==="
rm -rf "$DOEL"
mkdir -p "$DOEL"
cp booktool.py requirements.txt "$DOEL/"
ls -1 "$DOEL"

cd "$DOEL"

echo
echo "=== 3. Virtuele omgeving aanmaken ==="
python3 -m venv booktool_env
echo "Aangemaakt. Wat zit erin?"
ls -1 booktool_env/bin | head -8

echo
echo "=== 4. Omgeving activeren ==="
source booktool_env/bin/activate
echo "Actieve interpreter is nu:"
python3 -c "import sys; print('  ', sys.executable)"

echo
echo "=== 5. Afhankelijkheden installeren uit requirements.txt ==="
pip install --quiet --upgrade pip
pip install -r requirements.txt
echo
pip list

echo
echo "=== 6. De applicatie draaien in de nieuwe omgeving ==="
python3 booktool.py versies

echo
echo "=== 7. Bewijs van isolatie: buiten de venv is requests er niet ==="
deactivate
echo "Na deactivate is de interpreter weer:"
python3 -c "import sys; print('  ', sys.executable)"

echo
echo "Klaar. De omgeving staat in $DOEL/booktool_env"
