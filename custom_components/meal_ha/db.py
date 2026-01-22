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
        name TEXT NOT NULL UNIQUE, 
        category TEXT DEFAULT 'ingredient'
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        nb_meal INTEGER DEFAULT 1,
        type TEXT DEFAULT 'dish'
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
    
    conn.commit()
    conn.close()
