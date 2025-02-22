"""Number platform for Chicken Farm."""

from __future__ import annotations
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up number platform."""
    numbers = [
        # Egg count inputs
        ChickenNumber(
            "white_eggs_daily",
            "White Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "beige_eggs_daily",
            "Beige Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "mint_eggs_daily",
            "Mint Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "olive_eggs_daily",
            "Olive Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "brown_eggs_daily",
            "Brown Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "chocolate_eggs_daily",
            "Chocolate Eggs Today",
            "mdi:egg",
            0,
            100,
            1
        ),
        ChickenNumber(
            "broken_eggs",
            "Broken Eggs",
            "mdi:egg-off",
            0,
            100,
            1
        ),
        # Usage tracking
        ChickenNumber(
            "eggs_used",
            "Eggs Used",
            "mdi:egg-off",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "eggs_to_hatchery",
            "Eggs to Hatchery",
            "mdi:egg-easter",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "eggs_sold_amount",
            "Eggs Sold (Amount)",
            "mdi:egg",
            0,
            10000,
            1
        ),
        ChickenNumber(
            "eggs_sold_value",
            "Eggs Sold (Value)",
            "mdi:cash",
            0,
            10000,
            0.01,
            CURRENCY_EURO
        ),
        # Cost inputs
        ChickenNumber(
            "pellets_kg",
            "Pellets Weight (KG)",
            "mdi:weight-kilogram",
            0,
            1000,
            0.1
        ),
        ChickenNumber(
            "pellets_cost",
            "Pellets Cost",
            "mdi:cash",
            0,
            1000,
            0.01,
            CURRENCY_EURO
        ),
        ChickenNumber(
            "scratch_grains_kg",
            "Scratch Grains Weight (KG)",
            "mdi:weight-kilogram",
            0,
            1000,
            0.1
        ),
        ChickenNumber(
            "scratch_grains_cost",
            "Scratch Grains Cost",
            "mdi:cash",
            0,
            1000,
            0.01,
            CURRENCY_EURO
        ),
        ChickenNumber(
            "bedding_cost",
            "Bedding Cost",
            "mdi:cash",
            0,
            1000,
            0.01,
            CURRENCY_EURO
        ),
        ChickenNumber(
            "misc_cost",
            "Miscellaneous Cost",
            "mdi:cash",
            0,
            1000,
            0.01,
            CURRENCY_EURO
        ),
        ChickenNumber(
            "number_of_hens",
            "Number of Hens",
            "mdi:gender-female",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "number_of_roosters",
            "Number of Roosters",
            "mdi:gender-male",
            0,
            100,
            1
        ),
        ChickenNumber(
            "chicken_died",
            "Chickens Died",
            "mdi:cross",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "chicken_butchered",
            "Chickens Butchered",
            "mdi:knife",
            0,
            1000,
            1
        ),
        # Hatchery tracking
        ChickenNumber(
            "eggs_in_hatchery",
            "Eggs in Hatchery",
            "mdi:egg-easter",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "hatched_eggs",
            "Hatched Eggs",
            "mdi:egg-easter",
            0,
            1000,
            1
        ),
        ChickenNumber(
            "died_eggs",
            "Died Eggs",
            "mdi:egg-off",
            0,
            1000,
            1
        ),
        # Purchase tracking
        ChickenNumber(
            "purchase_weight",
            "Purchase Weight",
            "mdi:weight-kilogram",
            0,
            1000,
            0.1
        ),
        ChickenNumber(
            "purchase_cost",
            "Purchase Cost",
            "mdi:cash",
            0,
            1000,
            0.01,
            CURRENCY_EURO
        )        
    ]
    async_add_entities(numbers, True)

class ChickenNumber(NumberEntity):
    """Representation of a Chicken Farm Number Input."""

    def __init__(
        self,
        unique_id: str,
        name: str,
        icon: str,
        min_value: float,
        max_value: float,
        step: float,
        unit: str | None = None,
    ) -> None:
        """Initialize the number input."""
        self._unique_id = unique_id
        self._name = name
        self._icon = icon
        self._min = min_value
        self._max = max_value
        self._step = step
        self._unit = unit
        self._value = min_value  # Initialize with the minimum value
        self._attr_native_unit_of_measurement = unit # Set unit of measurement

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"chicken_{self._unique_id}"

    @property
    def name(self) -> str:
        """Return the name of the number input."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon of the number input."""
        return self._icon

    @property
    def native_min_value(self) -> float:
        """Return the minimum value."""
        return self._min

    @property
    def native_max_value(self) -> float:
        """Return the maximum value."""
        return self._max

    @property
    def native_step(self) -> float:
        """Return the increment/decrement step."""
        return self._step

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self._value

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        return self._attr_native_unit_of_measurement

    async def async_set_value(self, value: float) -> None:
        """Set a new value."""
        self._value = value
        self.async_write_ha_state()

