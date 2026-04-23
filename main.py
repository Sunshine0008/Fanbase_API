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
