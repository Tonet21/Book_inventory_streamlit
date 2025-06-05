import streamlit as st
import os
import duckdb
from scrapper import get_book


MD_TOKEN = os.getenv("MD_TOKEN")
con = duckdb.connect(f"md:?motherduck_token={MD_TOKEN}")

st.write("Entra les dades, siusplau.")

isbn = st.text_input("ISBN: ")

lloc = st.text_input("Localització: ")

data = st.date_input("Data de publicació: ")

preu = st.number_input("Preu: ")

button = st.button("Entra les dades")

if button:

    book = get_book(isbn)
    title = book["title"]
    author = book["author"]
    con.execute(
        """
                INSERT INTO inventory.llibres (
                    ISBN, "Títol", "Autor/traductor",
                    Localització, Lloc_comprador, Datapub, Datavenda, PreuPub, Preuvenda
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
        (isbn, title, author, lloc, "on", data, data, preu, 0),  # PreuPub  # Preuvenda
    )
