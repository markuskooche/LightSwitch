import gc
import ujson
from machine import Pin
from time import sleep
from network import WLAN, AP_IF, STA_IF
from mqtt import MQTTClient
from ws281x import Ws281xController

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

# PIN CONFIGURATION
ONBOARD_LED = Pin(2, Pin.OUT)
RELAY = Pin(15, Pin.OUT)
# STATE = Pin(4, Pin.IN)

light_controller = Ws281xController(3)
light_controller.set_hex_color("00FF00")

def light_switch(topic, message):
    if (topic == b"esp-led-set" and message == b"true"):
        ONBOARD_LED.off()
        light_controller.set_is_on(True)
    elif (topic == b"esp-led-set" and message == b"false"):
        ONBOARD_LED.on()
        light_controller.set_is_on(False)

client = MQTTClient("a8b3", "raspberrypi", port=1883)
client.connect()
client.set_callback(light_switch)
client.subscribe(b"esp-led-set")

# MAIN PROGRAM
while True:
    client.check_msg()
    sleep(0.3)
