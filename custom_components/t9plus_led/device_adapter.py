"""
Controls the RGB LED on a T9 Plus mini PC via a serial connection.

This script sends a 5-byte command packet to the device's serial port
to set the LED mode, brightness, and animation speed.
"""

import logging
import time
from typing import List

from homeassistant.helpers import device_registry as dr
from .const import *
from .select import ModeSelectEntity
from .number import DeviceNumberEntity

_LOGGER = logging.getLogger(__name__)

try:
  import serial
except ImportError:
  _LOGGER.error("Error: The 'pyserial' library is required. Please install it using 'pip install pyserial'")

# --- Protocol Constants ---
class DeviceAdapter:
  def __init__(self, hass, device: str):
    self.hass = hass
    self._device = device
    self.mode: ModeSelectEntity
    self.brightness: DeviceNumberEntity
    self.speed: DeviceNumberEntity
    self.device_id: str
    self.device_info: dr.DeviceInfo
	
  def update_device(self):
    """Send parameters to physical device"""
    # Implement your device communication here
    # Example: serial.write(f"{self.brightness},{self.speed},{self.mode}")
    self.set_state()

  def set_state(self):
    try:
      command_packet        = self.build_command_packet(self.mode.current_option or 'Auto', int(self.brightness.native_value or 3), int(self.speed.native_value or 3))
      self.send_command(self._device, command_packet, False)
      _LOGGER.info(
    	"New LED state: %s 🔅 %s ⏩ %s",
        self.mode.state,
        self.brightness.native_value,
        self.speed.native_value
      )
    except serial.SerialException as e:
      _LOGGER.error(f"Could not open serial port '{self._device}': {e}.")
      _LOGGER.error("Please ensure the device is connected and you have selected the correct port.")
    except Exception as e:
      _LOGGER.error(f"An unexpected error occurred: {e}")

  def build_command_packet(self, mode: str, brightness: int, speed: int) -> List[bytes]:
    """
    Constructs the 5-byte command sequence to be sent to the LED controller.

    Args:
      mode: The desired LED mode (e.g., 'rainbow').
      brightness: The brightness level as a string ('1' through '5').
      speed: The speed level as a string ('1' through '5').

    Returns:
      A list of single-byte objects representing the full command packet.
    """
    mode_byte       = MODE_BYTES[mode] or b'\x05'
    brightness_byte = BRIGHTNESS_BYTES[brightness] or b'\x03'
    speed_byte      = SPEED_BYTES[speed] or b'\x03'

    # The checksum is the sum of the command bytes, truncated to 8 bits.
    checksum_val    = (BEGIN_BYTE[0] + mode_byte[0] + brightness_byte[0] + speed_byte[0]) & 0xFF
    checksum_byte   = checksum_val.to_bytes(1, 'big')

    return [
      BEGIN_BYTE,
      mode_byte,
      brightness_byte,
      speed_byte,
      checksum_byte,
    ]

  def send_command(self, serial_port: str, packet: List[bytes], verbose: bool):
    """
    Opens the serial port and sends the command packet byte by byte.

    Args:
      serial_port: The name of the serial port (e.g., 'COM3' or '/dev/ttyUSB1').
      packet: The 5-byte command packet to send.
      verbose: If True, prints detailed debugging information.

    Raises:
      serial.SerialException: If the port cannot be opened or written to.
    """
    if verbose: _LOGGER.debug(f"Connecting to {serial_port} at {BAUD_RATE} baud...")
    # Using a 'with' statement ensures the serial port is automatically closed.
    with serial.Serial(serial_port, BAUD_RATE, timeout=1) as s:
      
      if verbose: _LOGGER.info("Sending command packet...")
      for byte_to_send in packet:
        s.write(byte_to_send)
        # The hex representation is useful for debugging the protocol.
        if verbose:
          _LOGGER.debug(f" -> Sent {byte_to_send.hex()}")
        # A small delay seems to be required between sending each byte.
        time.sleep(0.005)
        
    if verbose: _LOGGER.debug("Command sent successfully.")