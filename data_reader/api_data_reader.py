import serial
import time
from digi.xbee.devices import ZigBeeDevice


ser = serial.Serial('/dev/ttyS6', 9600)
ser.write(str.encode("\n\n"))
time.sleep(0.1)
ser.write(str.encode("B"))
time.sleep(0.1)
ser.close()
print('done')
device = ZigBeeDevice('/dev/ttyS6', 9600, parity=serial.PARITY_EVEN)

device.open()

print('opened')

xbee_message = device.read_data()

remote_device = xbee_message.remote_device
data = xbee_message.data
is_broadcast = xbee_message.is_broadcast
timestamp = xbee_message.timestamp

print(xbee_message)
