import serial

ser = serial.Serial('/dev/ttyS6')

print(ser.name)
while True:
    print(ser.readline())

ser.close()