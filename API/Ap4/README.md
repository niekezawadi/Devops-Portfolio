# Ap4 – Eigen API-experiment 2 (Python, webforms)

**In één zin:** dezelfde weerapplicatie als Ap3, maar de gebruiker vult nu een HTML-formulier in plaats van vragen in de terminal te beantwoorden.

## Waarom dit experiment

Ap3 draait in de terminal en gebruikt `input()`. Dat werkt, maar alleen voor wie een terminal openzet. Ik wilde weten wat er verandert als dezelfde logica achter een webpagina komt — en het antwoord is: verrassend weinig. De API-calls, de foutafhandeling en de verwerking blijven identiek. Alleen de bron van de invoer verandert.

```python
# Ap3
plaats = input("Plaats: ")

# Ap4
plaats = request.form.get("plaats", "").strip()
```

## Uitvoeren

```bash
pip3 install flask requests
python3 ap4_app.py
```

Open daarna `http://127.0.0.1:5000` in Chromium.

![Het formulier](screenshots/01-formulier.png)
![Resultaat met voorspelling](screenshots/02-resultaat.png)
![Onbestaande plaats](screenshots/03-fout.png)

## Structuur

```
Ap4/
├── ap4_app.py
├── templates/
│   └── index.html
└── screenshots/
```

De map moet **templates** heten. Flask zoekt daar automatisch, en `render_template("index.html")` werkt niet als het bestand ergens anders staat.

## Het formulier

Drie verschillende soorten velden, om te tonen hoe Flask elk uitleest:

| Veld | HTML | Uitlezen in Python |
|---|---|---|
| Plaats | `<input type="text" name="plaats" required>` | `request.form.get("plaats")` |
| Eenheid | `<select name="eenheid">` met twee opties | `request.form.get("eenheid")` |
| Voorspelling | `<input type="checkbox" name="voorspelling" value="ja">` | `request.form.get("voorspelling") == "ja"` |

Het aankruisvakje werkt anders dan de andere twee: **een niet-aangevinkt vakje wordt helemaal niet meegestuurd.** Er komt dus geen `False` binnen, er komt niets binnen. Daarom vergelijk ik met de waarde `"ja"` in plaats van te controleren of de sleutel bestaat.

## Eén route, twee methodes

```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ...
```

Bij een **GET** — iemand opent de pagina — tonen we het lege formulier. Bij een **POST** — het formulier is verzonden — zit de invoer in `request.form` en verwerken we die. Beide gevallen renderen hetzelfde sjabloon; alleen de meegegeven variabelen verschillen.

## De ingevulde waarden blijven staan

Na het verzenden geef ik `request.form` terug aan het sjabloon:

```python
return render_template("index.html", resultaat=..., fout=..., ingevuld=request.form)
```

In de HTML gebruik ik dat om de velden opnieuw te vullen:

```html
<input type="text" name="plaats" value="{{ ingevuld.get('plaats', '') }}">
```

Zonder dat staat het formulier na elke zoekopdracht weer leeg en moet de gebruiker alles opnieuw typen. Kleine moeite, groot verschil in bruikbaarheid.

## Foutafhandeling

Drie gevallen worden op de pagina getoond in plaats van in een stacktrace:

| Situatie | Melding |
|---|---|
| leeg veld | "Vul een plaatsnaam in." |
| onbekende plaats | "Geen plaats gevonden met de naam '…'." |
| geen verbinding | "Geen verbinding met de weerdienst." |

Het `required`-attribuut in de HTML vangt het lege veld al af in de browser, maar ik controleer het óók in Python. Een browser kan die controle overslaan, en wie rechtstreeks een POST stuurt met curl heeft er sowieso geen last van. Validatie in de browser is gemak; validatie op de server is beveiliging.

## Mogelijke vragen

**Waarom POST en niet GET?**
Een zoekopdracht is strikt genomen een GET — je verandert niets aan de server, en met GET zou de plaatsnaam in de URL staan, wat je kunt bookmarken en delen. Ik koos POST omdat de opdracht over webformulieren gaat en `request.form` daar het duidelijkst is. In een echte toepassing zou GET hier verdedigbaar zijn.

**Waarom `.strip()`?**
Spaties voor en na weghalen. Zonder dat glipt " " door de `required`-controle van de browser.

**Wat doet `{{ }}` in het HTML-bestand?**
Dat is Jinja2, de sjabloontaal van Flask. Wat daartussen staat wordt op de server vervangen door de echte waarde vóór de pagina naar de browser gaat.

**Waarom `host="0.0.0.0"`?**
Dan luistert de server op alle netwerkinterfaces van de VM, niet alleen op localhost. Handig als je vanaf je laptop naar de VM wil surfen.

**Wat betekent `debug=True`?**
De server herstart automatisch bij een wijziging en toont fouten in de browser. Handig tijdens het bouwen, maar uit te zetten in productie — die foutpagina toont je broncode.

## Verschil met Ap3

| | Ap3 | Ap4 |
|---|---|---|
| Invoer | `input()` in de terminal | HTML-formulier |
| Uitvoer | `print()` | HTML-pagina |
| Herhalen | `while True`-lus | opnieuw op de knop duwen |
| Stoppen | `q` of `quit` | tabblad sluiten |
| Extra keuzes | — | eenheid en zevendaagse voorspelling |
| API-calls | identiek | identiek |

Die laatste rij is het punt van dit experiment: de manier waarop je een API aanspreekt verandert niet met de schil eromheen.

## Wat ik ondervond

Het omzetten van mijn terminal-script naar een webformulier ging vlotter dan verwacht omdat de kernfunctie (`get_coordinates`/`get_weather`) ongewijzigd kon blijven — enkel de manier waarop de input binnenkomt (`request.form` in plaats van `sys.argv`) en de output getoond wordt (HTML-template in plaats van `print()`) veranderde. De Fahrenheit-omrekening toevoegen was een leuke extra die me deed nadenken over waar in de applicatie zo'n omzetting eigenlijk thuishoort.
```
