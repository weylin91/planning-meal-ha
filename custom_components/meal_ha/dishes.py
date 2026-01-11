"""
Module pour la gestion des plats avec gestion des ingrédients via SQLite.
"""

from .db import get_db_path
import sqlite3

class DishManager:
    def __init__(self, hass):
        self.hass = hass

    def add_dish(self, name, ingredients=None):
        """Crée un plat et associe des ingrédients (liste d'id d'aliments)."""
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dishes (name) VALUES (?)", (name,))
            dish_id = cursor.lastrowid
            if ingredients:
                for food_id, quantity in ingredients:
                    cursor.execute("INSERT INTO dish_ingredients (dish_id, food_id, quantity) VALUES (?, ?, ?)", (dish_id, food_id, quantity))
            conn.commit()
        return dish_id

    def update_dish(self, dish_id, new_name=None, new_ingredients=None):
        """Modifie le nom et/ou la liste des ingrédients d'un plat."""
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            if new_name:
                cursor.execute("UPDATE dishes SET name = ? WHERE id = ?", (new_name, dish_id))
            if new_ingredients is not None:
                cursor.execute("DELETE FROM dish_ingredients WHERE dish_id = ?", (dish_id,))
                for food_id, quantity in new_ingredients:
                    cursor.execute("INSERT INTO dish_ingredients (dish_id, food_id, quantity) VALUES (?, ?, ?)", (dish_id, food_id, quantity))
            conn.commit()

    def list_dishes(self):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM dishes")
            return cursor.fetchall()

    def get_ingredients(self, dish_id):
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT foods.id, foods.name, dish_ingredients.quantity
                FROM dish_ingredients
                JOIN foods ON dish_ingredients.food_id = foods.id
                WHERE dish_ingredients.dish_id = ?
            """, (dish_id,))
            return cursor.fetchall()
        
    def delete_dish(self, dish_id):
        """Supprime un plat et ses liaisons avec les ingrédients."""
        db_path = get_db_path(self.hass)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dish_ingredients WHERE dish_id = ?", (dish_id,))
            cursor.execute("DELETE FROM dishes WHERE id = ?", (dish_id,))
            conn.commit()