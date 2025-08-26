# [EN] Home Assistant integration for controlling the LED backlight of the Mini PC T9 Plus

## Installation via HACS

1. [HACS](https://www.hacs.xyz/) must be installed in the Home Assistant.
2. Add a custom repository in the HACS settings https://github.com/ETCDema/T9PlusLED.Intergration.git with the `Integration` type
3. Open and download the integration   
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ETCDema&repository=T9PlusLED.Intergration&category=Intergration)

## Manual installation

1. Download the catalog https://github.com/ETCDema/T9PlusLED.Intergration/tree/main/custom_components/t9plus_led to the Home Assistant components `/config/custom_components`
2. Restart the Home Assistant

## Setting up

1. Add T9Plus LED integration  
   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=t9plus_led)
2. Specify the control device, usually it is `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0`
3. A `T9Plus LED` device and three controls will be created: operating mode, speed and brightness

## Possible problems

For a detailed diagnosis of problems, see the Home Assistant log.

### Integration does not change the backlight state

Such problems are usually accompanied by errors writing to `SerialPort` and you need to try changing the device to `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0`, perhaps the device on your Mini PC has a different identifier.

# [RU] Home Assistant интеграция для управления LED подсветкой Mini PC T9 Plus

## Установка через HACS

1. В Home Assistant должен быть установлен [HACS](https://www.hacs.xyz/).
2. В настройках HACS добавте пользовательский репозиторий https://github.com/ETCDema/T9PlusLED.Intergration.git с типом `Integration`
3. Откройте и скачайте интеграцию   
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ETCDema&repository=T9PlusLED.Intergration&category=Intergration)

## Ручная установка

1. Сачайте каталог https://github.com/ETCDema/T9PlusLED.Intergration/tree/main/custom_components/t9plus_led к компонентам Home Assistant `/config/custom_components`
2. Перезапустите Home Assistant

## Настройка

1. Добавьте интеграцию T9Plus LED  
   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=t9plus_led)
2. Укажите устройство для управления, обычно это `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0`
3. Будет создано устройство `T9Plus LED` и три элемента управления: режим работы, скорость и яркость

## Возможные проблемы

Для детальной диагностики проблем смотрите лог Home Assistant.

### Интеграция не меняет состояние подсветки

Такие проблемы обычно сопровождаются ошибками записи в `SerialPort` и нужно попробовать изменить устройство `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0`, возможно на вашем Mini PC устройство имеет другой идентификатор.
