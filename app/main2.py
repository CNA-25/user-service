from fastapi import FastAPI
import os, psycopg
from psycopg.rows import dict_row

app = FastAPI()

print(os.environ.get('DB_URL'))

try:
    conn = psycopg.connect(os.environ.get('DB_URL'), autocommit=True, row_factory=dict_row)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS foo ( id SERIAL PRIMARY KEY );
            ALTER TABLE foo ADD COLUMN IF NOT EXISTS name VARCHAR;
            ALTER TABLE foo ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT now()""")
    
except Exception as e:
    print(e)

@app.get("/")
def read_root():
    return { "Hello": "Rahti2", "v": "0.5" }


@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}


@app.get("/db")
def read_db():
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO foo (name) VALUES ('test')""")
        cur.execute("""SELECT *, version() FROM foo ORDER BY id DESC LIMIT 10""")
        return cur.fetchall()