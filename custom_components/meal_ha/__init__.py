"""
Initialisation du composant meal_ha pour Home Assistant.
"""

DOMAIN = "meal_ha"



from .db import init_db
from .food_library import FoodLibrary

async def async_setup(hass, config):
            # Déclare la plateforme sensor pour la liste des ingrédients
            hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)
        # Service pour lister les ingrédients
        async def handle_list_foods(call):
            food_lib = FoodLibrary(hass)
            foods = food_lib.list_foods()
            if foods:
                msg = "Ingrédients : " + ", ".join([f"{fid}: {name}" for fid, name in foods])
            else:
                msg = "Aucun ingrédient trouvé."
            hass.components.logger.info(msg)

        hass.services.async_register(DOMAIN, "list_foods", handle_list_foods, schema=None)
    """Initialisation du composant."""
    hass.data[DOMAIN] = {}
    # Création/initialisation de la base de données
    init_db(hass)

    # Service pour ajouter un ingrédient
    async def handle_add_food(call):
        name = call.data.get("name")
        if not name:
            return
        food_lib = FoodLibrary(hass)
        food_lib.add_food(name)

    hass.services.async_register(DOMAIN, "add_food", handle_add_food, schema=None)
    return True
