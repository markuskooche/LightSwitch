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

true_string = "true"
false_string = "false"

lamp_name = "wlan-lamp"
topic_lamp_set_on = lamp_name+"/set_on"
topic_lamp_set_rgb = lamp_name+"/set_rgb"

def mqtt_did_recieve(topic, message):
    topic_str = topic.decode("utf-8")
    message_str = message.decode("utf-8")
    if (topic_str == topic_lamp_set_on):
        if (message_str == true_string):
            light_controller.set_is_on(True)
            ONBOARD_LED.off()
        elif(message_str == false_string):
            light_controller.set_is_on(False)
            ONBOARD_LED.on()
    elif (topic_str == topic_lamp_set_rgb):
        rgb = message_str.split(",")
        light_controller.set_rgb_color(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
client = MQTTClient("a8b3", "raspberrypi", port=1883)
client.connect()
client.set_callback(mqtt_did_recieve)
client.subscribe(topic_lamp_set_on)
client.subscribe(topic_lamp_set_rgb)
# MAIN PROGRAM
while True:
    client.check_msg()
    sleep(0.3)
