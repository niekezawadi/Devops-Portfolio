#!/bin/bash
#
# Ap5 - Eigen REST-API experiment met curl
#
# Doorloopt de volledige levenscyclus van één boek met alleen curl:
#   inloggen -> aanmaken -> lezen -> wijzigen -> verwijderen -> controleren
#
# Waarom een script en niet zes losse commando's: de token moet doorgegeven
# worden aan elke beveiligde call. Door hem in een variabele te zetten hoef
# ik hem maar één keer op te halen.
#
# Uitvoeren:  chmod +x crud_lifecycle.sh && ./crud_lifecycle.sh

set -u  # stoppen bij gebruik van een niet-bestaande variabele

APIHOST="http://library.demo.local"
LOGIN="cisco"
PASSWORD='Cisco123!'   # enkele quotes: de ! wordt anders door bash geïnterpreteerd
BOOK_ID=999

kop() { echo; echo "=== $1 ==="; }

# ---------------------------------------------------------------- 1. token
kop "1. Token ophalen (POST /loginViaBasic)"
TOKEN=$(curl -s -X POST "$APIHOST/api/v1/loginViaBasic" \
             -u "$LOGIN:$PASSWORD" \
        | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

if [ -z "$TOKEN" ]; then
  echo "FOUT: geen token gekregen. Draait de API en klopt het wachtwoord?"
  exit 1
fi
echo "Token: ${TOKEN:0:25}..."

# ------------------------------------------------------------- 2. aanmaken
kop "2. Boek aanmaken (POST /books)"
curl -s -X POST "$APIHOST/api/v1/books" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: $TOKEN" \
     -d "{\"id\": $BOOK_ID, \"title\": \"DevOps voor gevorderden\", \"author\": \"Nieke Karhamba Zawadi\", \"isbn\": \"978-9-000-00001-1\"}"
echo

# --------------------------------------------------------------- 3. lezen
kop "3. Dat ene boek opvragen (GET /books/$BOOK_ID)"
curl -s -X GET "$APIHOST/api/v1/books/$BOOK_ID" -H "accept: application/json"
echo

# ------------------------------------------------------------ 4. wijzigen
kop "4. Boek wijzigen (PUT /books/$BOOK_ID)"
curl -s -X PUT "$APIHOST/api/v1/books/$BOOK_ID" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: $TOKEN" \
     -d "{\"id\": $BOOK_ID, \"title\": \"DevOps voor gevorderden - tweede druk\", \"author\": \"Nieke Karhamba Zawadi\"}"
echo

kop "4b. Controle: is de titel aangepast?"
curl -s -X GET "$APIHOST/api/v1/books/$BOOK_ID" -H "accept: application/json"
echo

# ---------------------------------------------------------- 5. verwijderen
kop "5. Boek verwijderen (DELETE /books/$BOOK_ID)"
curl -s -X DELETE "$APIHOST/api/v1/books/$BOOK_ID" -H "X-API-Key: $TOKEN"
echo

kop "5b. Controle: statuscode na verwijderen"
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APIHOST/api/v1/books/$BOOK_ID")
echo "HTTP $CODE  (404 betekent: correct verwijderd)"

# ------------------------------------------------- 6. zonder token proberen
kop "6. Tegenproef: POST zonder token"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$APIHOST/api/v1/books" \
       -H "Content-Type: application/json" \
       -d '{"id": 998, "title": "Mag niet", "author": "Niemand"}')
echo "HTTP $CODE  (401 betekent: de beveiliging werkt)"

echo
echo "Klaar."