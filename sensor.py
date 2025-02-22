from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    PERCENTAGE,
    CURRENCY_EURO,
    UnitOfMass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

DOMAIN = "chicken"

# Conversion factor for grams to kilograms
GRAMS_PER_KG = 1000

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    sensors = [
        # Egg Production Sensors
        ChickenSensor("white_eggs_daily", "White Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.white_eggs_daily").state)),
        ChickenSensor("beige_eggs_daily", "Beige Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.beige_eggs_daily").state)),
        ChickenSensor("mint_eggs_daily", "Mint Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.mint_eggs_daily").state)),
        ChickenSensor("olive_eggs_daily", "Olive Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.olive_eggs_daily").state)),
        ChickenSensor("brown_eggs_daily", "Brown Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.brown_eggs_daily").state)),
        ChickenSensor("chocolate_eggs_daily", "Chocolate Eggs Today", "mdi:egg", lambda hass: float(hass.states.get("input_number.chocolate_eggs_daily").state)),
        ChickenSensor("subtotal_eggs", "Subtotal Eggs", "mdi:egg-multiple", lambda hass: calculate_subtotal_eggs(hass)),
        ChickenSensor("broken_eggs", "Broken Eggs", "mdi:egg-off", lambda hass: float(hass.states.get("input_number.broken_eggs").state)),
        ChickenSensor("total_eggs", "Total Eggs", "mdi:egg-multiple", lambda hass: calculate_total_eggs(hass)),

        # Storage and Usage Sensors
        ChickenSensor("eggs_in_storage", "Eggs in Storage", "mdi:egg", lambda hass: calculate_eggs_in_storage(hass)),
        ChickenSensor("eggs_used", "Eggs Used", "mdi:egg-off", lambda hass: float(hass.states.get("input_number.eggs_used").state)),
        ChickenSensor("eggs_to_hatchery", "Eggs to Hatchery", "mdi:egg-easter", lambda hass: float(hass.states.get("input_number.eggs_to_hatchery").state)),
        ChickenSensor("eggs_sold_amount", "Eggs Sold (Amount)", "mdi:egg", lambda hass: float(hass.states.get("input_number.eggs_sold_amount").state)),
        ChickenSensor("eggs_sold_value", "Eggs Sold (Value)", "mdi:cash", lambda hass: float(hass.states.get("input_number.eggs_sold_value").state), CURRENCY_EURO),

        # Feed and Purchase Sensors
        ChickenSensor("pellets_kg", "Pellets Weight", "mdi:weight-kilogram", lambda hass: float(hass.states.get("input_number.pellets_kg").state) * GRAMS_PER_KG, UnitOfMass.GRAMS),
        ChickenSensor("pellets_cost", "Pellets Cost", "mdi:cash", lambda hass: float(hass.states.get("input_number.pellets_cost").state), CURRENCY_EURO),
        ChickenSensor("scratch_grains_kg", "Scratch Grains Weight", "mdi:weight-kilogram", lambda hass: float(hass.states.get("input_number.scratch_grains_kg").state) * GRAMS_PER_KG, UnitOfMass.GRAMS),
        ChickenSensor("scratch_grains_cost", "Scratch Grains Cost", "mdi:cash", lambda hass: float(hass.states.get("input_number.scratch_grains_cost").state), CURRENCY_EURO),
        ChickenSensor("bedding_cost", "Bedding Cost", "mdi:cash", lambda hass: float(hass.states.get("input_number.bedding_cost").state), CURRENCY_EURO),
        ChickenSensor("misc_cost", "Miscellaneous Cost", "mdi:cash", lambda hass: float(hass.states.get("input_number.misc_cost").state), CURRENCY_EURO),
        ChickenSensor("total_costs", "Total Costs", "mdi:cash-minus", lambda hass: calculate_total_costs(hass), CURRENCY_EURO),
        ChickenSensor("pellets_cost_per_kg", "Pellets Cost per KG", "mdi:scale-balance", lambda hass: calculate_cost_per_kg(hass, "pellets"), CURRENCY_EURO),
        ChickenSensor("scratch_grains_cost_per_kg", "Scratch Grains Cost per KG", "mdi:scale-balance", lambda hass: calculate_cost_per_kg(hass, "scratch_grains"), CURRENCY_EURO),

        # Financial Sensors
        ChickenSensor("profit_subtotal", "Profit Subtotal", "mdi:cash-plus", lambda hass: float(hass.states.get("input_number.eggs_sold_value").state), CURRENCY_EURO),
        ChickenSensor("profit_total", "Profit Total", "mdi:cash", lambda hass: calculate_total_profit(hass), CURRENCY_EURO),
        ChickenSensor("profit_per_egg", "Profit per Egg", "mdi:cash", lambda hass: calculate_profit_per_egg(hass), CURRENCY_EURO),

        # Date Tracking Sensors
        TimestampSensor("pellets_purchase_date", "Last Pellets Purchase", "mdi:calendar", "input_datetime.pellets_purchase_date"),
        TimestampSensor("scratch_grains_purchase_date", "Last Scratch Grains Purchase", "mdi:calendar", "input_datetime.scratch_grains_purchase_date"),
        TimestampSensor("bedding_purchase_date", "Last Bedding Purchase", "mdi:calendar", "input_datetime.bedding_purchase_date"),

        # New Sensors
        ChickenSensor("eggs_laid_7_days", "Eggs Laid (Last 7 Days)", "mdi:egg", lambda hass: calculate_eggs_laid_7_days(hass)),
        ChickenSensor("eggs_in_storage_7_days", "Eggs in Storage (Last 7 Days)", "mdi:egg", lambda hass: calculate_eggs_in_storage_7_days(hass)),
        ChickenSensor("last_sale_1", "Last Sale 1", "mdi:cash", lambda hass: calculate_last_sale(hass, 1)),
        ChickenSensor("last_sale_2", "Last Sale 2", "mdi:cash", lambda hass: calculate_last_sale(hass, 2)),
        ChickenSensor("last_sale_3", "Last Sale 3", "mdi:cash", lambda hass: calculate_last_sale(hass, 3)),
        ChickenSensor("last_sale_4", "Last Sale 4", "mdi:cash", lambda hass: calculate_last_sale(hass, 4)),
        ChickenSensor("last_sale_5", "Last Sale 5", "mdi:cash", lambda hass: calculate_last_sale(hass, 5)),
        ChickenSensor("last_sale_6", "Last Sale 6", "mdi:cash", lambda hass: calculate_last_sale(hass, 6)),
        ChickenSensor("last_purchase_1", "Last Purchase 1", "mdi:cart", lambda hass: calculate_last_purchase(hass, 1)),
        ChickenSensor("last_purchase_2", "Last Purchase 2", "mdi:cart", lambda hass: calculate_last_purchase(hass, 2)),
        ChickenSensor("last_purchase_3", "Last Purchase 3", "mdi:cart", lambda hass: calculate_last_purchase(hass, 3)),
        ChickenSensor("last_purchase_4", "Last Purchase 4", "mdi:cart", lambda hass: calculate_last_purchase(hass, 4)),
        ChickenSensor("last_purchase_5", "Last Purchase 5", "mdi:cart", lambda hass: calculate_last_purchase(hass, 5)),
        ChickenSensor("last_purchase_6", "Last Purchase 6", "mdi:cart", lambda hass: calculate_last_purchase(hass, 6)),

        # Chicken Population Sensors
        ChickenSensor(
            "total_chickens",
            "Total Chickens",
            "mdi:egg",
            lambda hass: calculate_total_chickens(hass)
        ),
        ChickenSensor(
            "days_to_hatch",
            "Days to Hatch",
            "mdi:calendar-clock",
            lambda hass: calculate_days_to_hatch(hass)
        ),
        ChickenSensor(
            "hatchery_status",
            "Hatchery Status",
            "mdi:egg-easter",
            lambda hass: calculate_hatchery_status(hass)
        )  # Added missing closing parenthesis
    ]  # This closing bracket now matches the opening bracket from the sensors list

    async_add_entities(sensors, True)

    async_add_entities(sensors, True)

# Helper functions
def calculate_subtotal_eggs(hass):
    """Calculate subtotal of all eggs."""
    return sum(float(hass.states.get(f"input_number.{color}_eggs_daily").state) for color in ['white', 'beige', 'mint', 'olive', 'brown', 'chocolate'])

def calculate_total_eggs(hass):
    """Calculate total eggs (subtotal - broken)."""
    return calculate_subtotal_eggs(hass) - float(hass.states.get("input_number.broken_eggs").state)

def calculate_eggs_in_storage(hass):
    """Calculate eggs currently in storage."""
    total = calculate_total_eggs(hass)
    used = float(hass.states.get("input_number.eggs_used").state)
    hatchery = float(hass.states.get("input_number.eggs_to_hatchery").state)
    sold = float(hass.states.get("input_number.eggs_sold_amount").state)
    return total - used - hatchery - sold

def calculate_total_costs(hass):
    """Calculate total costs."""
    return sum(float(hass.states.get(f"input_number.{cost}").state) for cost in ['pellets_cost', 'scratch_grains_cost', 'bedding_cost', 'misc_cost'])

def calculate_cost_per_kg(hass, cost_type):
    """Calculate cost per kg."""
    if cost_type == "pellets":
        return float(hass.states.get("input_number.pellets_cost").state) / (float(hass.states.get("input_number.pellets_kg").state) or 1)
    elif cost_type == "scratch_grains":
        return float(hass.states.get("input_number.scratch_grains_cost").state) / (float(hass.states.get("input_number.scratch_grains_kg").state) or 1)

def calculate_total_profit(hass):
    """Calculate total profit."""
    return float(hass.states.get("input_number.eggs_sold_value").state) - calculate_total_costs(hass)

def calculate_profit_per_egg(hass):
    """Calculate profit per egg."""
    return calculate_total_profit(hass) / (calculate_total_eggs(hass) or 1)

def calculate_eggs_laid_7_days(hass):
    """Calculate the eggs laid in the last 7 days."""
    return sum([float(hass.states.get(f"input_number.{day}_eggs_daily").state) for day in range(1, 8)])

def calculate_eggs_in_storage_7_days(hass):
    """Calculate the eggs in storage over the last 7 days."""
    return sum([float(hass.states.get(f"input_number.{day}_eggs_in_storage").state) for day in range(1, 8)])

def calculate_last_sale(hass, sale_number):
    """Calculate the last sale date and amount."""
    return hass.states.get(f"input_number.last_sale_{sale_number}").state

def calculate_last_purchase(hass, purchase_number):
    """Calculate the last purchase date and amount."""
    return hass.states.get(f"input_number.last_purchase_{purchase_number}").state

def calculate_total_chickens(hass):
    """Calculate total number of chickens."""
    hens = float(hass.states.get("input_number.number_of_hens").state)
    roosters = float(hass.states.get("input_number.number_of_roosters").state)
    died = float(hass.states.get("input_number.chicken_died").state)
    butchered = float(hass.states.get("input_number.chicken_butchered").state)
    return hens + roosters - died - butchered

def calculate_days_to_hatch(hass):
    """Calculate days remaining until eggs hatch."""
    # Assuming 21 days for chicken eggs to hatch
    eggs_in_hatchery = float(hass.states.get("input_number.eggs_in_hatchery").state)
    if eggs_in_hatchery > 0:
        return 21
    return 0

def calculate_hatchery_status(hass):
    """Calculate current hatchery status."""
    in_hatchery = float(hass.states.get("input_number.eggs_in_hatchery").state)
    hatched = float(hass.states.get("input_number.hatched_eggs").state)
    died = float(hass.states.get("input_number.died_eggs").state)
    return f"In Hatchery: {in_hatchery}, Hatched: {hatched}, Died: {died}"
