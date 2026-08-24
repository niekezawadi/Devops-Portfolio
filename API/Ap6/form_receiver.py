#!/usr/bin/env python3
"""
Ap6 - Eigen REST-API experiment met curl 2 (forms)

Twee endpoints die hetzelfde doen maar een ander formaat verwachten:

  POST /book/form   verwacht  application/x-www-form-urlencoded   (curl -d "a=1&b=2")
  POST /book/json   verwacht  application/json                    (curl -d '{"a":1}')

Beide zetten het resultaat door naar de School Library API. Zo toon ik het
verschil tussen een klassieke formulier-POST en een REST-API-POST, en dat
een server allebei kan aanvaarden.

Starten:  python3 form_receiver.py     ->  http://127.0.0.1:5001
"""

import json

import requests
from flask import Flask, jsonify, request

APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

app = Flask(__name__)


def get_auth_token():
    r = requests.post(f"{APIHOST}/api/v1/loginViaBasic", auth=(LOGIN, PASSWORD), timeout=5)
    r.raise_for_status()
    return r.json()["token"]


def next_id():
    r = requests.get(f"{APIHOST}/api/v1/books", headers={"accept": "application/json"}, timeout=5)
    r.raise_for_status()
    return max((b["id"] for b in r.json()), default=-1) + 1


def store(title, author, isbn=None):
    book = {"id": next_id(), "title": title, "author": author}
    if isbn:
        book["isbn"] = isbn

    r = requests.post(
        f"{APIHOST}/api/v1/books",
        headers={"Content-type": "application/json", "X-API-Key": get_auth_token()},
        data=json.dumps(book),
        timeout=5,
    )
    r.raise_for_status()
    return book


@app.route("/book/form", methods=["POST"])
def from_form():
    """Leest uit request.form -- dat is de form-encoded body."""
    if not request.form:
        return jsonify(error="geen formuliervelden ontvangen; "
                             "gebruik curl -d \"title=...&author=...\""), 400
    title = request.form.get("title")
    author = request.form.get("author")
    if not title or not author:
        return jsonify(error="title en author zijn verplicht"), 400

    book = store(title, author, request.form.get("isbn"))
    return jsonify(bron="form-encoded", toegevoegd=book), 201


@app.route("/book/json", methods=["POST"])
def from_json():
    """Leest uit request.json -- dat is de JSON-body."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="geen geldige JSON ontvangen; "
                             "vergeet -H \"Content-Type: application/json\" niet"), 400
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify(error="title en author zijn verplicht"), 400

    book = store(title, author, data.get("isbn"))
    return jsonify(bron="json", toegevoegd=book), 201


@app.route("/", methods=["GET"])
def help_page():
    return """<pre>
Ap6 - form-encoded versus JSON

  curl -X POST http://127.0.0.1:5001/book/form \\
       -d "title=Het formulierboek&amp;author=Nieke K. Zawadi"

  curl -X POST http://127.0.0.1:5001/book/json \\
       -H "Content-Type: application/json" \\
       -d '{"title": "Het JSON-boek", "author": "Nieke K. Zawadi"}'

Verwissel de twee en je krijgt een 400 terug.
</pre>"""


if __name__ == "__main__":
    app.run(port=5001, debug=True)