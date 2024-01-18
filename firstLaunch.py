from datetime import datetime
import getprice
import os
import sqlite3

# Šis kods piepildīs datubāzes tabulas ar datiem, kas palīdzēs programmas prezentēšanai.

# šis vajadzīgs, lai datubāze veidotos tajā directory kā pats python fails
script_dir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(script_dir, "database.db")
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

with connection:

    # Datubāzes izveide, ja tā jau neeksistē
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produkts(
                modelis TEXT PRIMARY KEY,
                tips TEXT,
                nosaukums TEXT )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veikals(
                veikala_produkts INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                veikala_nosaukums TEXT,
                produkta_modelis TEXT,
                cena DECIMAL,
                url TEXT,
                date_checked DATETIME,
                FOREIGN KEY (produkta_modelis) REFERENCES produkts(modelis) )""")

    # Data has to be hard coded
    dateNow = datetime.now()
    product = 'R9 5900X'
    productType = 'CPU'
    productNoSpaces = product.replace(' ', '')
    # shop, url
    dataArray = [['dateks', 'https://www.dateks.lv/cenas/procesori-amd/622422-amd-ryzen-9-5900x-12c-24t-3-70-ghz-64mb-cache-105w-'], 
                ['1a', 'https://www.1a.lv/p/procesors-amd-amd-ryzen-9-5900x-3-7ghz-64mb-100-100000061wof-3-7ghz-am4-64mb/a6gn?mtd=search&pos=regular&src=searchnode'], 
                ['rdveikals', 'https://www.rdveikals.lv/products/lv/428/330674/sort/5/filter/0_0_0_0/Ryzen-9-5900X-100-100000061WOF-procesors.html'], 
                ['m79', 'https://m79.lv/datorukomponentes/procesori/amd-ryzen-9-5900x-box-am4-12c24t-105w'], 
                ['tet', 'https://www.tet.lv/veikals/procesori/amd-ryzen-9-5900x-3-7ghz-64mb-100-100000061wof.html'], 
                ['balticdata', 'https://www.balticdata.lv/lv/datortehnika/datoru-komponentes/procesori/amd-ryzen-9-5900x'], 
                ['elkor', 'https://www.elkor.lv/amd-100-100000061wof-100-100000061wof-ac336179.html']]

    for row in dataArray:
        shop = '' + row[0]
        url = '' + row[1]

        price = getprice.cenu_iegusana_tagad(shop, url) # getting the price can take a few seconds, if you want this to run faster, hard code the price instead
        productName = productNoSpaces + shop
        
        cursor.execute("""
            INSERT OR REPLACE INTO produkts(modelis, tips, nosaukums)
            VALUES (?, ?, ?) """, (productName, productType, product,))

        cursor.execute("""
            INSERT INTO veikals (veikala_nosaukums, produkta_modelis, cena, url, date_checked)
            VALUES (?, ?, ?, ?, ?) """, (shop, productName, price, url, dateNow,))
        
        print('Data from', shop, 'inserted!')

print("Dati ievietoti!") # Tīri tā, lai pārliecinātos, ka dati tika ievietoti