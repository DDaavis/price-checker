import helpers
import sqlite3
import os
from datetime import datetime

# Paredzēts aktīvās cenas iegūšanai
def cenu_iegusana_tagad(veikals, url):
            
    price = helpers.get_price_methods_dynamic(veikals,url)
    price = price.replace(' ', '')

    # cursor.execute("""
    # INSERT INTO veikals(veikala_produkts, veikala_nosaukums, produkta_modelis, cena, url, date_checked)
    # VALUES(?,?,?,?,?,?)""", (row[3]+dateString, row[4], row[5], price, row[7], datetime.now()))

    return price

# Paredzēts tūlītējas cenas iegūšanai kad tiek pievienots jauns produkts
def cenu_iegusana_kad_pievieno():
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:
        cursor.execute(""" 
        SELECT *
        FROM produkts
        INNER JOIN veikals ON produkts.modelis = veikals.produkta_modelis ORDER BY veikala_produkts DESC""")

        rows = cursor.fetchall()

        for row in rows:

            url = row[7]
            veikals = row[4]
            price = helpers.get_price_methods_dynamic(veikals,url)

            # # cursor.execute("""
            # # INSERT INTO veikals(veikala_produkts, veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            # # VALUES(?,?,?,?,?,?)""", (row[3]+dateString, row[4], row[5], price, row[7], datetime.now()))

            return price
        
def cenas_pec_nosaukuma(nosaukums):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:
        cursor.execute(""" 
            SELECT *
            FROM produkts WHERE nosaukums = ?
            INNER JOIN (
                SELECT * FROM veikals
                GROUP BY produkta_modelis 
            ) veikals ON produkts.modelis = veikals.produkta_modelis ORDER BY veikala_produkts ASC """, (nosaukums,))

        rows = cursor.fetchall()

        for row in rows:

            url = row[7]
            veikals = row[4]
            price = helpers.get_price_methods_dynamic(veikals,url)

            # # cursor.execute("""
            # # INSERT INTO veikals(veikala_produkts, veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            # # VALUES(?,?,?,?,?,?)""", (row[3]+dateString, row[4], row[5], price, row[7], datetime.now()))

            return price

def cenu_iegusana_visi_produkti():

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
            ) veikals ON produkts.modelis = veikals.produkta_modelis ORDER BY nosaukums ASC """)

        rows = cursor.fetchall() # Iegūs visas rindas
        rindasMasivs = []

        for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

            # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
            # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
            
            date_checked = datetime.now()
            datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')

            veikals = row[4]
            url = row[7]
            produkta_modelis = row[5]
            produkta_nosaukums = row[2]
            produkta_tips = row[1]

            price = cenu_iegusana_tagad(veikals, url)
            rindasMasivs.append([produkta_nosaukums, veikals, price, url, datumsParveidots])
            
            cursor.execute("""
            INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES(?,?,?,?,?)""", (veikals, produkta_modelis, price, url, date_checked))

        return(rindasMasivs)
    
def cenas_pec_tipa(tips):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    rindasMasivs = []

    with connection:
        cursor.execute(""" 
            SELECT *
            FROM produkts
            INNER JOIN (
                SELECT * FROM veikals
                GROUP BY produkta_modelis 
            ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.tips = ? ORDER BY veikala_produkts ASC """, (tips,))

        rows = cursor.fetchall() 

        for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

            # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
            # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
            
            date_checked = datetime.now()
            datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')

            veikals = row[4]
            url = row[7]
            produkta_modelis = row[5]
            produkta_nosaukums = row[2]
            produkta_tips = row[1]

            price = cenu_iegusana_tagad(veikals, url)
            rindasMasivs.append([produkta_nosaukums, veikals, price, url, datumsParveidots])
            
            cursor.execute("""
            INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES(?,?,?,?,?)""", (veikals, produkta_modelis, price, url, date_checked))

        return(rindasMasivs)
    
def cenas_tikai_nosaukums(nosaukums):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:
        cursor.execute(""" 
            SELECT *
            FROM produkts
            INNER JOIN (
                SELECT * FROM veikals
                GROUP BY produkta_modelis 
            ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.nosaukums = ? ORDER BY veikala_produkts ASC """, (nosaukums,))

        rows = cursor.fetchall()
        rindasMasivs = []

        for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

            # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
            # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
            
            date_checked = datetime.now()
            datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')

            veikals = row[4]
            url = row[7]
            produkta_modelis = row[5]
            produkta_nosaukums = row[2]
            produkta_tips = row[1]

            price = cenu_iegusana_tagad(veikals, url)
            rindasMasivs.append([produkta_nosaukums, veikals, price, url, datumsParveidots])
            
            cursor.execute("""
            INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES(?,?,?,?,?)""", (veikals, produkta_modelis, price, url, date_checked))

        return(rindasMasivs)
    
def cenas_pec_nosaukuma_un_veikala(produkts, veikals):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:
        cursor.execute(""" 
            SELECT *
            FROM produkts
            INNER JOIN (
                SELECT * FROM veikals
                GROUP BY produkta_modelis 
            ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.nosaukums = ?  
                AND veikals.veikala_nosaukums = ? ORDER BY veikala_produkts ASC """, (produkts, veikals,))

        rows = cursor.fetchall()
        rindasMasivs = []

        for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

            # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
            # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
            
            date_checked = datetime.now()
            datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')

            veikals = row[4]
            url = row[7]
            produkta_modelis = row[5]
            produkta_nosaukums = row[2]
            produkta_tips = row[1]

            price = cenu_iegusana_tagad(veikals, url)
            rindasMasivs.append([produkta_nosaukums, veikals, price, url, datumsParveidots])
            
            cursor.execute("""
            INSERT INTO veikals(veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES(?,?,?,?,?)""", (veikals, produkta_modelis, price, url, date_checked))

        return(rindasMasivs)