"""
Initialisation du composant meal_ha pour Home Assistant.
"""

DOMAIN = "meal_ha"


from .db import init_db

async def async_setup(hass, config):
    """Initialisation du composant."""
    hass.data[DOMAIN] = {}
    # Création/initialisation de la base de données
    init_db(hass)
    return True
