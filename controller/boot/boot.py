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


client = MQTTClient("a8b3", "raspberrypi", port=1883)
client.connect()
client.set_callback(light_switch)
client.subscribe(topic="esp-led-set")
# client.publish(topic="esp-led-get", msg="true")


def light_switch(topic, message):
    if (topic == "setOn" and message == "true"):
        # ONBOARD_LED.on()
        pass
    elif (topic == "setOn" and message == "false"):
        # ONBOARD_LED.off()
        pass


# PIN CONFIGURATION
ONBOARD_LED = Pin(2, Pin.OUT)
RELAY = Pin(15, Pin.OUT)
# STATE = Pin(4, Pin.IN)

STATE = 0


# MAIN PROGRAM
while True:
    STATE = (STATE + 1) % 2
    MSG = "true" if STATE == 1 else "false"

    ONBOARD_LED.value(STATE)
    client.publish(topic="esp-led-online", msg=MSG)
    sleep(2)
