import gc
import ujson
from machine import Pin
import utime
from network import WLAN, AP_IF, STA_IF
from mqtt import MQTTClient
from ws281x import Ws281xController

#MARK: Configurable Constants
SLEEPTIME_SECONDS = 0.3
NUMBER_OF_PIXELS = 3
PIN_WS281X = 4
MQTT_CLIENT_ID_RANDOM = "a8b3"
MQTT_BROKER_ADDRESS = "raspberrypi"
LAMP_NAME = "wlan-lamp"
TOPIC_LAMP_SET_ON = LAMP_NAME+"/set_on"
TOPIC_LAMP_SET_RGB = LAMP_NAME+"/set_rgb"
TOPIC_LAMP_GET_ONLINE = LAMP_NAME+"/get_online"

#MARK: Constants
PIN_ONBOARD_LED = 2
TRUE_STRING = "true"
FALSE_STRING = "false"
MQTT_PORT = 1883
KEEP_ALIVE_TIME_SEC = 600
PING_EVERY_SEC = KEEP_ALIVE_TIME_SEC * 0.9

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

#MARK: Lights

# LIGHTS CONFIGURATION
ONBOARD_LED = Pin(PIN_ONBOARD_LED, Pin.OUT)
LIGHT_CONTROLLER = Ws281xController(NUMBER_OF_PIXELS,PIN_WS281X)

def mqtt_did_recieve(topic, message):
    topic_str = topic.decode("utf-8")
    message_str = message.decode("utf-8")
    #processing recieved topic and
    if (topic_str == TOPIC_LAMP_SET_ON):
        if (message_str == TRUE_STRING):
            # On
            LIGHT_CONTROLLER.set_is_on(True)
            ONBOARD_LED.off()
        elif(message_str == FALSE_STRING):
            # Off
            LIGHT_CONTROLLER.set_is_on(False)
            ONBOARD_LED.on()
    elif (topic_str == TOPIC_LAMP_SET_RGB):
        #rgb change
        rgb = message_str.split(",")
        LIGHT_CONTROLLER.set_rgb_color(int(rgb[0]), int(rgb[1]), int(rgb[2]))


#MARK: MQTT
client = MQTTClient(MQTT_CLIENT_ID_RANDOM, MQTT_BROKER_ADDRESS , port=MQTT_PORT, keepalive=KEEP_ALIVE_TIME_SEC)
client.set_last_will(TOPIC_LAMP_GET_ONLINE, FALSE_STRING)
client.connect()
client.publish(TOPIC_LAMP_GET_ONLINE, TRUE_STRING)
client.set_callback(mqtt_did_recieve)
client.subscribe(TOPIC_LAMP_SET_ON)
client.subscribe(TOPIC_LAMP_SET_RGB)

next_scheduled_ping_time = 0

#MARK: MAIN PROGRAM
while True:
    #ping to ensure that the keep alive time will not expire
    if (next_scheduled_ping_time < utime.time() ):
        client.ping()
        next_scheduled_ping_time = utime.time() + PING_EVERY_SEC
    #normal execution
    client.check_msg()
    utime.sleep(SLEEPTIME_SECONDS)