"""Input number platform for Chicken Farm integration."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.input_number import InputNumber
from homeassistant.config_entries import ConfigEntry

DOMAIN = "chicken"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up input_number entities for Chicken Farm."""
    input_numbers = [
        # Daily Egg Collection
        InputNumber(
            hass,
            "white_eggs_daily",
            "White Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "beige_eggs_daily",
            "Beige Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "mint_eggs_daily",
            "Mint Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "olive_eggs_daily",
            "Olive Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "brown_eggs_daily",
            "Brown Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "chocolate_eggs_daily",
            "Chocolate Eggs Daily",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "broken_eggs",
            "Broken Eggs",
            0,
            1000,
            1,
        ),

        # Eggs in Storage
        InputNumber(
            hass,
            "eggs_used",
            "Eggs Used",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "eggs_sold_amount",
            "Eggs Sold (Amount)",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "eggs_sold_value",
            "Eggs Sold (Value)",
            0,
            10000,
            0.01,
        ),
        InputNumber(
            hass,
            "eggs_to_hatchery",
            "Eggs to Hatchery",
            0,
            1000,
            1,
        ),

        # Purchases
        InputNumber(
            hass,
            "purchase_weight",
            "Purchase Weight (kg)",
            0,
            1000,
            0.1,
        ),
        InputNumber(
            hass,
            "purchase_cost",
            "Purchase Cost (€)",
            0,
            10000,
            0.01,
        ),
        InputNumber(
            hass,
            "pellets_kg",
            "Pellets (kg)",
            0,
            1000,
            0.1,
        ),
        InputNumber(
            hass,
            "pellets_cost",
            "Pellets Cost (€)",
            0,
            10000,
            0.01,
        ),
        InputNumber(
            hass,
            "scratch_grains_kg",
            "Scratch Grains (kg)",
            0,
            1000,
            0.1,
        ),
        InputNumber(
            hass,
            "scratch_grains_cost",
            "Scratch Grains Cost (€)",
            0,
            10000,
            0.01,
        ),
        InputNumber(
            hass,
            "bedding_cost",
            "Bedding Cost (€)",
            0,
            10000,
            0.01,
        ),
        InputNumber(
            hass,
            "misc_cost",
            "Miscellaneous Cost (€)",
            0,
            10000,
            0.01,
        ),

        # Chicken Counter
        InputNumber(
            hass,
            "number_of_hens",
            "Number of Hens",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "number_of_roosters",
            "Number of Roosters",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "chicken_died",
            "Chickens Died",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "chicken_butchered",
            "Chickens Butchered",
            0,
            1000,
            1,
        ),

        # Hatchery
        InputNumber(
            hass,
            "eggs_in_hatchery",
            "Eggs in Hatchery",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "hatched_eggs",
            "Hatched Eggs",
            0,
            1000,
            1,
        ),
        InputNumber(
            hass,
            "died_eggs",
            "Died Eggs",
            0,
            1000,
            1,
        ),
    ]

    # Add all input_number entities
    async_add_entities(input_numbers)