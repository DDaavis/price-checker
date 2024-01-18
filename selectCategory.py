import os
import sqlite3

# Iegūs visas aktīvās kategorijas kas pieejamas DB, lai varētu tās parādīt vienā no optionMenu
def category_selection():

    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection: # beigās nebūs nepieciešams pievienot connection.commit() un connection.close()
        
        # Savāks katra produkta info, bet lai produkti neatkārtotos* (zemāk) - sagrupēju pēc produktaNosaukums + veikalaNosaukums
        # Datu atkārtošanās var notikt tikai tad, ja no konkrēta produkta ir iegūti dažādu datumu un laiku dati, tāpēc tie ir jāgrupē
        cursor.execute(""" 
        SELECT tips
        FROM produkts
        GROUP BY tips ORDER BY tips ASC""")
            
        rows = cursor.fetchall()
        arr = []
        for row in rows:
            arr.append(row[0])
        
        # arr.replace([',',''],["'",''],['(',''],[')',''])
            
        tupleToString=['Every Category']
        for each in arr:
            tupleToString.append(each)
        
        return tupleToString

# Atkarībā no izvēlētās kategorijas(tipa) izvēlēsies visus tās kategorijas produktus
def get_product_from_category(tips):
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection: # beigās nebūs nepieciešams pievienot connection.commit() un connection.close()
        
        # Savāks katra produkta info, bet lai produkti neatkārtotos* (zemāk) - sagrupēju pēc produktaNosaukums + veikalaNosaukums
        # Datu atkārtošanās var notikt tikai tad, ja no konkrēta produkta ir iegūti dažādu datumu un laiku dati, tāpēc tie ir jāgrupē
        cursor.execute(""" 
        SELECT tips, nosaukums
        FROM produkts
        WHERE tips = ?
        GROUP BY tips ORDER BY tips ASC""", (tips,))
        rows = cursor.fetchall()
        arr = []
        for row in rows:
            arr.append(row[1])
        
        # arr.replace([',',''],["'",''],['(',''],[')',''])
            
        tupleToString=['Every Product']

        for each in arr:
            tupleToString.append(each)
        return tupleToString
    
def get_all_products():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    database_file = os.path.join(script_dir, "database.db")
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with connection: # beigās nebūs nepieciešams pievienot connection.commit() un connection.close()
        
        # Savāks katra produkta info, bet lai produkti neatkārtotos* (zemāk) - sagrupēju pēc produktaNosaukums + veikalaNosaukums
        # Datu atkārtošanās var notikt tikai tad, ja no konkrēta produkta ir iegūti dažādu datumu un laiku dati, tāpēc tie ir jāgrupē
        cursor.execute(""" 
        SELECT tips, nosaukums
        FROM produkts
        GROUP BY tips ORDER BY tips ASC""")
        rows = cursor.fetchall()
        arr = []
        for row in rows:
            arr.append(row[1])
        
        # arr.replace([',',''],["'",''],['(',''],[')',''])
            
        tupleToString=['Every Product']
        
        for each in arr:
            tupleToString.append(each)
        return tupleToString