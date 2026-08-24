#!/bin/bash
#
# Ap6 - de curl-commando's tegen form_receiver.py
# Start eerst in een andere terminal:  python3 form_receiver.py

HOST="http://127.0.0.1:5001"

echo "=== 1. Form-encoded POST (curl -d zonder Content-Type) ==="
curl -s -X POST "$HOST/book/form" \
     -d "title=Het formulierboek&author=Nieke K. Zawadi&isbn=978-9-000-00002-8"
echo

echo
echo "=== 2. JSON POST (met expliciete Content-Type) ==="
curl -s -X POST "$HOST/book/json" \
     -H "Content-Type: application/json" \
     -d '{"title": "Het JSON-boek", "author": "Nieke K. Zawadi"}'
echo

echo
echo "=== 3. Tegenproef: JSON naar het form-endpoint sturen ==="
curl -s -X POST "$HOST/book/form" \
     -H "Content-Type: application/json" \
     -d '{"title": "Verkeerd formaat", "author": "Niemand"}'
echo

echo
echo "=== 4. Tegenproef: form-data naar het JSON-endpoint sturen ==="
curl -s -X POST "$HOST/book/json" \
     -d "title=Ook verkeerd&author=Niemand"
echo

echo
echo "=== 5. Wat gaat er precies over de lijn? (-v toont de headers) ==="
curl -v -X POST "$HOST/book/form" \
     -d "title=Zichtbaar in de header&author=Nieke K. Zawadi" 2>&1 | grep -Ei "^> (POST|Content-Type|Content-Length)|^< HTTP"
echo