import gc
import ujson
from machine import Pin
from time import sleep
from network import WLAN, AP_IF, STA_IF
from mqtt import MQTTClient


# NETWORK CONFIGURATION
def connect_to_network():
    with open("config.json", "r") as file:
        config = ujson.load(file)

    ssid = config["credentials"]["ssid"]
    password = config["credentials"]["password"]

    access_point = WLAN(AP_IF)
    access_point.active(False)
    
    station = WLAN(STA_IF)
    station.active(True)

    if not station.isconnected():
        print('Verbindung zu', ssid, 'wird hergestellt...')
        station.connect(ssid, password)

        while not station.isconnected():
            pass
    
    print('Verbindung wurde hergestellt!')
    print('Netzwerkverbinung:', station.ifconfig())

connect_to_network()


# MQTT CONFIGURATION
# client = MQTTClient("device_id", "io.adafruit.com", user="your_username", password="your_api_key", port=1883)
# client.connect()
# client.subscribe(topic="youraccount/feeds/lights")


# PIN CONFIGURATION
ONBOARD_LED = Pin(2, Pin.OUT)
RELAY = Pin(15, Pin.OUT)
#STATE = Pin(4, Pin.IN)

STATE = 0


# MAIN PROGRAM
while True:
    STATE = (STATE + 1) % 2
    ONBOARD_LED.value(STATE)
    sleep(1)
