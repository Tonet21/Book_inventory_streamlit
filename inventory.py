import streamlit as st
import os
import duckdb
from scrapper import get_book


MD_TOKEN = os.getenv("MD_TOKEN")
con = duckdb.connect(f"md:?motherduck_token={MD_TOKEN}")

mode = st.radio("Selecciona acció:", ["Afegir entrada", "Modificar entrada"])

if mode == "Afegir entrada":

    
    for key in ["isbn", "lloc", "data", "preu", "title", "author", "data_entered"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.write("Entra les dades, siusplau.")

    
    st.session_state.isbn = st.text_input("ISBN:", value=st.session_state.isbn or "")
    st.session_state.lloc = st.text_input(
        "Localització:", value=st.session_state.lloc or ""
    )
    st.session_state.data = st.date_input(
        "Data de publicació:", value=st.session_state.data or None
    )
    st.session_state.preu = st.number_input("Preu:", value=st.session_state.preu or 0.0)

    
    if st.button("Entra les dades"):
        book = get_book(st.session_state.isbn)
        st.session_state.title = book["title"]
        st.session_state.author = book["author"]
        st.session_state.data_entered = True

    
    if st.session_state.data_entered:
        if not st.session_state.title or st.session_state.title == "Títol desconegut":
            st.warning("No s'ha trobat el títol.")
            st.session_state.title = st.text_input("Títol:", key="manual_title")

        else:
            st.write(f"**Títol detectat:** {st.session_state.title}")

        if not st.session_state.author or st.session_state.author == "Autor desconegut":
            st.warning("No s'ha trobat l'autor.")
            st.session_state.author = st.text_input(
                "Autor/Traductor:", key="manual_author"
            )
        else:
            st.write(f"**Autor detectat:** {st.session_state.author}")

        if st.button("Confirma les dades."):
            try:
                con.execute(
                    """
                INSERT INTO inventory.llibres (
                    ISBN, "Títol", "Autor/traductor",
                    Localització, Lloc_comprador, Datapub, Datavenda, PreuPub, Preuvenda
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        st.session_state.isbn,
                        st.session_state.title,
                        st.session_state.author,
                        st.session_state.lloc,
                        "ciutat",
                        st.session_state.data,
                        st.session_state.data,
                        st.session_state.preu,
                        0,
                    ),
                )
                st.success("Taula actualitzada")

                # Reset session state
                for key in [
                    "isbn",
                    "lloc",
                    "data",
                    "preu",
                    "title",
                    "author",
                    "data_entered",
                ]:
                    st.session_state[key] = None

            except Exception as e:
                st.error(f"Hi ha hagut un error: {e}")

    # Show table
    with st.expander("Taula actual"):
        df = con.execute("SELECT * FROM inventory.llibres ORDER BY ID ASC").df()
        st.dataframe(df)

else:

    title = st.text_input("Títol: ")

    if title:

        results = con.execute(
            """
        SELECT ID, ISBN, "Títol", "Autor/traductor"
        FROM inventory.llibres
        WHERE "Títol" ILIKE ?
    """,
            (f"%{title}%",),
        ).fetchall()

        options = {f"{row[2]} — {row[1]} ({row[3]})": row[0] for row in results}
        selected = st.selectbox(
            "Selecciona l'entrada a modificar:", [""] + list(options.keys())
        )

        if selected:
            selected_id = options[selected]
            current = con.execute(
                """
            SELECT ISBN, "Títol", "Autor/traductor", Localització, Lloc_comprador, 
                Datapub, Datavenda, PreuPub, Preuvenda
            FROM inventory.llibres
            WHERE ID = ?
            """,
                (selected_id,),
            ).fetchone()
            new_local = st.text_input("Nova localització:", value=current[3])
            new_buyer = st.text_input("Nou lloc comprador:", value=current[4])
            new_datavenda = st.date_input("Nova data de venda:", value=current[6])
            new_preuvenda = st.number_input(
                "Nou preu de venda:", value=float(current[8])
            )

            if st.button("Guardar canvis"):
                con.execute(
                    """
                UPDATE inventory.llibres
                SET Localització = ?, Lloc_comprador = ?, Datavenda = ?, Preuvenda = ?
                WHERE ID = ?
                """,
                    (new_local, new_buyer, new_datavenda, new_preuvenda, selected_id),
                )
                st.success("Entrada modificada correctament.")
            with st.expander("Taula actual"):
                df = con.execute("SELECT * FROM inventory.llibres ORDER BY ID ASC").df()
                st.dataframe(df)
        else:
            st.info("No s'ha trobat cap llibre amb aquest títol.")
