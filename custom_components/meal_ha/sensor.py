from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities
):
    food_lib = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MealIngredientsSensor(food_lib)], True)

class MealIngredientsSensor(SensorEntity):
    _attr_name = "Meal Ingredients"
    _attr_icon = "mdi:food"

    def __init__(self, food_lib):
        self.food_lib = food_lib

    @property
    def native_value(self):
        foods = self.food_lib.list_foods()
        return len(foods)

    @property
    def extra_state_attributes(self):
        foods = self.food_lib.list_foods()
        return {
            "ingredients": {fid: name for fid, name in foods}
        }
