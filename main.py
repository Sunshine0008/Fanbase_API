from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect("quotes.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
    )
    """)

    if conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0] == 0:
        conn.execute("INSERT INTO quotes (text) VALUES ('Stay hungry, stay foolish.')")
        conn.execute("INSERT INTO quotes (text) VALUES ('Talk is cheap. Show me the code.')")
        conn.execute("INSERT INTO quotes (text) VALUES ('Programs must be written for people to read.')")
        conn.commit()

    conn.close()

init_db()

@app.get("/quotes")
def get_quotes():
    conn = get_db()
    data = conn.execute("SELECT * FROM quotes").fetchall()
    return [dict(row) for row in data]

@app.get("/quotes/{quote_id}")
def get_quote(quote_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM quotes WHERE id=?", (quote_id,)).fetchone()
    if row:
        return dict(row)
    return {"error": "Not found"}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Quote API</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; }
            button { padding: 10px 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Quote API</h1>
        <button onclick="loadQuotes()">Load Quotes</button>
        <ul id="quotes"></ul>

        <script>
            async function loadQuotes() {
                let res = await fetch('/quotes');
                let data = await res.json();
                let list = document.getElementById('quotes');
                list.innerHTML = "";
                data.forEach(q => {
                    let li = document.createElement('li');
                    li.textContent = q.text;
                    list.appendChild(li);
                });
            }
        </script>
    </body>
    </html>
    """
