"""Constants for the Chicken Farm integration."""
from homeassistant.const import Platform

# Domain and platforms
DOMAIN = "chicken"
PLATFORMS = [Platform.SENSOR, Platform.NUMBER]  # Removed Platform.SCRIPT

# Configuration keys
CONF_FARM_NAME = "farm_name"
CONF_FARM_SIZE = "farm_size"
CONF_CHICKEN_TYPE = "chicken_type"

# Default values
DEFAULT_FARM_NAME = "My Chicken Farm"
DEFAULT_FARM_SIZE = "Small"
DEFAULT_CHICKEN_TYPE = "Rhode Island Red"

# Units
UNIT_KG = "kg"
UNIT_EURO = "€"

# Entity IDs
ENTITY_EGGS_IN_STORAGE = "sensor.eggs_in_storage"
ENTITY_TOTAL_COSTS = "sensor.total_costs"

# Error Messages
ERROR_INVALID_FARM_SIZE = "Invalid farm size. Choose from Small, Medium, or Large."
ERROR_INVALID_CHICKEN_TYPE = "Invalid chicken type. Choose from Rhode Island Red, Plymouth Rock, or Sussex."

# Purchase Types
PURCHASE_TYPES = ["Pellets", "Scratch Grains", "Bedding", "Misc"]

# Egg Types
EGG_TYPES = ["white", "beige", "mint", "olive", "brown", "chocolate"]

# Chicken Types
CHICKEN_TYPES = ["Rhode Island Red", "Plymouth Rock", "Sussex"]

# Farm Sizes
FARM_SIZES = ["Small", "Medium", "Large"]