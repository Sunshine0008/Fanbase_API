from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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
        name TEXT,
        nationality TEXT,
        age INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        bio TEXT,
        actor_id INTEGER
    )
    """)

    if conn.execute("SELECT COUNT(*) FROM actors").fetchone()[0] == 0:
        # Actors
        conn.execute("INSERT INTO actors VALUES (1,'Jisoo','South Korean',29)")
        conn.execute("INSERT INTO actors VALUES (2,'Jennie','South Korean',28)")
        conn.execute("INSERT INTO actors VALUES (3,'Rosé','New Zealand / Korean',27)")
        conn.execute("INSERT INTO actors VALUES (4,'Lisa','Thai',27)")

        # Characters (Fanbase-style roles)
        conn.execute("""
        INSERT INTO characters VALUES 
        (1,'Jisoo','Visual / Actress',
        'Kim Jisoo is known for her elegant visuals and calm personality. She debuted with BLACKPINK in 2016 and later pursued acting.',
        1)
        """)

        conn.execute("""
        INSERT INTO characters VALUES 
        (2,'Jennie','Main Rapper',
        'Jennie Kim is recognized for her charisma and fashion influence. She trained for years before debut and became a global icon.',
        2)
        """)

        conn.execute("""
        INSERT INTO characters VALUES 
        (3,'Rosé','Main Vocalist',
        'Rosé Park is famous for her unique voice and emotional singing style. She grew up in New Zealand and Australia.',
        3)
        """)

        conn.execute("""
        INSERT INTO characters VALUES 
        (4,'Lisa','Main Dancer',
        'Lalisa Manobal is known for her powerful dance skills and stage presence. She is the first non-Korean idol under YG Entertainment.',
        4)
        """)

        conn.commit()

    conn.close()

init_db()

# --- API ROUTES ---

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

# --- UI ---

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>BLACKPINK Fanbase</title>
        <style>
            body {
                font-family: Arial;
                background-color: #ffe4ec;
                text-align: center;
            }
            h1 { color: #ff1493; }
            button {
                padding: 10px;
                margin: 10px;
                cursor: pointer;
            }
            .card {
                background: white;
                margin: 10px auto;
                padding: 15px;
                width: 300px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <h1>BLACKPINK Fanbase</h1>

        <button onclick="loadCharacters()">Show Characters</button>
        <button onclick="loadActors()">Show Actors</button>

        <div id="output"></div>

        <script>
            async function loadCharacters() {
                let res = await fetch('/characters');
                let data = await res.json();
                let output = document.getElementById('output');
                output.innerHTML = "";

                data.forEach(c => {
                    let div = document.createElement('div');
                    div.className = "card";
                    div.innerHTML = `
                        <h3>${c.name}</h3>
                        <p><b>Role:</b> ${c.role}</p>
                        <p>${c.bio}</p>
                    `;
                    output.appendChild(div);
                });
            }

            async function loadActors() {
                let res = await fetch('/actors');
                let data = await res.json();
                let output = document.getElementById('output');
                output.innerHTML = "";

                data.forEach(a => {
                    let div = document.createElement('div');
                    div.className = "card";
                    div.innerHTML = `
                        <h3>${a.name}</h3>
                        <p><b>Nationality:</b> ${a.nationality}</p>
                        <p><b>Age:</b> ${a.age}</p>
                    `;
                    output.appendChild(div);
                });
            }
        </script>
    </body>
    </html>
    """
