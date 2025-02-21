"""The Chicken Farm integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_FARM_NAME,
    CONF_FARM_SIZE,
    CONF_CHICKEN_TYPE,
    DEFAULT_FARM_NAME,
    DEFAULT_FARM_SIZE,
    DEFAULT_CHICKEN_TYPE,
)

# Configuration schema for YAML (optional if using config flow)
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_FARM_NAME, default=DEFAULT_FARM_NAME): cv.string,
                vol.Optional(CONF_FARM_SIZE, default=DEFAULT_FARM_SIZE): cv.string,
                vol.Optional(CONF_CHICKEN_TYPE, default=DEFAULT_CHICKEN_TYPE): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Chicken Farm component from YAML."""
    conf = config.get(DOMAIN)
    hass.data.setdefault(DOMAIN, {})

    if conf is not None:
        # Trigger config flow for YAML configuration
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": "import"},
                data=conf,
            )
        )

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Chicken Farm from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the platforms (e.g., sensor, input_number)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up scripts
    from .script import async_setup_scripts
    await async_setup_scripts(hass)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms (e.g., sensor, input_number)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Remove the entry data from hass.data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok