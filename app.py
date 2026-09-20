import os

import psycopg
from fastapi import FastAPI

app = FastAPI()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


@app.get("/")
def root():
    return {"mensaje": "FastAPI roto"}


@app.get("/experimentos")
def obtener_experimentos():
    with psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM experimentos ORDER BY id;")
            filas = cur.fetchall()

    return [
        {"id": fila[0], "nombre": fila[1]}
        for fila in filas
    ]