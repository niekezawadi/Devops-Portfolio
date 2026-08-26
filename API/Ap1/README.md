# 1. Ap1 – School Library API

**Pad:** `~/Devops-Portfolio/Ap1-school-library/README.md`

```markdown
# Ap1 – Lab 4.5.5 Explore REST APIs with API Simulator and Postman

**In één zin:** ik bevraag dezelfde REST-API op vier manieren — via de OpenAPI-documentatie, via curl, via Postman, en via een Python-script — om te tonen dat een API losstaat van de tool waarmee je hem aanspreekt.

**Omgeving:** DEVASC VM · API-simulator op `http://library.demo.local` · namespace `/api/v1`

---

## De API in het kort

Zes endpoints, zichtbaar op `library.demo.local/api/v1/docs`:

```
GET    /books           lijst van boeken          open
POST   /books           boek toevoegen            slot
DELETE /books/{id}      boek verwijderen          slot
GET    /books/{id}      één boek opvragen         open
PUT    /books/{id}      boek wijzigen             slot
POST   /loginViaBasic   token ophalen             open
```

Het slotje betekent: dit endpoint vraagt een token. Lezen mag iedereen, schrijven niet.

![Overzicht van de endpoints](img/00-endpoints.png)

---

## 1 · Lijst opvragen via de documentatie

Bij `GET /books` op **Try it out** → **Execute**, zonder parameters.

Resultaat: **200** en vier boeken in JSON.

![GET /books](img/01-get-books.png)

De docs tonen onder Responses ook het curl-commando en de Request URL. Die twee gebruik ik straks opnieuw in de terminal en in Postman.

## 2 · Parameters gebruiken

`GET /books` heeft vier optionele parameters: `includeISBN`, `sortBy`, `author`, `page`.

Met `includeISBN=true` → dezelfde vier boeken, nu met een `isbn`-veld erbij. De URL wordt:

```
http://library.demo.local/api/v1/books?includeISBN=true
```

![GET /books met includeISBN](img/02-includeisbn.png)

Parameters zitten achter het vraagteken in de URL, gescheiden door `&`. De server bepaalt welke hij aanvaardt.

## 3 · Dezelfde call via curl

```bash
curl -X GET "http://library.demo.local/api/v1/books" -H "accept: application/json"
```

![curl in de terminal](img/03-curl.png)

Exact dezelfde JSON als in de browser. `-X` is de HTTP-methode, `-H` zet een header — hier zeg ik dat ik JSON terug wil.

## 4 · Token ophalen

`POST /loginViaBasic` → **Execute** → inloggen met `cisco` / `Cisco123!`.

De response bevat een token. Die kopieer ik en plak ik bovenaan bij **Authorize**, onder de naam `X-API-KEY`.

![Token](img/04-token.png)

Vanaf nu zijn de sloten open en werken POST en DELETE.

## 5 · Boeken toevoegen

Bij `POST /books` vraagt de payload om JSON:

```json
{ "id": 4, "title": "IPv6 Fundamentals", "author": "Rick Graziani" }
```

Daarna hetzelfde met id 5, "31 Days Before Your CCNA Exam" van Allan Johnson. Beide → **200**.

![POST /books](img/05-post.png)

## 6 · Eén boek opvragen en verwijderen

`GET /books/{id}` met id 4 → dat ene boek.
`DELETE /books/{id}` met id 4 → 200, en bij een nieuwe `GET /books` is id 4 weg. Id 5 staat er nog.

![DELETE](img/06-delete.png)

---

## 7 · Alles opnieuw, nu in Postman

Drie requests aangemaakt:

**GET** `http://library.demo.local/api/v1/books` — geen authenticatie nodig.

**POST** `.../loginViaBasic` — tabblad Authorization → type **Basic Auth** → `cisco` / `Cisco123!` → Send → token in de body.

**POST** `.../books` — tabblad Authorization → type **API Key** → Key `X-API-KEY`, Value = de token. Tabblad Body → **raw** → **JSON** → het boek erin.

![Postman](img/07-postman.png)

Query parameters gaan in Postman via het tabblad **Params**: `includeISBN=true` en `sortBy=author`. Postman bouwt de URL dan zelf op:

```
http://library.demo.local/api/v1/books?includeISBN=true&sortBy=author
```

Het verschil met de docs: in Postman blijven mijn requests bewaard en kan ik ertussen springen.

---

## 8 · 100 boeken toevoegen met Python

`add100RandomBooks.py` in `~/labs/devnet-src/school-library/`

Twee functies. `getAuthToken()` doet dezelfde POST naar `/loginViaBasic` en geeft de token terug. `addBook()` doet de POST naar `/books`, met de token in de header:

```python
r = requests.post(
    f"{APIHOST}/api/v1/books",
    headers = {"Content-type": "application/json",
               "X-API-Key": apiKey},
    data = json.dumps(book)
)
```

Daarna een lus die honderd keer een boek verzint met de `faker`-library — `catch_phrase()` als titel, `name()` als auteur, `isbn13()` als ISBN — en telkens `addBook()` aanroept:

```python
for i in range(4, 104):
    book = {"id": i, "title": fake.catch_phrase(),
            "author": fake.name(), "isbn": fake.isbn13()}
    addBook(book, apiKey)
```

```bash
python3 add100RandomBooks.py
```

![Output van het script](img/08-python.png)
![De website met 100 nieuwe boeken](img/09-website.png)

---

## Vragen die kunnen komen

**Waarom eerst een token?**
POST, DELETE en PUT wijzigen data, GET niet. Alleen de schrijf-endpoints zijn beveiligd.

**Wat is het verschil tussen de docs, curl, Postman en Python?**
Niets aan de kant van de server — het zijn vier clients die dezelfde HTTP-requests sturen. De docs zijn om te verkennen, curl om snel iets te testen, Postman om requests te bewaren en te hergebruiken, Python om te automatiseren.

**Wat betekent 200 / 401 / 404?**
200 gelukt, 401 niet geauthenticeerd, 404 niet gevonden.

**Waar staat de token precies?**
In een HTTP-header, `X-API-Key`. Niet in de URL, want een URL wordt gelogd.

**Nog 100 boeken toevoegen?**
`range(104, 204)` — de id's moeten uniek blijven. Beter nog: de start- en eindwaarde als argument aan het script meegeven in plaats van hard te coderen.

**Waarom `json.dumps(book)`?**
`book` is een Python-dictionary. De API verwacht JSON als tekst, dus die moet eerst omgezet worden.

---

## Wat ik ondervond

Het lastigste was het verschil tussen `/loginViaBasic` en de manier waarop Postman met Basic Auth omgaat goed te zien: ik dacht eerst dat ik verkeerd was ingelogd omdat de token er in Postman anders uitzag dan in Swagger, maar het bleek gewoon hetzelfde token, enkel anders weergegeven. Verder liep de volledige CRUD-flow — token ophalen, boek toevoegen, controleren, verwijderen, opnieuw controleren — in één keer goed, en het Python-script met 100 boeken was een leuke bevestiging dat alles wat ik manueel deed ook automatisch kan.
```

---
