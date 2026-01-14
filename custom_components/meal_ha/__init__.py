from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.frontend import async_register_built_in_panel

from .const import DOMAIN
from .db import init_db
from .food_library import FoodLibrary
from .api import MealHAFoodsView


async def async_setup(hass: HomeAssistant, config: dict):
    # Fichiers statiques
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            "/local/meal_ha",
            str(hass.config.path("custom_components/meal_ha/www")),
            False,
        )
    ])

    # Panel iframe
    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Meal HA",
        sidebar_icon="mdi:food",
        frontend_url_path="meal_ha",
        config={"url": "/local/meal_ha/index.html"},
        require_admin=False,
    )

    # Init BDD + lib
    init_db(hass)
    hass.data[DOMAIN] = FoodLibrary(hass)

    # Sensor
    hass.async_create_task(
        async_load_platform(hass, SENSOR_DOMAIN, DOMAIN, {}, config)
    )

    # Routes API
    hass.http.register_view(MealHAFoodsView)

    return True
