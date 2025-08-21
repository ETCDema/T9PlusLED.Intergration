import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import RestoreNumber, NumberMode
from .const import *

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the number platform."""
    adapter = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        DeviceNumberEntity(
            hass,
            adapter,
            'brightness',
            BRIGHTNESS_NAME,
            BRIGHTNESS_MIN,
            BRIGHTNESS_MAX,
            BRIGHTNESS_STEP,
            BRIGHTNESS_DEFAULT,
            "mdi:brightness-6"
        ),
        DeviceNumberEntity(
            hass,
            adapter,
            'speed',
            SPEED_NAME,
            SPEED_MIN,
            SPEED_MAX,
            SPEED_STEP,
            SPEED_DEFAULT,
            "mdi:play-speed"
        )
    ]
    
    # Сохраняем ссылки на сущности в устройстве
    adapter.brightness = entities[0]
    adapter.speed = entities[1]
    
    async_add_entities(entities)

class DeviceNumberEntity(RestoreNumber):
    def __init__(self, hass, adapter, entity_type, name, min_val, max_val, step, default, icon):
        self._hass = hass
        self._adapter = adapter
        self._type = entity_type
        self._attr_name = name
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_mode = NumberMode.SLIDER
        self._default = default
        self._attr_native_value = default
        self._attr_icon = icon
        
        self.editable = False
        
        # Unique ID for entity registration
        self.entity_id = f"number.{DOMAIN}_{entity_type}"
        self._attr_unique_id = f"{DOMAIN}_{entity_type}_num"
        
		# Привязка к устройству
        self._attr_device_info = adapter.device_info

    async def async_set_native_value(self, value):
        """Update the current value."""
        self._attr_native_value = value
        
        # Send update to physical device
        self._adapter.update_device()
        self.async_write_ha_state()  # Сохраняем состояние

    async def async_added_to_hass(self):
        """Restore state when entity added to hass."""
        await super().async_added_to_hass()
        
        # Восстанавливаем состояние из хранилища
        if (last_state := await self.async_get_last_number_data()) is not None:
            try:
                self._attr_native_value = last_state.native_value
                _LOGGER.info("Restored state for %s: %s", self.entity_id, self._attr_native_value)
            except (ValueError, TypeError):
                self._attr_native_value = self._default
                _LOGGER.warning("Invalid state for %s", self.entity_id)
        else:
            self._attr_native_value = self._default
            _LOGGER.info("No previous state for %s, using default", self.entity_id)
