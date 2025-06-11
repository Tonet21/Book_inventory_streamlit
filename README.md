# Book_inventory_streamlit

This is a simple web application built with **Streamlit** to manage a personal book inventory. It allows you to:

-  Add new book entries by fetching data from the Open Library API using the ISBN
-  Manually modify existing entries
-  Store and query all data using **DuckDB** with **MotherDuck** as the backend



##  Features

- Fetch book metadata (title, author) automatically using an ISBN
- Insert missing metadata manually when needed
- Modify fields like location, purchase place, sale date, and sale price
- View the entire inventory in an interactive table



##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/book-inventory-app.git
cd book-inventory-app
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Set Up Your MotherDuck Token

You must store your **MotherDuck token** as a Streamlit secret or environment variable.  
To do so, create a `.streamlit/secrets.toml` file with the following:

```toml
MD_TOKEN = "your_motherduck_token_here"
```

Alternatively, set it in your environment:

```bash
export MD_TOKEN="your_motherduck_token_here"
```

>  **Reminder:** Make sure your `.gitignore` includes `.streamlit/secrets.toml` to keep your token private.



## Database Schema

Here’s the SQL used to create the table used in this app:

```sql
CREATE SCHEMA IF NOT EXISTS inventory;

CREATE SEQUENCE IF NOT EXISTS llibres_id_seq;
CREATE TABLE IF NOT EXISTS  inventory.llibres (
  ID INTEGER PRIMARY KEY DEFAULT nextval('llibres_id_seq'),
  ISBN VARCHAR,
  "Títol" VARCHAR,
  "Autor/traductor" VARCHAR,
  Localització VARCHAR,
  Lloc_comprador VARCHAR,
  Datapub DATE,
  Datavenda DATE,
  PreuPub DECIMAL(10,2),
  Preuvenda DECIMAL (10,2)
);
```



##  Running the App

Run the Streamlit app locally:

```bash
streamlit run inventory.py
```



##  Notes

- This app was designed for personal use and learning purposes.
- It demonstrates integration between Streamlit, DuckDB, and an external book metadata API.
- Deployment is not enabled by default but could be added later using Streamlit Cloud, Hugging Face Spaces, or similar.