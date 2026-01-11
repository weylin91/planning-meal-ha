"""
Sensor personnalisé pour afficher la liste des ingrédients dans Home Assistant.
"""
from homeassistant.helpers.entity import Entity
from .food_library import FoodLibrary
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([FoodListSensor(hass)], True)

class FoodListSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._state = None
        self._attributes = {}
        self._name = "Liste des ingrédients"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        food_lib = FoodLibrary(self._hass)
        foods = food_lib.list_foods()
        self._state = len(foods)
        self._attributes = {str(fid): name for fid, name in foods}
