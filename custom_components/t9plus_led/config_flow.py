import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required("device", 
                                    	default="/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0", 
                                        description="Path to USB device with substring '*1a86_USB_Serial-if00*'"
                                      ): str})

class T9PlusLEDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """T9Plus LED config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 0
    MINOR_VERSION = 1
    
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                if len(user_input["device"]) < 5:
                    errors["device"] = "device_required"
                else:
                    return self.async_create_entry(title="T9Plus LED", data=user_input)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
                
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )