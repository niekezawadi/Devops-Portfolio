# Ap2 – Lab 4.9.2: REST API-gegevens verwerken met Python

**In één zin:** ik haal met een Python-script de volledige boekenlijst op bij de School Library API en verwerk de JSON-data verder in Python (tellen, filteren), in plaats van de JSON enkel te bekijken in de browser.

## Uitvoeren

```bash
cd ~/Devops-Portfolio/Ap2-lab-4.9.2
python3 process_books.py
```

## Wat het script doet

`requests.get()` haalt de ruwe JSON op bij `/api/v1/books`, `.json()` zet die om naar Python-lijsten/dictionaries. Daarna een `for`-lus om elk boek te tonen, en een dictionary om het aantal boeken per auteur te tellen met `.get(key, 0) + 1`.

## Resultaat

![Output van het script](img/01-output.png)

## Mogelijke vragen

**Wat is het verschil met Ap1?**
Ap1 toont de data (Swagger/Postman/terminal). Ap2 verwerkt de data in Python — tellen, groeperen — wat met een browser alleen niet lukt.

**Wat doet `r.raise_for_status()`?**
Bij een foutieve HTTP-statuscode (4xx/5xx) stopt het script direct met een duidelijke fout, in plaats van door te rekenen met foutieve data.

## Wat ik ondervond

Het grootste verschil met de vorige oefening was dat ik hier niet meer zelf naar de JSON hoefde te kijken — Python telt en groepeert voor mij via een gewone dictionary met `.get()`.
