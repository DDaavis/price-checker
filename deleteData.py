import sqlite3
import os

# Varianti kādos var dzēst produktus:
# 1. - Cilvēks izvēlas tikai kategoriju:
#           Jādzēš ārā visi kategorijas produkti
# 2. - Cilvēks izvēlas kategoriju un produkta nosaukumu:
#           Jādzēš ārā visi produkti ar to nosaukumu no visiem veikaliem
# 3. - Cilvēks izvēlas visu
#           Jādzēš ārā konkrētais produkts tikai no konkrētā veikala

# Paredzēts, lai delete ekrānā iegūtu visas kategorijas
def get_all_categories():

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:

        cursor.execute(""" 
            SELECT *
            FROM produkts
            GROUP BY tips
            ORDER BY tips ASC """)

        rows = cursor.fetchall()
        rindasMasivs = []

        for row in rows:
            tips = '' + row[1]
            rindasMasivs.append(tips)

        return(rindasMasivs)   

# Kad delete ekrānā uzspiedīs pogu Delete, šī funkcija no datubāzes izdzēsīs visus datus par izvēlētajiem atribūtiem
def delete_selected_products(tips, nosaukums, veikals):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection:
        # Ja ir izvēlēts tips, nosaukums, veikals:
        if veikals != 'Every Shop':
            cursor.execute("""
                SELECT *
                FROM produkts
                INNER JOIN veikals ON produkts.modelis = veikals.produkta_modelis
                WHERE nosaukums = ? AND veikala_nosaukums = ?
                ORDER BY veikala_produkts ASC
            """, (nosaukums, veikals,))

            rows = cursor.fetchall()
            
            for row in rows:

                cursor.execute("""
                    DELETE FROM produkts
                    WHERE modelis = ?
                """, (row[5],))

                cursor.execute("""
                    DELETE FROM veikals
                    WHERE produkta_modelis = ?
                """, (row[5],))

                
        # Ja nekas nav izvēlēts
        if veikals == 'Every Shop' and tips == 'Every Category' and nosaukums == 'Every Product':
                cursor.execute(""" DELETE FROM produkts """)
                cursor.execute(""" DELETE FROM veikals """)
        
        # Ja nav izvēlēts veikals, bet ir izvēlēts konkrēts produkts - jādzēš ārā visi ieraksti ar šo produktu:
        if veikals == 'Every Shop'  and nosaukums != 'Every Product':

            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE nosaukums = ? ORDER BY veikala_produkts ASC """, (nosaukums,))
            
            rows = cursor.fetchall()

            for row in rows:

                cursor.execute("""
                    DELETE FROM produkts
                    WHERE modelis = ?
                """, (row[5],))

                cursor.execute("""
                    DELETE FROM veikals
                    WHERE produkta_modelis = ?
                """, (row[5],))
                
        # Ja ir izvēlēta tikai kategorija
        if tips != 'Every Category' and nosaukums == 'Every Product':

            cursor.execute(""" 
                SELECT *
                FROM produkts
                INNER JOIN (
                    SELECT * FROM veikals
                ) veikals ON produkts.modelis = veikals.produkta_modelis WHERE tips = ? ORDER BY veikala_produkts ASC """, (tips,))
            
            rows = cursor.fetchall()
            for row in rows:
                cursor.execute("""
                    DELETE FROM produkts
                    WHERE modelis = ?
                """, (row[5],))

                cursor.execute("""
                    DELETE FROM veikals
                    WHERE produkta_modelis = ?
                """, (row[5],))
                

# Paredzēts, lai iegūtu produkta tipu atkarībā no produkta nosaukums
def get_product_from_type(tips):

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    if tips == 'Every Category':

        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts
                GROUP BY nosaukums
                """,)

            rows = cursor.fetchall()
            produktuMasivs = ['Every Product']

            for row in rows:

                produkts = '' + row[2]
                produktuMasivs.append(produkts)
                produkts = ''

            return produktuMasivs

    else:
        with connection:
            cursor.execute(""" 
                SELECT *
                FROM produkts WHERE tips = ?
                GROUP BY nosaukums
                """, (tips,))

            rows = cursor.fetchall()
            produktuMasivs = ['Every Product']

            for row in rows:

                produkts = '' + row[2]
                produktuMasivs.append(produkts)
                produkts = ''

            return produktuMasivs
        
# Paredzēts, lai iegūtu visus veikalus, kuros atrodas konkrētais produkts
def get_product_shop(nosaukums):

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
            ) veikals ON produkts.modelis = veikals.produkta_modelis  WHERE nosaukums = ? ORDER BY veikala_produkts ASC """, (nosaukums,))

        rows = cursor.fetchall()
        veikaluMasivs = ['Every Shop']

        for row in rows:

            veikals = '' + row[4]
            veikaluMasivs.append(veikals)
            veikals = ''

        return veikaluMasivs
        
def delete_everything():

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    cursor.execute(""" DELETE FROM veikals""")
    cursor.execute(""" DELETE FROM produkts""")

# delete_everything() # !!! UNCOMMENT ONLY IF YOU NEED TO DELETE EVERYTHING !!! 