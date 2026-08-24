# Ap6 – Eigen REST-API experiment met curl 2 (forms)

**In één zin:** twee endpoints die hetzelfde doen maar een ander formaat verwachten — form-encoded tegenover JSON — om te tonen dat "de body van een verzoek" niet één ding is.

## Waarom dit experiment

In Ap4 vulde ik een formulier in de browser in en klikte op verzenden. Dat werkte, maar ik zag niet wát de browser dan verstuurde. In Ap5 stuurde ik met curl JSON naar een API. Twee verschillende dingen, allebei "een POST".

Dit experiment zet die twee naast elkaar en maakt het verschil zichtbaar op de lijn.

## Uitvoeren

Je hebt **twee terminalvensters** nodig.

In het eerste, de ontvanger starten:

```bash
python3 form_receiver.py
```

Laat dat venster open staan. In het tweede:

```bash
chmod +x test_calls.sh
./test_calls.sh
```

![Beide formaten en de tegenproeven](Img/01-form-vs-json.png)

## Het verschil

Dezelfde gegevens, twee formaten:

```bash
# form-encoded — dit is wat een browserformulier stuurt
curl -X POST http://127.0.0.1:5001/book/form \
     -d "title=Het formulierboek&author=Nieke K. Zawadi"

# JSON — dit is wat een REST-client stuurt
curl -X POST http://127.0.0.1:5001/book/json \
     -H "Content-Type: application/json" \
     -d '{"title": "Het JSON-boek", "author": "Nieke K. Zawadi"}'
```

Over de lijn ziet dat er zo uit:

```
> POST /book/form HTTP/1.1
> Content-Type: application/x-www-form-urlencoded
> Content-Length: 51
```

De header **Content-Type** bepaalt hoe de server de body moet lezen. Curl zet die bij `-d` standaard op `x-www-form-urlencoded`; wil je JSON, dan moet je hem zelf meegeven. Dát is de vergeten `-H` waar iedereen ooit op vastloopt.

Aan de Flask-kant is het onderscheid één regel:

```python
request.form          # leest form-encoded
request.get_json()    # leest JSON
```

## De vier testen

| | Wat er gestuurd wordt | Naar welk endpoint | Verwacht |
|---|---|---|---|
| 1 | form-encoded | `/book/form` | 201 Created |
| 2 | JSON | `/book/json` | 201 Created |
| 3 | JSON | `/book/form` | **400** |
| 4 | form-encoded | `/book/json` | **400** |

Test 3 en 4 zijn bewust fout. Ze geven een leesbare melding terug:

```json
{"error": "geen geldige JSON ontvangen; vergeet -H \"Content-Type: application/json\" niet"}
```

Een experiment dat alleen de goede weg toont, laat niet zien wat er misgaat als je hem verlaat.

## Test 5: kijken wat er echt over de lijn gaat

```bash
curl -v -X POST http://127.0.0.1:5001/book/form -d "title=..."
```

De optie `-v` (verbose) toont de headers die verstuurd en ontvangen worden. Regels die met `>` beginnen zijn wat curl verstuurt, regels met `<` wat de server terugstuurt. Zo zie je de `Content-Type` die curl zelf invulde zonder dat je erom vroeg.

## Waarom er een ontvanger nodig is

De School Library API aanvaardt alleen JSON. Om het verschil met form-encoded te kunnen tonen, heb ik zelf een kleine Flask-ontvanger geschreven met twee endpoints. Die zet wat hij ontvangt door naar de School Library API, zodat het geen loze demo is: er wordt echt een boek toegevoegd.

De keten is dus:

```
curl  --form of JSON-->  form_receiver.py  --JSON-->  School Library API
```

## Mogelijke vragen

**Wanneer gebruik je welk formaat?**
Form-encoded als een HTML-formulier de afzender is — dat is wat browsers standaard sturen. JSON zodra je geneste gegevens hebt: form-encoded kent alleen platte sleutel-waardeparen, geen lijsten of objecten in objecten.

**Wat is het verschil tussen `-d` en `-F` in curl?**
`-d` stuurt `x-www-form-urlencoded`, `-F` stuurt `multipart/form-data`. Dat laatste gebruik je bij bestandsuploads, want het kan binaire data aan.

**Waarom 201 en niet 200?**
201 Created betekent: gelukt én er is iets nieuws aangemaakt. Preciezer dan een kale 200.

**Waarom poort 5001?**
Poort 5000 is bezet door de app van Ap4. Twee servers op dezelfde poort kan niet.

**Waarom `silent=True` bij `get_json()`?**
Anders gooit Flask zelf een 415-fout voor ik mijn eigen leesbare melding kan teruggeven.

## Verband met de vorige experimenten

| | Wat het toont |
|---|---|
| Ap3 | data ophalen met Python |
| Ap4 | hetzelfde, maar met een formulier in de browser |
| Ap5 | data wegschrijven met curl, met authenticatie |
| Ap6 | wat dat formulier uit Ap4 nu eigenlijk verstuurt |

## Wat ik ondervond

<!-- Eén of twee eigen zinnen. Bijvoorbeeld over de Content-Type die curl
     stilzwijgend invult, of over test 3 en 4 die je verwachtte te zien lukken. -->