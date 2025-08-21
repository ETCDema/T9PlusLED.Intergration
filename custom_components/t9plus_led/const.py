from typing import Dict

DOMAIN = "t9plus_led"

DEVICE_NAME = "T9Plus LED"
DEVICE_ID = "t9plus_led_device"  # Уникальный идентификатор устройства

# The baud rate is fixed at 10000 for the device's controller.
BAUD_RATE: int = 10000

# The first byte sent in every command sequence.
BEGIN_BYTE: bytes = b'\xfa'

# Maps user-friendly mode names to their corresponding byte codes.
MODE_BYTES: Dict[str, bytes] = {
  'Off':       b'\x04',
  'Auto':      b'\x05',
  'Rainbow':   b'\x01',
  'Breathing': b'\x02',
  'Cycle':     b'\x03',
}

# Maps brightness levels (1-5) to their byte codes.
# Note: The device uses inverted logic (level 5 is brightest).
BRIGHTNESS_BYTES: Dict[int, bytes] = {
  5: b'\x01',  # Brightest
  4: b'\x02',
  3: b'\x03',
  2: b'\x04',
  1: b'\x05',  # Dimmest
}

# Maps speed levels (1-5) to their byte codes.
# Note: The device uses inverted logic (level 5 is fastest).
SPEED_BYTES: Dict[int, bytes] = {
  5: b'\x01',  # Fastest
  4: b'\x02',
  3: b'\x03',
  2: b'\x04',
  1: b'\x05',  # Slowest
}

MODE_NAME = " Mode"
MODE_OPTIONS = list(MODE_BYTES.keys())
MODE_DEFAULT = "Off"

BRIGHTNESS_NAME = "Brightness"
BRIGHTNESS_MIN = 1
BRIGHTNESS_MAX = 5
BRIGHTNESS_STEP = 1
BRIGHTNESS_DEFAULT = 1

SPEED_NAME = "Speed"
SPEED_MIN = 1
SPEED_MAX = 5
SPEED_STEP = 1
SPEED_DEFAULT = 1
