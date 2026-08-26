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
