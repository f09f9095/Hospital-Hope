import sqlite3 as sql

from src.dictionary import ROOT


def db_connect(db):
    try:
        conn = sql.connect(ROOT / db)
    except sql.DatabaseError as e:
        print(e)
        conn = None
    return conn