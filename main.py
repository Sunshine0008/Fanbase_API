from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI(title="BLACKPINK Fanbase API")

def get_db():
    conn = sqlite3.connect("fanbase.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS actors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        actor_id INTEGER
    )
    """)

    if conn.execute("SELECT COUNT(*) FROM actors").fetchone()[0] == 0:
        actors = ["Jisoo", "Jennie", "Rosé", "Lisa"]
        for a in actors:
            conn.execute("INSERT INTO actors (name) VALUES (?)", (a,))

        conn.execute("INSERT INTO characters (name, role, actor_id) VALUES ('Jisoo', 'Visual / Actress', 1)")
        conn.execute("INSERT INTO characters (name, role, actor_id) VALUES ('Jennie', 'Main Rapper', 2)")
        conn.execute("INSERT INTO characters (name, role, actor_id) VALUES ('Rosé', 'Main Vocalist', 3)")
        conn.execute("INSERT INTO characters (name, role, actor_id) VALUES ('Lisa', 'Main Dancer', 4)")

        conn.commit()

    conn.close()

init_db()

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>BLACKPINK Fanbase API</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                margin-top: 50px;
                background-color: #ffe4ec;
            }
            h1 {
                color: #ff1493;
            }
            button {
                padding: 10px 20px;
                margin: 10px;
                font-size: 16px;
                cursor: pointer;
            }
            ul {
                list-style: none;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <h1>BLACKPINK Fanbase API</h1>

        <button onclick="loadCharacters()">Show Characters</button>
        <button onclick="loadActors()">Show Actors</button>

        <ul id="output"></ul>

        <script>
            async function loadCharacters() {
                let res = await fetch('/characters');
                let data = await res.json();
                let output = document.getElementById('output');
                output.innerHTML = "";
                data.forEach(c => {
                    let li = document.createElement('li');
                    li.textContent = c.name + " - " + c.role;
                    output.appendChild(li);
                });
            }

            async function loadActors() {
                let res = await fetch('/actors');
                let data = await res.json();
                let output = document.getElementById('output');
                output.innerHTML = "";
                data.forEach(a => {
                    let li = document.createElement('li');
                    li.textContent = a.name;
                    output.appendChild(li);
                });
            }
        </script>
    </body>
    </html>
    """
    
@app.get("/characters")
def get_characters():
    conn = get_db()
    data = conn.execute("SELECT * FROM characters").fetchall()
    return [dict(row) for row in data]

@app.get("/characters/{character_id}")
def get_character(character_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM characters WHERE id=?", (character_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Character not found")
    return dict(row)

@app.get("/actors")
def get_actors():
    conn = get_db()
    data = conn.execute("SELECT * FROM actors").fetchall()
    return [dict(row) for row in data]
