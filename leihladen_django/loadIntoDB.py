import json
import sqlite3
from datetime import date

#JSON-File öffnen und als dictionary laden
with open('json_daten_formatiert.json',  encoding='utf-8') as f:
    data = json.load(f)

try:
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    print("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

    # Tabelle leeren
    cursor.execute("DELETE FROM product_product")
    print("Table product_product emptied")
    cursor.execute("DELETE FROM product_category")
    print("Table product_category emptied")

    for category in set(category for product in data['data'] for category in product['kategorien']):
        try:
            if isinstance(category, str):
                slug = category.lower().replace(" ", "-")
            else:
                slug = str(category)
            conn.execute("INSERT INTO product_category (name, slug) VALUES (?,?)", (category, slug))
            
        except sqlite3.IntegrityError as e:
            print(str(e))

    print("product_category filled")

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
        date_added = date.today()

        try:
            conn.execute("INSERT INTO product_product (id, slug, name, description, dimension, weight, smallPieces, deposit, fee, images, date_added, quantity, available) VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?)", (id, slug, name, description, dimension, weight, smallPieces, deposit, fee, images, date_added, quantity, available))
        except sqlite3.IntegrityError as e:
            print(str(e))

        for category in product['kategorien']:
            try:
                # Find category ID by name
                cursor.execute("SELECT id FROM product_category WHERE name=?", (category,))
                category_id = cursor.fetchone()[0]
                conn.execute("INSERT INTO product_product_categories (product_id, category_id) VALUES (?, ?)", (id, category_id))
                
            except sqlite3.IntegrityError as e:
                print(str(e))

    conn.commit()
    print("product_product filled")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")