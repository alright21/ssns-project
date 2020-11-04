import serial
import time
from digi.xbee.devices import ZigBeeDevice
from digi.xbee.models.mode import OperatingMode

arduino = ZigBeeDevice('/dev/ttyS6', 9600)
arduino.open()
print('done')
print(arduino.get_64bit_addr())