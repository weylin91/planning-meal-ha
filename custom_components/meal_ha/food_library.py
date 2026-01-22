"""
Module pour la gestion de la bibliothèque d'aliments avec SQLite.
"""

from .db import get_db_path
import sqlite3

class FoodLibrary:
    def __init__(self, hass):
        self.hass = hass

    def add_food(self, name, category):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO foods (name, category) VALUES (?, ?)", (name, category))
            conn.commit()

    def update_food(self, food_id, new_name):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE foods SET name = ? WHERE id = ?", (new_name, food_id))
            conn.commit()

    def delete_food(self, food_id):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM foods WHERE id = ?", (food_id,))
            conn.commit()

    def list_foods(self):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM foods")
            return cursor.fetchall()
