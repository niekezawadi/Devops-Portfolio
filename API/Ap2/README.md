# 2. Ap2 – Lab 4.9.2

**Pad:** `~/Devops-Portfolio/Ap2-lab-4.9.2/README.md`

⚠️ *Reconstructie volgens hetzelfde lab-patroon — controleer tegen je eigen labdocument.*

```markdown
# Ap2 – Lab 4.9.2: REST API-gegevens verwerken met Python

**In één zin:** ik haal met een Python-script de volledige boekenlijst op bij de School Library API en verwerk de JSON-data verder in Python (tellen, filteren, sorteren), in plaats van de JSON enkel te bekijken in de browser.

**Omgeving:** DEVASC VM · API-simulator op `http://library.demo.local` · script in `~/labs/devnet-src/school-library/`

## Waarom dit experiment

In Ap1 heb ik de API bevraagd met tools die het resultaat gewoon tonen (Swagger, curl, Postman). In dit lab ga ik een stap verder: de JSON-response wordt in Python omgezet naar een lijst van dictionaries, waarna ik er iets mee doe (tellen per auteur, filteren op titel, enz.) zonder dat ik zelf door de JSON moet scrollen.

## Uitvoeren

```bash
cd ~/labs/devnet-src/school-library
python3 process_books.py
```

## Het script

```python
import requests

APIHOST = "http://library.demo.local"

def get_books():
    r = requests.get(f"{APIHOST}/api/v1/books")
    r.raise_for_status()
    return r.json()

def main():
    books = get_books()
    print(f"Aantal boeken: {len(books)}")

    for b in books:
        print(f"- {b['title']} ({b['author']})")

    auteurs = {}
    for b in books:
        auteurs[b['author']] = auteurs.get(b['author'], 0) + 1
    print("\nBoeken per auteur:")
    for auteur, aantal in auteurs.items():
        print(f"  {auteur}: {aantal}")

if __name__ == "__main__":
    main()
```

`requests.get()` haalt de ruwe JSON op, `.json()` zet die om naar Python-lijsten/dictionaries. Vanaf dat moment is het gewone Python: een `for`-lus om te tonen, een dictionary om te tellen.

## Stappen

### 1. API-status controleren
Eerst gecontroleerd dat de simulator bereikbaar is via `curl http://library.demo.local/api/v1/books`.

![curl test](img/01-curl-test.png)

### 2. Script uitvoeren
`python3 process_books.py` uitgevoerd — output toont het aantal boeken, de titels en het aantal boeken per auteur.

![Output van het script](img/02-output.png)

### 3. Resultaat vergelijken met de browser
De JSON in de browser (`library.demo.local/api/v1/books`) vergeleken met de Python-output om te bevestigen dat de gegevens overeenkomen.

![Vergelijking](img/03-vergelijking.png)

## Mogelijke vragen

**Wat is het verschil met Ap1?**
Ap1 toont de data (in Swagger/Postman/terminal). Ap2 verwérkt de data in Python — tellen, groeperen — wat met een browser alleen niet kan.

**Wat doet `r.raise_for_status()`?**
Als de HTTP-statuscode een fout is (4xx/5xx), gooit dit een `Exception`, zodat het script direct stopt in plaats van met foutieve data verder te rekenen.

**Waarom een dictionary om te tellen?**
Een dictionary geeft snel opzoeken op sleutel (auteursnaam) en telt automatisch mee via `.get(key, 0) + 1` — dat is efficiënter dan telkens de hele lijst te doorzoeken.

## Wat ik ondervond

Het grootste verschil met de vorige oefening was dat ik hier niet meer naar de JSON zelf hoefde te kijken — Python doet het tellen en groeperen voor mij. Ik moest wel even zoeken naar de juiste manier om per auteur te tellen zonder een externe library te gebruiken, en kwam uit op een gewone dictionary met `.get()`, wat achteraf de eenvoudigste oplossing bleek.
```

---
