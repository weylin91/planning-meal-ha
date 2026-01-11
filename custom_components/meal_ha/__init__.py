from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .db import init_db
from .food_library import FoodLibrary

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    init_db(hass)

    hass.data[DOMAIN][entry.entry_id] = FoodLibrary(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def handle_add_food(call):
        name = call.data.get("name")
        if name:
            hass.data[DOMAIN][entry.entry_id].add_food(name)

    async def handle_list_foods(call):
        foods = hass.data[DOMAIN][entry.entry_id].list_foods()
        msg = (
            "Ingrédients : " + ", ".join(f"{fid}: {name}" for fid, name in foods)
            if foods
            else "Aucun ingrédient trouvé."
        )
        hass.components.logger.info(msg)

    hass.services.async_register(DOMAIN, "add_food", handle_add_food)
    hass.services.async_register(DOMAIN, "list_foods", handle_list_foods)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
