import sqlite3
import os

def datu_bazes_izveide():

    # šis vajadzīgs, lai datubāze veidotos tajā directory kā pats python fails
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Datubāzes izveide, ja tā jau neeksistē
    # Saprotu, ka šis nav BCNF, bet šī programma iztiks bez starptabulām.

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produkts(
                modelis TEXT PRIMARY KEY,
                tips TEXT,
                nosaukums TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veikals(
                veikala_produkts INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                veikala_nosaukums TEXT,
                produkta_modelis TEXT,
                cena DECIMAL,
                url TEXT,
                date_checked DATETIME,
                FOREIGN KEY (produkta_modelis) REFERENCES produkts(modelis)
    )
    """)

    connection.commit()
    connection.close()