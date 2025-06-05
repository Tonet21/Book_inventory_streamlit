import requests 

def get_book(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)

    try:
        data = response.json()
    except ValueError:
        return {"title": None, "author": None}

    book = data.get(f"ISBN:{isbn}")
    if not book:
        return {"title": None, "author": None}

    title = book.get("title", "No title")
    raw_authors = [a["name"] for a in book.get("authors", [])]
    authors = ", ".join(dict.fromkeys(raw_authors)) if raw_authors else "No authors"

    return {"title": title, "author": authors}


