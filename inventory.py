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

    data = st.date_input("Data de publicació: ")

    preu = st.number_input("Preu: ")

    button = st.button("Entra les dades")

    if button:

        book = get_book(isbn)
        title = book["title"]
        author = book["author"]
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
            st.success("Taula actualitzada")

        except Exception as e:
            st.error(f"Hi ha hagut un error: {e}")
        
## mirar si puc mirar a la taula que si el valor es none el poso manualmet
    with st.expander("Taula actual"):
        df = con.execute("SELECT * FROM inventory.llibres ORDER BY ID ASC").df()
        st.dataframe(df)

else:

    title = st.text_input("Títol: ")

    if title:

        results = con.execute("""
        SELECT ID, ISBN, "Títol", "Autor/traductor"
        FROM inventory.llibres
        WHERE "Títol" ILIKE ?
    """, (f"%{title}%",)).fetchall()

        options = {f"{row[2]} — {row[1]} ({row[3]})": row[0] for row in results}
        selected = st.selectbox("Selecciona l'entrada a modificar:", [""] + list(options.keys()))

        if selected:
            selected_id = options[selected]
            current = con.execute("""
            SELECT ISBN, "Títol", "Autor/traductor", Localització, Lloc_comprador, 
                Datapub, Datavenda, PreuPub, Preuvenda
            FROM inventory.llibres
            WHERE ID = ?
            """, (selected_id,)).fetchone()
            new_local = st.text_input("Nova localització:", value=current[3])
            new_buyer = st.text_input("Nou lloc comprador:", value=current[4])
            new_datavenda = st.date_input("Nova data de venda:", value=current[6])
            new_preuvenda = st.number_input("Nou preu de venda:", value=float(current[8]))

            if st.button("Guardar canvis"):
                con.execute("""
                UPDATE inventory.llibres
                SET Localització = ?, Lloc_comprador = ?, Datavenda = ?, Preuvenda = ?
                WHERE ID = ?
                """, (new_local, new_buyer, new_datavenda, new_preuvenda, selected_id))
                st.success("Entrada modificada correctament.")
            with st.expander("Taula actual"):
                df = con.execute("SELECT * FROM inventory.llibres ORDER BY ID ASC").df()
                st.dataframe(df)
        else:
            st.info("No s'ha trobat cap llibre amb aquest títol.")       

