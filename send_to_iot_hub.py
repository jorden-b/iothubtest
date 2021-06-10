# pylint: disable=W0603
"""Script that sends commands back from Azure IoT Hub to the SmartController"""
import sys
import threading
from random import randrange
import time
import json

# Importing neccesary Azure_IoT_Hub Device SDK
# This sample connects to a MQTT endpoint on the IoT Hub
from azure.iot.device import IoTHubDeviceClient, Message
from azure.iot.device.exceptions import CredentialError
from azure.iot.device.exceptions import ConnectionFailedError

# DICTIONARY = '{"array: []"}'
START_TIME = time.time()
READ_INTERVAL = 5 #int
THRESHOLD = 2 # int
EQUIDISTANT = True # True or False
ULTRASONIC_MSG = '{{"DeviceId": {DeviceId}, "Ultrasonicsensor": {Ultrasonicsensor}}}'
DEVICE_ID = '"SmartController"'
# The device connection string to authenticate the device for IoT Hub access
CONNECTION_STRING = "HostName=SmartControllerTest.azure-devices.net;DeviceId=SmartControllerDemo;SharedAccessKey=ssj6oxdpm39Gjn3XtlJ2+WqOnDaFN/JrDR8Q5nLK0y8="
A_VALUE = 0  # A value between 0 and 3
ANALOG = f"in_current{A_VALUE}_raw".format()
print(CONNECTION_STRING)
print(ULTRASONIC_MSG)
print(DEVICE_ID)
print(A_VALUE)
print(EQUIDISTANT)
print(READ_INTERVAL)
print(THRESHOLD)

def send_telemetry_equidistant():
    """Send Telemtery equidistant to the database"""
    global START_TIME
    threading.Timer(READ_INTERVAL, send_telemetry_equidistant).start()
    try:
        # ultrasonicsensor = os.popen(f"cat /sys/bus/iio/devices/iio:device0/"
        #                             f"{analog}".format()).read()
        ultranosicsensor = randrange(10)
        if ultranosicsensor > THRESHOLD or  time.time() - START_TIME > (READ_INTERVAL * 5) :
            formatted_msg = ULTRASONIC_MSG.format(Ultrasonicsensor=ultranosicsensor,
                                                  DeviceId=DEVICE_ID)
            START_TIME = time.time()
            message = Message(formatted_msg)

            # Send message
            CLIENT.send_message(message)
            print(message, "Trying to data to IoT Hub endpoint")
        else:
            save_to_json(ultranosicsensor)
    except KeyboardInterrupt:
        print("Device disconnected")
    except CredentialError:
        print("wrong connection string")
    except ConnectionFailedError:
        print("no connection to the internet")
        save_to_json(message)

def save_to_json(message):
    """Save telemetry to json"""
    measurments = open('data.json')
    array = json.load(measurments)
    array.append(message)
    with open('data.json', 'w') as outfile:
        json.dump(array, outfile)

def send_telemetry_non_equidistant():
    """Send Telemtery non-equidistant to the database"""
    try:
        measurments = open('data.json')
        array = json.load(measurments)
        measurments.close()
        for value in array:
            formatted_msg = ULTRASONIC_MSG.format(Ultrasonicsensor=value, DeviceId=DEVICE_ID)
            message = Message(formatted_msg)

            # Send message
            CLIENT.send_message(message)
            print(message, "Trying to data to IoT Hub endpoint")
        with open('data.json', 'w') as outfile:
            json.dump([], outfile)

    except KeyboardInterrupt:
        print("Device disconnected")
    except CredentialError:
        print("UnauthorizedError")
    except ConnectionFailedError:
        print("no connection to the internet")

try:
    CLIENT = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    CLIENT.send_message("test")
    print(CLIENT.connected)
    if(EQUIDISTANT == True):
        send_telemetry_equidistant()
    else:
        send_telemetry_non_equidistant()

except KeyboardInterrupt:
    print("Device disconnected")
except CredentialError:
    print("UnauthorizedError")
except ConnectionFailedError:
    print("no connection to the internet")
    save_to_json("test")
