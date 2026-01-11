"""
Module pour la gestion de plusieurs listes de courses.
"""

class ShoppingLists:
    def __init__(self):
        self.lists = {}

    def create_list(self, name):
        if name not in self.lists:
            self.lists[name] = []

    def add_item(self, name, item):
        if name in self.lists:
            self.lists[name].append(item)

    def get_list(self, name):
        return self.lists.get(name, [])
