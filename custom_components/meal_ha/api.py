from unicodedata import category
from homeassistant.helpers.http import HomeAssistantView
from .const import DOMAIN

class MealHAFoodsView(HomeAssistantView):
    url = "/api/meal_ha/foods"
    name = "api:meal_ha:foods"
    requires_auth = True

    async def get(self, request):
        hass = request.app["hass"]
        foods = hass.data[DOMAIN].list_foods()
        return self.json({"foods": foods})

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()
        name = data.get("name")
        category = data.get("category", "ingredient")

        if not name:
            return self.json({"error": "name is required"}, status_code=400)

        hass.data[DOMAIN].add_food(name, category)
        return self.json({"status": "ok", "name": name, "category": category})