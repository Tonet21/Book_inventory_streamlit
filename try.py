import streamlit as st
import os
import duckdb
from scrapper import get_book


MD_TOKEN = os.getenv("MD_TOKEN")
con = duckdb.connect(f"md:?motherduck_token={MD_TOKEN}")
mode = st.radio("Selecciona acció:", ["Afegir entrada", "Modificar entrada"])

if mode == "Afegir entrada":

    st.write("Entra les dades, siusplau.")

    isbn = st.text_input("ISBN: ")
    lloc = st.text_input("Localització: ")
    data = st.date_input("Data de publicació:")
    preu = st.number_input("Preu:")

    button = st.button("Entra les dades")

    if button and isbn:
        book = get_book(isbn)
        title = book["title"]
        author = book["author"]

        # 1. INSERT INTO TABLE
        try:
            con.execute(
                """
                INSERT INTO inventory.llibres (
                    ISBN, "Títol", "Autor/traductor",
                    Localització, Lloc_comprador, Datapub, Datavenda, PreuPub, Preuvenda
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (isbn, title, author, lloc, "ciutat", data, data, preu, 0),
            )
            st.success("Entrada afegida a la taula.")
        except Exception as e:
            st.error(f"Error a l'inserir: {e}")

        # 2. CHECK IF MANUAL INPUT IS NEEDED
        if title == "Títol desconegut" or author == "Autor desconegut":
            st.warning("Falten metadades. Introdueix-les manualment.")

            manual_title = st.text_input("Títol corregit:", value="" if title == "Títol desconegut" else title)
            manual_author = st.text_input("Autor/traductor corregit:", value="" if author == "Autor desconegut" else author)

            if st.button("Actualitza entrada"):
                try:
                    con.execute(
                        """
                        UPDATE inventory.llibres
                        SET "Títol" = ?, "Autor/traductor" = ?
                        WHERE ISBN = ?
                        """,
                        (manual_title, manual_author, isbn),
                    )
                    st.success("Entrada actualitzada correctament.")
                except Exception as e:
                    st.error(f"Error a l'actualitzar: {e}")

    # 3. SHOW TABLE
    with st.expander("Taula actual"):
        df = con.execute("SELECT * FROM inventory.llibres ORDER BY ID ASC").df()
        st.dataframe(df)
