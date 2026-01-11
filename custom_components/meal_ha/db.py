"""
Gestion de la base de données SQLite pour meal_ha.
"""
import sqlite3
import os

DB_FILENAME = "meal_ha.sqlite3"

def get_db_path(hass):
    return os.path.join(hass.config.path("."), DB_FILENAME)

def init_db(hass):
    db_path = get_db_path(hass)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Création des tables si elles n'existent pas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    # Table de liaison entre plats et ingrédients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dish_ingredients (
        dish_id INTEGER NOT NULL,
        food_id INTEGER NOT NULL,
        PRIMARY KEY (dish_id, food_id),
        FOREIGN KEY(dish_id) REFERENCES dishes(id),
        FOREIGN KEY(food_id) REFERENCES foods(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        main_dish_id INTEGER,
        side_dish_id INTEGER,
        FOREIGN KEY(main_dish_id) REFERENCES dishes(id),
        FOREIGN KEY(side_dish_id) REFERENCES dishes(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shopping_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shopping_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER,
        item TEXT NOT NULL,
        FOREIGN KEY(list_id) REFERENCES shopping_lists(id)
    )
    """)
    
    conn.commit()
    conn.close()
