from homeassistant.components.sensor import SensorEntity
from .food_library import FoodLibrary
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([FoodListSensor(hass)], True)

class FoodListSensor(SensorEntity):
    _attr_name = "Liste des ingrédients"
    _attr_icon = "mdi:food"

    def __init__(self, hass):
        self.hass = hass

    @property
    def native_value(self):
        food_lib = FoodLibrary(self.hass)
        foods = food_lib.list_foods()
        return len(foods)

    @property
    def extra_state_attributes(self):
        food_lib = FoodLibrary(self.hass)
        foods = food_lib.list_foods()
        return {"ingredients": {fid: name for fid, name in foods}}
