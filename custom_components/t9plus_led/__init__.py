import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.config_entries import ConfigEntry
from .device_adapter import DeviceAdapter
from .const import *

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration."""
    # Создаем объект управления
    adapter = DeviceAdapter(hass, entry.data["device"])
    hass.data[DOMAIN] = { entry.entry_id: adapter }
	
	# Создаем устройство в реестре устройств
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, DEVICE_ID)},
        name=DEVICE_NAME,
    )
    # Данные устройства для элементов управления
    adapter.device_id = device.id
    adapter.device_info = dr.DeviceInfo(
        identifiers={(DOMAIN, DEVICE_ID)},
        name=DEVICE_NAME,
	)
    
    # Создаем элементы управления
    await hass.config_entries.async_forward_entry_setups(entry, ['select', 'number'])

    # Инициализируем устройство по значениям созданных элементов
    await adapter.update_device()

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    adapter = hass.data[DOMAIN][entry.entry_id]
    
	# Удаляем все сущности
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [ 'select', 'number' ])
    if unload_ok:
        # Удаляем устройство
        if adapter.device_id:
            device_registry = dr.async_get(hass)
            device_registry.async_remove_device(adapter.device_id)
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok