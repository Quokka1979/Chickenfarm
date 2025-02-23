"""Platform for Chicken Farm."""

from __future__ import annotations

import random
import time

import voluptuous as vol

from homeassistant.components.number import NumberEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.service import async_register_admin_service

from .const import DOMAIN, EGG_TYPES, PURCHASE_TYPES


# Schemas for services
SAVE_PURCHASE_SCHEMA = vol.Schema(
    {
        vol.Required("purchase_type"): vol.In(PURCHASE_TYPES),
        vol.Required("purchase_weight", default=0): vol.Coerce(float),
        vol.Required("purchase_cost"): vol.Coerce(float),
        vol.Required("purchase_date"): str,
    }
)

SAVE_EGG_COLLECTION_SCHEMA = vol.Schema(
    {
        vol.Required("white_eggs", default=0): vol.Coerce(float),
        vol.Required("beige_eggs", default=0): vol.Coerce(float),
        vol.Required("mint_eggs", default=0): vol.Coerce(float),
        vol.Required("olive_eggs", default=0): vol.Coerce(float),
        vol.Required("brown_eggs", default=0): vol.Coerce(float),
        vol.Required("chocolate_eggs", default=0): vol.Coerce(float),
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Chicken Farm platform."""

    # Set up entities
    numbers = [
        ChickenNumber("white_eggs_daily", "White Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("beige_eggs_daily", "Beige Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("mint_eggs_daily", "Mint Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("olive_eggs_daily", "Olive Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("brown_eggs_daily", "Brown Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("chocolate_eggs_daily", "Chocolate Eggs Today", "mdi:egg", 0, 100, 1),
        ChickenNumber("broken_eggs", "Broken Eggs", "mdi:egg-off", 0, 100, 1),
        ChickenNumber("eggs_used", "Eggs Used", "mdi:egg-off", 0, 1000, 1),
        ChickenNumber("eggs_to_hatchery", "Eggs to Hatchery", "mdi:egg-easter", 0, 1000, 1),
        ChickenNumber("eggs_sold_amount", "Eggs Sold (Amount)", "mdi:egg", 0, 10000, 1),
        ChickenNumber("eggs_sold_value", "Eggs Sold (Value)", "mdi:cash", 0, 10000, 0.01, CURRENCY_EURO),
        ChickenNumber("pellets_kg", "Pellets Weight (KG)", "mdi:weight-kilogram", 0, 1000, 0.1),
        ChickenNumber("pellets_cost", "Pellets Cost", "mdi:cash", 0, 1000, 0.01, CURRENCY_EURO),
        ChickenNumber("scratch_grains_kg", "Scratch Grains Weight (KG)", "mdi:weight-kilogram", 0, 1000, 0.1),
        ChickenNumber("scratch_grains_cost", "Scratch Grains Cost", "mdi:cash", 0, 1000, 0.01, CURRENCY_EURO),
        ChickenNumber("bedding_cost", "Bedding Cost", "mdi:cash", 0, 1000, 0.01, CURRENCY_EURO),
        ChickenNumber("misc_cost", "Miscellaneous Cost", "mdi:cash", 0, 1000, 0.01, CURRENCY_EURO),
        ChickenNumber("number_of_hens", "Number of Hens", "mdi:gender-female", 0, 1000, 1),
        ChickenNumber("number_of_roosters", "Number of Roosters", "mdi:gender-male", 0, 100, 1),
        ChickenNumber("chicken_died", "Chickens Died", "mdi:cross", 0, 1000, 1),
        ChickenNumber("chicken_butchered", "Chickens Butchered", "mdi:knife", 0, 1000, 1),
        ChickenNumber("eggs_in_hatchery", "Eggs in Hatchery", "mdi:egg-easter", 0, 1000, 1),
        ChickenNumber("hatched_eggs", "Hatched Eggs", "mdi:egg-easter", 0, 1000, 1),
        ChickenNumber("died_eggs", "Died Eggs", "mdi:egg-off", 0, 1000, 1),
        ChickenNumber("purchase_weight", "Purchase Weight", "mdi:weight-kilogram", 0, 1000, 0.1),
        ChickenNumber("purchase_cost", "Purchase Cost", "mdi:cash", 0, 1000, 0.01, CURRENCY_EURO),
    ]
    async_add_entities(numbers)

    # Set up the Eggs in Storage sensor
    async_add_entities([EggsInStorageSensor(hass)], True)

async def async_setup_services(hass: HomeAssistant):
    """Set up Chicken Farm services."""

    async def save_purchase(call: ServiceCall):
        """Save purchase data."""
        purchase_type = call.data.get("purchase_type")
        purchase_weight = call.data.get("purchase_weight", 0)
        purchase_cost = call.data.get("purchase_cost")
        purchase_date = call.data.get("purchase_date")

        # Map purchase types to their corresponding entities
        purchase_entities = {
            "Pellets": (
                "number.pellets_kg",
                "number.pellets_cost",
                "input_datetime.pellets_purchase_date",
            ),
            "Scratch Grains": (
                "number.scratch_grains_kg",
                "number.scratch_grains_cost",
                "input_datetime.scratch_grain_purchase_date",
            ),
            "Bedding": (None, "number.bedding_cost", "input_datetime.bedding_purchase_date"),
            "Misc": (None, "number.misc_cost", None),
        }

        weight_entity, cost_entity, date_entity = purchase_entities.get(
            purchase_type, (None, None, None)
        )

        if weight_entity:
            await hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": weight_entity, "value": purchase_weight},
            )

        if cost_entity:
            await hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": cost_entity, "value": purchase_cost},
            )

        if date_entity:
            await hass.services.async_call(
                "input_datetime",
                "set_datetime",
                {"entity_id": date_entity, "datetime": purchase_date},
            )

    async def save_daily_eggs(call: ServiceCall):
        """Save daily egg collection data and reset counts."""
        egg_data = {
            "white_eggs": call.data.get("white_eggs", 0),
            "beige_eggs": call.data.get("beige_eggs", 0),
            "mint_eggs": call.data.get("mint_eggs", 0),
            "olive_eggs": call.data.get("olive_eggs", 0),
            "brown_eggs": call.data.get("brown_eggs", 0),
            "chocolate_eggs": call.data.get("chocolate_eggs", 0),
        }

        # Update storage
        for egg_type, value in egg_data.items():
            await hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": f"number.{egg_type}_daily", "value": value},
            )

        # Reset daily egg counts
        for egg_type in EGG_TYPES:
            await hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": f"number.{egg_type}_eggs_daily", "value": 0},
            )

    async def reset_daily_eggs(call: ServiceCall):
        """Reset daily egg counts."""
        for egg_type in EGG_TYPES:
            await hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": f"number.{egg_type}_eggs_daily", "value": 0},
            )

    async def save_storage_data(call: ServiceCall):
        """Save storage data."""
        # Implement logic to save storage data
        pass

    async def save_chicken_data(call: ServiceCall):
        """Save chicken population data."""
        # Implement logic to save chicken data
        pass

    async def save_hatchery_data(call: ServiceCall):
        """Save hatchery data."""
        # Implement logic to save hatchery data
        pass

    async def reset_purchase_inputs(call: ServiceCall):
        """Reset purchase input fields."""
        await hass.services.async_call(
            "number", "set_value", {"entity_id": "number.purchase_weight", "value": 0}
        )
        await hass.services.async_call(
            "number", "set_value", {"entity_id": "number.purchase_cost", "value": 0}
        )

    # Register services
    async_register_admin_service(
        hass, DOMAIN, "save_purchase", save_purchase, schema=SAVE_PURCHASE_SCHEMA
    )
    async_register_admin_service(
        hass, DOMAIN, "save_daily_eggs", save_daily_eggs, schema=SAVE_EGG_COLLECTION_SCHEMA
    )
    async_register_admin_service(hass, DOMAIN, "reset_daily_eggs", reset_daily_eggs)
    async_register_admin_service(hass, DOMAIN, "save_storage_data", save_storage_data)
    async_register_admin_service(hass, DOMAIN, "save_chicken_data", save_chicken_data)
    async_register_admin_service(hass, DOMAIN, "save_hatchery_data", save_hatchery_data)
    async_register_admin_service(hass, DOMAIN, "reset_purchase", reset_purchase_inputs)


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
        rand = str(time.time()).split(".")[0] + str(random.randint(100000, 999999))
        self._attr_unique_id = f"chicken_number_{unique_id}_{rand}"  # Ensure unique ID
        self._attr_name = name  # Set the entity name
        self._attr_icon = icon  # Set the entity icon
        self._attr_native_min_value = min_value  # Set the minimum value
        self._attr_native_max_value = max_value  # Set the maximum value
        self._attr_native_step = step  # Set the step value
        self._attr_native_unit_of_measurement = unit  # Set the unit of measurement
        self._attr_native_value = min_value  # Initialize with the minimum value

    def set_native_value(self, value: float) -> None:
        """Set a new value."""
        # Ensure the value is within the allowed range
        if value < self._attr_native_min_value:
            value = self._attr_native_min_value
        elif value > self._attr_native_max_value:
            value = self._attr_native_max_value
        self._attr_native_value = value
        self.async_write_ha_state()  # Notify Home Assistant of the state change


class EggsInStorageSensor(SensorEntity):
    """Sensor to track eggs in storage."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._attr_name = "Eggs in Storage"  # Readable name
        self._attr_unique_id = "chicken_eggs_in_storage"  # Unique ID for HA
        self._attr_native_value = 0  # Initial state
        self._attr_icon = "mdi:egg"  # Icon for the sensor
        self._attr_native_unit_of_measurement = "eggs"

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()

        # Track changes to relevant entities (number inputs)
        tracked_entities = [
            f"number.{egg_type}_eggs_daily" for egg_type in EGG_TYPES
        ] + [
            "number.broken_eggs",
            "number.eggs_sold_amount",
            "number.eggs_used",
            "number.eggs_to_hatchery",
        ]
        async_track_state_change(
            self.hass, tracked_entities, self._async_state_changed
        )

        # Calculate initial state
        await self._async_update_state()

    async def _async_state_changed(
        self, entity_id: str, old_state: str, new_state: str
    ) -> None:
        """Handle tracked entity state changes."""
        await self._async_update_state()

    async def _async_update_state(self) -> None:
        """Update the sensor state."""
        # Get values from the number entities, defaulting to 0 if not available
        total_eggs = sum(
            float(self.hass.states.get(f"number.{egg_type}_eggs_daily").state or 0)
            for egg_type in EGG_TYPES
        )
        broken_eggs = float(self.hass.states.get("number.broken_eggs").state or 0)
        sold_eggs = float(self.hass.states.get("number.eggs_sold_amount").state or 0)
        used_eggs = float(self.hass.states.get("number.eggs_used").state or 0)
        moved_eggs = float(self.hass.states.get("number.eggs_to_hatchery").state or 0)

        # Calculate eggs in storage
        self._attr_native_value = total_eggs - (
            broken_eggs + sold_eggs + used_eggs + moved_eggs
        )

        # Update the state in Home Assistant
        self.async_write_ha_state()
