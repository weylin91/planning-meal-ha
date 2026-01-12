from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .db import init_db
from .food_library import FoodLibrary
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.components.http import StaticPathConfig

async def async_setup(hass: HomeAssistant, config: dict):
    # Panel embarqué Meal HA
    await hass.http.async_register_static_paths([
        StaticPathConfig("/meal_ha-panel", str(hass.config.path("custom_components/meal_ha/www")), False)
    ])
    hass.async_create_task(
        hass.helpers.frontend.async_register_built_in_panel(
            component_name="iframe",
            sidebar_title="Meal HA",
            sidebar_icon="mdi:food",
            frontend_url_path="meal_ha-panel",
            config={"url": "/meal_ha-panel/meal_ha_panel.html"},
            require_admin=False
        )
    )
    # Initialisation de la BDD et FoodLibrary
    init_db(hass)
    hass.data[DOMAIN] = FoodLibrary(hass)

    # Déclaration du sensor
    hass.async_create_task(async_load_platform(hass, SENSOR_DOMAIN, DOMAIN, {}, config))

    # Service pour ajouter un ingrédient
    async def handle_add_food(call):
        name = call.data.get("name")
        if name:
            hass.data[DOMAIN].add_food(name)

    # Service pour lister les ingrédients (logs)
    async def handle_list_foods(call):
        foods = hass.data[DOMAIN].list_foods()
        msg = (
            "Ingrédients : " + ", ".join(f"{fid}: {name}" for fid, name in foods)
            if foods
            else "Aucun ingrédient trouvé."
        )
        hass.components.logger.info(msg)

    hass.services.async_register(DOMAIN, "add_food", handle_add_food)
    hass.services.async_register(DOMAIN, "list_foods", handle_list_foods)

    return True
