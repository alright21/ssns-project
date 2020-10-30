import requests
import time
import serial
import sys
from requests.exceptions import HTTPError

# serial configuration parameters
port = '/dev/ttyS6'
baud_rate = 9600


# variable used to extract packet data
startMarker = '{'
endMarker = '}'
dataStarted = False
dataBuf = ""
messageComplete = False

# decode message in utf-8, catching errors
def decode_utf8(text):
    try:
        text = text.decode('utf-8')
    except UnicodeDecodeError:
        print(text)
        return 'Unable to decode the bytes'
    return text

# set up the Arduino serial listener
def setupSerial(baudRate, serialPortName):
    
    global arduino
    try:
        arduino = serial.Serial(serialPortName, 
                            baudRate,
                            parity=serial.PARITY_EVEN, 
                            stopbits=serial.STOPBITS_ONE, 
                            bytesize=serial.EIGHTBITS, 
                            timeout=1)
        print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))
        waitForArduino()
    except serial.SerialException as se:
        
        print(f'Serial Exception: {se.strerror}\nProgram will be closed')
        quit()

    


#Receive and exttract Arduino data. Packet example {1,2,3}

def recvLikeArduino():

    global startMarker, endMarker, dataStarted, dataBuf, messageComplete
    if arduino.in_waiting > 0 and messageComplete == False:
        
        x = arduino.read()
        # decode needed for Python3
        x = decode_utf8(x)
        
        if x=='Unable to decode the bytes':
            print(x)
            return "Error"

        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ''
            dataStarted = True
    
    if (messageComplete == True):
        messageComplete = False
        return dataBuf
    else:
        return "Error"

#reset the Arduino and wait for the welcoming packet: {Arduino is ready}

def waitForArduino():

    print("Waiting for Arduino to reset")
    print(arduino.get_settings())
    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == 'Error'):
            print(msg)
        

# Transform raw data in JSON data, rady to be sent to the server
def prepareData(raw_data):

    data_list = raw_data.rsplit(',')
    data_object = {}
    if len(data_list) == 3:
        
        data_object["node_id"] = data_list[0]
        data_object["light"] = data_list[1]
        data_object["range"] = data_list[2]
    
    return data_object


# sends data to the server
def sendData(url, data):

    try:

        response = requests.post(url = url, data = data)
        response.raise_for_status()

    except HTTPError as httpError:
        print(f'HTTP error occurred: {httpError}')
    except Exception as error:
        print(f'Other errors has occurred: {error}')
    else:
        print(f'POST request success: {response.status_code}')


setupSerial(baud_rate, port)
while True:
    
    # check for a reply
    arduinoReply = recvLikeArduino()

    if not (arduinoReply == 'Error'):
        data = prepareData(arduinoReply)
        print(data)
        url = 'http://localhost:8000/api/measures/'
        sendData(url, data)


        

