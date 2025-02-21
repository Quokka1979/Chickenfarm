from homeassistant.core import ServiceCall
from homeassistant.helpers.service import async_register_admin_service
import voluptuous as vol
from .const import DOMAIN, PURCHASE_TYPES, EGG_TYPES

# Schema for save_purchase service
SAVE_PURCHASE_SCHEMA = vol.Schema(
    {
        vol.Required("purchase_type"): vol.In(PURCHASE_TYPES),
        vol.Required("purchase_weight"): vol.Coerce(float),
        vol.Required("purchase_cost"): vol.Coerce(float),
    }
)

# Schema for save_egg_collection service
SAVE_EGG_COLLECTION_SCHEMA = vol.Schema(
    {
        vol.Required("white_eggs"): vol.Coerce(float),
        vol.Required("beige_eggs"): vol.Coerce(float),
        vol.Required("mint_eggs"): vol.Coerce(float),
        vol.Required("olive_eggs"): vol.Coerce(float),
        vol.Required("brown_eggs"): vol.Coerce(float),
        vol.Required("chocolate_eggs"): vol.Coerce(float),
    }
)

async def async_setup_scripts(hass):
    """Set up Chicken Farm scripts."""

    async def save_purchase(call: ServiceCall):
        """Save purchase data."""
        purchase_type = call.data.get("purchase_type")
        purchase_weight = call.data.get("purchase_weight")
        purchase_cost = call.data.get("purchase_cost")

        # Map purchase types to their corresponding entities
        purchase_entities = {
            "Pellets": ("input_number.pellets_kg", "input_number.pellets_cost"),
            "Scratch Grains": ("input_number.scratch_grains_kg", "input_number.scratch_grains_cost"),
            "Bedding": (None, "input_number.bedding_cost"),
            "Misc": (None, "input_number.misc_cost"),
        }

        weight_entity, cost_entity = purchase_entities.get(purchase_type, (None, None))

        if weight_entity:
            await hass.services.async_call(
                "input_number",
                "set_value",
                {"entity_id": weight_entity, "value": purchase_weight},
            )

        if cost_entity:
            await hass.services.async_call(
                "input_number",
                "set_value",
                {"entity_id": cost_entity, "value": purchase_cost},
            )

        # Reset input fields
        await reset_purchase_inputs(hass)

    async def save_egg_collection(call: ServiceCall):
        """Save daily egg collection data."""
        egg_data = {
            "white_eggs": call.data.get("white_eggs"),
            "beige_eggs": call.data.get("beige_eggs"),
            "mint_eggs": call.data.get("mint_eggs"),
            "olive_eggs": call.data.get("olive_eggs"),
            "brown_eggs": call.data.get("brown_eggs"),
            "chocolate_eggs": call.data.get("chocolate_eggs"),
        }

        for egg_type, value in egg_data.items():
            await hass.services.async_call(
                "input_number",
                "set_value",
                {"entity_id": f"input_number.{egg_type}_daily", "value": value},
            )

        # Reset input fields
        await reset_egg_collection_inputs(hass)

    async def reset_purchase_inputs(hass):
        """Reset purchase input fields."""
        await hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": "input_number.purchase_weight", "value": 0},
        )
        await hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": "input_number.purchase_cost", "value": 0},
        )

    async def reset_egg_collection_inputs(hass):
        """Reset egg collection input fields."""
        for egg_type in EGG_TYPES:
            await hass.services.async_call(
                "input_number",
                "set_value",
                {"entity_id": f"input_number.{egg_type}_eggs_daily", "value": 0},
            )

    # Register services
    async_register_admin_service(
        hass,
        DOMAIN,
        "save_purchase",
        save_purchase,
        schema=SAVE_PURCHASE_SCHEMA,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        "save_egg_collection",
        save_egg_collection,
        schema=SAVE_EGG_COLLECTION_SCHEMA,
    )