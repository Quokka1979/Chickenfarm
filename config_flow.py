"""Config flow for Chicken Farm integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    CONF_FARM_NAME,
    CONF_FARM_SIZE,
    CONF_CHICKEN_TYPE,
    DEFAULT_FARM_NAME,
    DEFAULT_FARM_SIZE,
    DEFAULT_CHICKEN_TYPE,
)

# Validation constants
VALID_FARM_SIZES = ["Small", "Medium", "Large"]
VALID_CHICKEN_TYPES = ["Rhode Island Red", "Plymouth Rock", "Sussex"]

class ChickenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Chicken Farm."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            farm_size = user_input[CONF_FARM_SIZE]
            chicken_type = user_input[CONF_CHICKEN_TYPE]

            if farm_size not in VALID_FARM_SIZES:
                errors[CONF_FARM_SIZE] = "invalid_farm_size"
            if chicken_type not in VALID_CHICKEN_TYPES:
                errors[CONF_CHICKEN_TYPE] = "invalid_chicken_type"

            if not errors:
                return self.async_create_entry(
                    title=user_input.get(CONF_FARM_NAME, DEFAULT_FARM_NAME),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_FARM_NAME, default=DEFAULT_FARM_NAME): str,
                vol.Required(CONF_FARM_SIZE, default=DEFAULT_FARM_SIZE): vol.In(VALID_FARM_SIZES),
                vol.Required(CONF_CHICKEN_TYPE, default=DEFAULT_CHICKEN_TYPE): vol.In(VALID_CHICKEN_TYPES),
            }),
            errors=errors,
        )

    async def async_step_import(self, import_config):
        """Handle import from YAML."""
        return self.async_create_entry(
            title=import_config.get(CONF_FARM_NAME, DEFAULT_FARM_NAME),
            data=import_config,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ChickenOptionsFlow(config_entry)

class ChickenOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Chicken Farm integration."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_FARM_NAME, 
                    default=self.config_entry.data.get(CONF_FARM_NAME, DEFAULT_FARM_NAME)): str,
                vol.Required(CONF_FARM_SIZE, 
                    default=self.config_entry.data.get(CONF_FARM_SIZE, DEFAULT_FARM_SIZE)): vol.In(VALID_FARM_SIZES),
                vol.Required(CONF_CHICKEN_TYPE, 
                    default=self.config_entry.data.get(CONF_CHICKEN_TYPE, DEFAULT_CHICKEN_TYPE)): vol.In(VALID_CHICKEN_TYPES),
            }),
        )