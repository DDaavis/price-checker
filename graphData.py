import sqlite3
import os

def get_data_for_graph(tips, produkts, veikals):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    
    # Ja tiek izvēlēts kāds konkrēts produkts, bet netiek izvēlēta kategorija un veikals, tad izpildīs šo 
    if produkts != 'Every Product' and veikals == 'Every Shop':
        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.nosaukums = ? 
                ORDER BY date_checked ASC """, (produkts,))

            rows = cursor.fetchall()
            rindasMasivs = []

            for row in rows:
                
                date_checked = row[8]
                # datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')
                veikals = row[4]
                produkta_nosaukums = row[2]
                price = row[6]
                rindasMasivs.append([price, date_checked, produkta_nosaukums, veikals])

            return(rindasMasivs)
        
    # ja ir izvēlēts tik sīki, ka izvēlas pat veikalu
    if produkts != 'Every Product' and veikals != 'Every Shop':
        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.nosaukums = ?
                    AND veikals.veikala_nosaukums = ?
                ORDER BY date_checked ASC """, (produkts, veikals,))

            rows = cursor.fetchall()
            rindasMasivs = []

            for row in rows:
                
                date_checked = row[8]
                # datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')
                veikals = row[4]
                produkta_nosaukums = row[2]
                price = row[6]
                rindasMasivs.append([price, date_checked, produkta_nosaukums, veikals])

            return(rindasMasivs)
        
    # Ja tiek izvēlēta konkrēta kategorija, bet netiek izvēlēts konkrēts produkts, tad izpildīs šo
    if produkts == 'Every Product' and tips != 'Every Category':
        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE produkts.tips = ?
                ORDER BY date_checked ASC """, (tips,))

            rows = cursor.fetchall()
            rindasMasivs = []

            for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

                # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
                # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
                
                date_checked = row[8]
                # datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')
                veikals = row[4]
                produkta_nosaukums = row[2]
                price = row[6]
                rindasMasivs.append([price, date_checked, produkta_nosaukums, veikals])

            return(rindasMasivs)
    
    # Ja netiek izvēlēta ne kategorija, ne produkts, tad atlasīs visas preces
    if produkts == 'Every Product' and tips == 'Every Category':
        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis
                ORDER BY date_checked ASC """)

            rows = cursor.fetchall()
            rindasMasivs = []

            for row in rows: # Šeit iterēs katru rindu un šeit jāievieto visa loģika, lai katrai rindai tiktu veikta apstrāde

                # row[x]: 0 - produktsPK, 1 - tips, 2 - nosaukums
                # 3 - veikalsPK, 4 - veikala nosaukums, 5 - produkta_modelis, 6 - cena, 7 - url, 8 - date_checked
                
                date_checked = row[8]
                # datumsParveidots = date_checked.strftime('%Y-%m-%d %H:%M:%S')
                veikals = row[4]
                produkta_nosaukums = row[2]
                price = row[6]
                rindasMasivs.append([price, date_checked, produkta_nosaukums, veikals])

            return(rindasMasivs)