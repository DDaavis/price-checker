import sqlite3
from datetime import datetime
import getprice
import os

# Paredzēts datu ievietošanai kad ar UI tiek pievienots produkts
def datu_ievietosana_kad_pievieno(nosaukums, tips, veikala_nosaukums, url):

    # Savienošanās ar datubāzi:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:

        nosaukums_bez_atstarpem = nosaukums.replace(" ", "") # Izņemu atstarpes no nosaukuma, lai produktam varētu piešķirt primary key
        modelis = nosaukums_bez_atstarpem+veikala_nosaukums # Kad atstarpes ir izņemtas, drošības pēc vēl beigās string-am pievienoju klāt string 'id'
        produkta_modelis = modelis
        date_checked = datetime.now() # Datuma un laika iegūšana

        cena = getprice.cenu_iegusana_tagad(veikala_nosaukums, url)
        # Datu ievietošana datubāzē:

        cursor.execute("""
        INSERT OR REPLACE INTO produkts(modelis, tips, nosaukums)
        VALUES(?,?,?)""", (modelis, tips, nosaukums,))

        cursor.execute("""
        INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
        VALUES(?,?,?,?,?)""", (veikala_nosaukums, produkta_modelis, cena, url, date_checked,))


# Paredzēts kad no UI izvēlas iegūt visu preču cenas - šis ievietos jaunos datus DB
def datu_ievietosana_visi_produkti():

    # Savienošanās ar datubāzi:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection: # beigās nebūs nepieciešams pievienot connection.commit() un connection.close()
        
        # Savāks katra produkta info, bet lai produkti neatkārtotos* (zemāk) - sagrupēju pēc produktaNosaukums + veikalaNosaukums
        # Datu atkārtošanās var notikt tikai tad, ja no konkrēta produkta ir iegūti dažādu datumu un laiku dati, tāpēc tie ir jāgrupē
        cursor.execute(""" 
            SELECT *
            FROM produkts
            INNER JOIN (
                SELECT * FROM veikals
                GROUP BY produkta_modelis 
            ) veikals ON produkts.modelis = veikals.produkta_modelis ORDER BY veikala_produkts ASC """)

        rows = cursor.fetchall() # Iegūs visas rindas
        oldRow = ''

        for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

            # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
            # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
            
            # if oldRow == row[2]: pass
            # else: print(row[2])
            # print('\t Veikals:', row[4], 'Cena: ', row[6], 'Eur')
            # oldRow = row[2]
            
            date_checked = datetime.now()

            veikals = row[4]
            url = row[7]
            produkta_modelis = row[5]
            produkta_nosaukums = row[2]
            produkta_tips = row[1]

            price = getprice.cenu_iegusana_tagad(veikals, url)

            cursor.execute("""
            INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES(?,?,?,?,?)""", (veikals, produkta_modelis, price, url, date_checked,))

            # print('Inserted price from ', veikals)

            # return(produkta_nosaukums, produkta_tips, veikals, price, date_checked)

            # karoche to do:
            # ievietot for loop kas ievietos datus 2D masiva vai nu labak to loop kaut ka izveidot funkcijas izsauksana,
            # kur funkcija iteres tik ilgi kamer dabus katru url
            # varbut pat nevajag return?