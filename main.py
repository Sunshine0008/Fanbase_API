from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect("fanbase.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/characters")
def get_characters():
    conn = get_db()
    characters = conn.execute("SELECT * FROM characters").fetchall()
    return [dict(row) for row in characters]


@app.get("/characters/{character_id}")
def get_character(character_id: int):
    conn = get_db()
    character = conn.execute(
        "SELECT * FROM characters WHERE id = ?", (character_id,)
    ).fetchone()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    return dict(character)


@app.get("/actors")
def get_actors():
    conn = get_db()
    actors = conn.execute("SELECT * FROM actors").fetchall()
    return [dict(row) for row in actors]
