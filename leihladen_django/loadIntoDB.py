import json
import sqlite3
from datetime import datetime

#JSON-File öffnen und als dictionary laden
with open('json_daten_formatiert.json',  encoding='utf-8') as f:
    data = json.load(f)

try:
    #Mit SQLite db (file) verbinden
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor() # Erzeugt cursor für SQL-Abfragen
    print("Datenbank erstellt und erfolgreich mit SQLite verbunden")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Datenbank Version ist: ", record)

    # Tabellen Product und Hilfstabelle Product_Category leeren
    cursor.execute("DELETE FROM product_product")
    print("Tabelle product_product geleert")
    cursor.execute("DELETE FROM product_category")
    print("Tabelle product_category geleert")

    #Jeden Eintrag im File durchlaufen und variable zuordnen
    for product in data['data']:
        id = product['inventarnummer']
        name = product['bezeichnung']
        slug = name.lower().replace(" ", "-")
        description = product['beschreibung']
        dimension = product['dimension']
        weight = product['gewicht']
        smallPieces = product['kleinteil']
        deposit = product['kaution']
        fee = product['kosten']
        images = json.dumps(product['bilder']) 
        quantity = 1
        available = 1
        now = datetime.now() #Datetime objekt erzeugen
        date_added = now.strftime("%Y-%m-%d %H:%M:%S") #Datum + Uhrzeit zum Ausführzeitpunkt holen

        #Da product['kleinteil'] ein String ist, aber die Datenbank ein bool erwartet -> True und False setzen
        if smallPieces == 'ja':
            smallPieces = True
        else:
            smallPieces = False

        #Versuchen den Eintrag in die Datenbank zu schreiben
        try:
            conn.execute("INSERT INTO product_product (id, slug, name, description, dimension, weight, smallPieces, deposit, fee, images, date_added, quantity, available) VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?)", (id, slug, name, description, dimension, weight, smallPieces, deposit, fee, images, date_added, quantity, available))
        except sqlite3.IntegrityError as e:
            print(str(e))

        #Kategorie 0,1,2,3,4,5,6,7,8,9,10 soweit erkennbar
        categories = ['Alle', 'Haushalt', 'Sonstiges', 'Kinder', 'Spiele', 'Büro', 'Garten', 'Werkzeug', '8', 'Instrumente', 'Diverses']
        
        #Kategorie Nummer aus der File zu einer Kategorie zuordnen und in DB speichern
        for category_num in product['kategorien']:
            category_num = int(category_num)

            category = categories[category_num]
            slug = category.lower().replace(" ", "-") #Kategorie slug erzeugen
            cursor.execute("SELECT id FROM product_category WHERE name=?", (category,))
            result = cursor.fetchone()

            if result:
                category_id = result[0]
            else:
                cursor.execute("INSERT INTO product_category (name, slug) VALUES (?, ?)", (category,slug))
                category_id = cursor.lastrowid

            #Hilfstabelle Product_Categories füllen
            try:
                conn.execute("INSERT INTO product_product_categories (product_id, category_id) VALUES (?, ?)", (id, category_id))
            except sqlite3.IntegrityError as e:
                print(str(e))

    print("Tabelle product_category filled")

    conn.commit()
    print("Tabelle product_product filled")

except sqlite3.Error as error:
    print("Fehler beim Verbinden mit SQLite", error)

finally:
    if conn:
        conn.close()
        print("Die SQLite Verbindung wurde getrennt")