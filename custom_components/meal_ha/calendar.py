"""
Module pour l'alimentation du calendrier avec les plats.
"""

class MealCalendar:
    def __init__(self):
        self.entries = []

    def add_entry(self, date, main_dish, side_dish):
        self.entries.append({
            "date": date,
            "main": main_dish,
            "side": side_dish
        })

    def get_entries(self):
        return self.entries
