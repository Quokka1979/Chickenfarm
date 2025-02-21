"""Sensor platform for Chicken Farm."""
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    PERCENTAGE,
    CURRENCY_EURO
)
from homeassistant.const import UnitOfMass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

DOMAIN = "chicken"

# Define a conversion factor for grams to kilograms
GRAMS_PER_KG = 1000

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    sensors = [
        # Egg Production Sensors remain the same
        ChickenSensor(
            "white_eggs_daily",
            "White Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.white_eggs_daily").state)
        ),
        ChickenSensor(
            "beige_eggs_daily",
            "Beige Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.beige_eggs_daily").state)
        ),
        ChickenSensor(
            "mint_eggs_daily",
            "Mint Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.mint_eggs_daily").state)
        ),
        ChickenSensor(
            "olive_eggs_daily",
            "Olive Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.olive_eggs_daily").state)
        ),
        ChickenSensor(
            "brown_eggs_daily",
            "Brown Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.brown_eggs_daily").state)
        ),
        ChickenSensor(
            "chocolate_eggs_daily",
            "Chocolate Eggs Today",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.chocolate_eggs_daily").state)
        ),
        ChickenSensor(
            "subtotal_eggs",
            "Subtotal Eggs",
            "mdi:egg-multiple",
            lambda hass: calculate_subtotal_eggs(hass)
        ),
        ChickenSensor(
            "broken_eggs",
            "Broken Eggs",
            "mdi:egg-off",
            lambda hass: float(hass.states.get("input_number.broken_eggs").state)
        ),
        ChickenSensor(
            "total_eggs",
            "Total Eggs",
            "mdi:egg-multiple",
            lambda hass: calculate_total_eggs(hass)
        ),
        
        # Storage and Sales sensors remain the same
        ChickenSensor(
            "eggs_in_storage",
            "Eggs in Storage",
            "mdi:egg",
            lambda hass: calculate_eggs_in_storage(hass)
        ),
        ChickenSensor(
            "eggs_used",
            "Eggs Used",
            "mdi:egg-off",
            lambda hass: float(hass.states.get("input_number.eggs_used").state)
        ),
        ChickenSensor(
            "eggs_to_hatchery",
            "Eggs to Hatchery",
            "mdi:egg-easter",
            lambda hass: float(hass.states.get("input_number.eggs_to_hatchery").state)
        ),
        ChickenSensor(
            "eggs_sold_amount",
            "Eggs Sold (Amount)",
            "mdi:egg",
            lambda hass: float(hass.states.get("input_number.eggs_sold_amount").state)
        ),
        ChickenSensor(
            "eggs_sold_value",
            "Eggs Sold (Value)",
            "mdi:cash",
            lambda hass: float(hass.states.get("input_number.eggs_sold_value").state),
            CURRENCY_EURO
        ),
        
        # Updated feed weight sensors to use UnitOfMass.GRAMS
        ChickenSensor(
            "pellets_kg",
            "Pellets Weight",
            "mdi:weight-kilogram",
            lambda hass: float(hass.states.get("input_number.pellets_kg").state) * GRAMS_PER_KG,
            UnitOfMass.GRAMS
        ),
        ChickenSensor(
            "pellets_cost",
            "Pellets Cost",
            "mdi:cash",
            lambda hass: float(hass.states.get("input_number.pellets_cost").state),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "scratch_grains_kg",
            "Scratch Grains Weight",
            "mdi:weight-kilogram",
            lambda hass: float(hass.states.get("input_number.scratch_grains_kg").state) * GRAMS_PER_KG,
            UnitOfMass.GRAMS
        ),
        ChickenSensor(
            "scratch_grains_cost",
            "Scratch Grains Cost",
            "mdi:cash",
            lambda hass: float(hass.states.get("input_number.scratch_grains_cost").state),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "bedding_cost",
            "Bedding Cost",
            "mdi:cash",
            lambda hass: float(hass.states.get("input_number.bedding_cost").state),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "misc_cost",
            "Miscellaneous Cost",
            "mdi:cash",
            lambda hass: float(hass.states.get("input_number.misc_cost").state),
            CURRENCY_EURO
        ),
        
        # Financial calculations remain the same
        ChickenSensor(
            "total_costs",
            "Total Costs",
            "mdi:cash-minus",
            lambda hass: calculate_total_costs(hass),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "profit_subtotal",
            "Profit Subtotal",
            "mdi:cash-plus",
            lambda hass: float(hass.states.get("input_number.eggs_sold_value").state),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "profit_total",
            "Profit Total",
            "mdi:cash",
            lambda hass: calculate_total_profit(hass),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "profit_per_egg",
            "Profit per Egg",
            "mdi:cash",
            lambda hass: calculate_profit_per_egg(hass),
            CURRENCY_EURO
        ),
        
        # Cost per unit calculations updated for grams
        ChickenSensor(
            "pellets_cost_per_kg",
            "Pellets Cost per KG",
            "mdi:scale-balance",
            lambda hass: calculate_cost_per_kg(hass, "pellets"),
            CURRENCY_EURO
        ),
        ChickenSensor(
            "scratch_grains_cost_per_kg",
            "Scratch Grains Cost per KG",
            "mdi:scale-balance",
            lambda hass: calculate_cost_per_kg(hass, "scratch_grains"),
            CURRENCY_EURO
        ),
        
        # Date tracking sensors remain the same
        TimestampSensor(
            "pellets_purchase_date",
            "Last Pellets Purchase",
            "mdi:calendar",
            "input_datetime.pellets_purchase_date"
        ),
        TimestampSensor(
            "scratch_grains_purchase_date",
            "Last Scratch Grains Purchase",
            "mdi:calendar",
            "input_datetime.scratch_grains_purchase_date"
        ),
        TimestampSensor(
            "bedding_purchase_date",
            "Last Bedding Purchase",
            "mdi:calendar",
            "input_datetime.bedding_purchase_date"
        )
    ]
    
    async_add_entities(sensors, True)

# Helper functions remain the same
def calculate_subtotal_eggs(hass):
    """Calculate subtotal of all eggs."""
    return sum(float(hass.states.get(f"input_number.{color}_eggs_daily").state) 
              for color in ['white', 'beige', 'mint', 'olive', 'brown', 'chocolate'])

def calculate_total_eggs(hass):
    """Calculate total eggs (subtotal - broken)."""
    subtotal = calculate_subtotal_eggs(hass)
    broken = float(hass.states.get("input_number.broken_eggs").state)
    return subtotal - broken

def calculate_eggs_in_storage(hass):
    """Calculate eggs currently in storage."""
    total = calculate_total_eggs(hass)
    used = float(hass.states.get("input_number.eggs_used").state)
    hatchery = float(hass.states.get("input_number.eggs_to_hatchery").state)
    sold = float(hass.states.get("input_number.eggs_sold_amount").state)
    return total - used - hatchery - sold

def calculate_total_costs(hass):
    """Calculate total costs."""
    costs = [
        "pellets_cost",
        "scratch_grains_cost",
        "bedding_cost",
        "misc_cost"
    ]
    return sum(float(hass.states.get(f"input_number.{cost}").state) for cost in costs)

def calculate_total_profit(hass):
    """Calculate total profit."""
    revenue = float(hass.states.get("input_number.eggs_sold_value").state)
    costs = calculate_total_costs(hass)
    return revenue - costs

def calculate_profit_per_egg(hass):
    """Calculate profit per egg sold."""
    sold_amount = float(hass.states.get("input_number.eggs_sold_amount").state)
    if sold_amount > 0:
        total_profit = calculate_total_profit(hass)
        return round(total_profit / sold_amount, 2)
    return 0

def calculate_cost_per_kg(hass, feed_type):
    """Calculate cost per kg for feed type."""
    kg = float(hass.states.get(f"input_number.{feed_type}_kg").state)
    cost = float(hass.states.get(f"input_number.{feed_type}_cost").state)
    return round(cost / kg, 2) if kg > 0 else 0

class ChickenSensor(SensorEntity):
    """Representation of a Chicken Farm Sensor."""

    def __init__(self, unique_id, name, icon, calculate_value, unit=None):
        """Initialize the sensor."""
        self._unique_id = unique_id
        self._name = name
        self._icon = icon
        self._calculate_value = calculate_value
        self._unit = unit
        self._state = None
        
    @property
    def unique_id(self):
        """Return unique ID."""
        return f"chicken_{self._unique_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    async def async_update(self):
        """Update the sensor."""
        self._state = self._calculate_value(self.hass)

class TimestampSensor(SensorEntity):
    """Sensor that tracks purchase dates."""
    
    def __init__(self, unique_id, name, icon, datetime_entity):
        """Initialize the timestamp sensor."""
        self._unique_id = unique_id
        self._name = name
        self._icon = icon
        self._datetime_entity = datetime_entity
        self._state = None

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"chicken_{self._unique_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the sensor."""
        state = self.hass.states.get(self._datetime_entity)
        if state:
            self._state = state.state