import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from .const import *

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the number platform."""
    adapter = hass.data[DOMAIN][entry.entry_id]
    
    entity = ModeSelectEntity(
            hass,
            adapter,
            MODE_NAME,
            MODE_OPTIONS,
            MODE_DEFAULT
        )
    adapter.mode = entity
    async_add_entities([entity])

class ModeSelectEntity(SelectEntity, RestoreEntity):
    def __init__(self, hass, adapter, name, options, default):
        self._hass = hass
        self._adapter = adapter
        self._attr_name = name
        self._attr_options = options
        self._default = default
        self._attr_current_option = default
        self._attr_icon = "mdi:led-strip-variant-off" if default=="Off" else "mdi:led-strip-variant"
        
        self.editable = False
        
        # Unique ID for entity registration
        self.entity_id = f"select.{DOMAIN}_mode"
        self._attr_unique_id = f"{DOMAIN}_mode_str"
        
		# Привязка к устройству
        self._attr_device_info = adapter.device_info
        
    async def async_select_option(self, option):
        """Update the current selected option."""
        if option not in self._attr_options:
            raise ValueError(f"Invalid option: {option}")
        
        self._attr_current_option = option
        self._attr_icon = "mdi:led-strip-variant-off" if option=="Off" else "mdi:led-strip-variant"
        await self._adapter.update_device()
        self.async_write_ha_state()  # Сохраняем состояние

    async def async_added_to_hass(self):
        """Restore state when entity added to hass."""
        await super().async_added_to_hass()
        
        # Восстанавливаем состояние из хранилища
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state in self.options:
                self._attr_current_option = last_state.state
                _LOGGER.info("Restored state for %s: %s", self.entity_id, self._attr_current_option)
            else:
                self._attr_current_option = self._default
                _LOGGER.warning("Invalid state for %s", self.entity_id)
        else:
            self._attr_current_option = self._default
            _LOGGER.info("No previous state for %s, using default", self.entity_id)
            
        self._attr_icon = "mdi:led-strip-variant-off" if self._attr_current_option=="Off" else "mdi:led-strip-variant"
