# Ap5 – Eigen REST-API experiment met curl

**In één zin:** de volledige levenscyclus van één boek — aanmaken, lezen, wijzigen, verwijderen — met alleen curl, in één script.

## Waarom dit experiment

Ap3 en Ap4 lezen alleen data op. Een GET is ongevaarlijk en vraagt geen authenticatie. Ik wilde het deel dat daar ontbrak: gegevens die ik zelf **wegschrijf**, en dus ook het token dat daarvoor nodig is.

Daarvoor gebruik ik de School Library API uit lab 4.5.5. Die draait lokaal in de DEVASC VM, heeft beveiligde endpoints, en ondersteunt alle vier de HTTP-methodes.

## Uitvoeren

Eerst controleren of de API draait:

```bash
curl -I http://library.demo.local
```

Dan:

```bash
chmod +x crud_lifecycle.sh
./crud_lifecycle.sh
```

![Volledige uitvoer](Img/01-lifecycle.png)

## De zes stappen

| | Methode | Endpoint | Token nodig |
|---|---|---|---|
| 1 | POST | `/loginViaBasic` | nee |
| 2 | POST | `/books` | **ja** |
| 3 | GET | `/books/999` | nee |
| 4 | PUT | `/books/999` | **ja** |
| 5 | DELETE | `/books/999` | **ja** |
| 6 | POST zonder token | `/books` | tegenproef |

Stap 6 moet **mislukken** met een 401. Een experiment dat alleen toont dat iets werkt, toont niet dat de beveiliging werkt.

## Het token in een variabele

```bash
TOKEN=$(curl -s -X POST "$APIHOST/api/v1/loginViaBasic" \
             -u "$LOGIN:$PASSWORD" \
        | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

Drie dingen gebeuren hier:

- `-u user:pass` is Basic Auth — curl bouwt daar zelf de header `Authorization: Basic ...` van
- `-s` onderdrukt de voortgangsbalk, anders komt die mee in de variabele
- de uitvoer is JSON, dus ik haal er met Python één veld uit

Door het token één keer op te halen en in een variabele te bewaren, kan ik het bij elke volgende call hergebruiken met `-H "X-API-Key: $TOKEN"`.

## Het wachtwoord tussen enkele quotes

```bash
PASSWORD='Cisco123!'
```

Bij dubbele quotes probeert bash het uitroepteken te vervangen door een commando uit de geschiedenis. Enkele quotes schakelen alle interpretatie uit. Dit kostte mij tijd voor ik het doorhad.

## Alleen de statuscode opvragen

```bash
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APIHOST/api/v1/books/999")
```

`-o /dev/null` gooit de inhoud weg, `-w "%{http_code}"` drukt alleen het getal af. Zo kan ik controleren zonder de hele JSON op het scherm te krijgen. Na de DELETE moet daar **404** staan; na een POST zonder token **401**.

## Van curl naar Python

Dezelfde call, twee talen:

```bash
curl -X POST "http://library.demo.local/api/v1/books" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: $TOKEN" \
     -d '{"id": 999, "title": "...", "author": "..."}'
```

```python
requests.post(
    "http://library.demo.local/api/v1/books",
    headers={"Content-Type": "application/json", "X-API-Key": token},
    data=json.dumps(boek),
)
```

Regel voor regel komt dat overeen:

| curl | Python (requests) |
|---|---|
| `-X POST` | `requests.post(...)` |
| `-H "naam: waarde"` | `headers={"naam": "waarde"}` |
| `-d '{...}'` | `data=json.dumps(...)` |
| `-u user:pass` | `auth=(user, pass)` |
| `-s` | standaardgedrag |

## Mogelijke vragen

**Verschil tussen PUT en POST?**
POST maakt aan, PUT vervangt een bestaand item. PUT is idempotent: tien keer hetzelfde PUT-verzoek geeft hetzelfde eindresultaat, tien keer POST maakt tien boeken.

**Waarom `set -u` bovenaan het script?**
Dan stopt het bij een typfout in een variabelenaam, in plaats van stilletjes een lege string te gebruiken.

**Waarom id 999?**
Ver van de bestaande id's, zodat het experiment niets kapotmaakt van wat er al staat.

**Waarom een script en niet zes losse commando's?**
Het token moet doorgegeven worden aan elke beveiligde call. In een script haal ik het één keer op. Bovendien is het script herhaalbaar — dat is het hele punt van automatisering.

**Wat betekent 401 tegenover 403?**
401 betekent: ik weet niet wie je bent. 403: ik weet wie je bent, maar je mag dit niet.

## Wat ik ondervond

Bij het testen merkte ik dat ik soms een 400 in plaats van de verwachte 401 kreeg wanneer ik de header-naam net verkeerd typte (`X-API-Key` met een kleine letter ergens) — dat leerde me dat REST-API's headers wél hoofdlettergevoelig kunnen behandelen aan de kant van het framework, ook al zegt de HTTP-standaard dat headernamen case-insensitive zouden moeten zijn. Na het corrigeren van de header liep de volledige lifecycle in één keer door.
```
