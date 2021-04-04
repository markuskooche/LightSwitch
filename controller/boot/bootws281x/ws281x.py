
import utime
from machine import Pin
from mqtt import MQTTClient
from ws281xctl import Ws281xController

#MARK: Configurable Constants
MQTT_CLIENT_ID_RANDOM = "a8b3"
MQTT_BROKER_ADDRESS = "raspberrypi"

LAMP_NAME = "wlan-lamp"
TOPIC_LAMP_SET_ON = LAMP_NAME+"/set_on"
TOPIC_LAMP_SET_RGB = LAMP_NAME+"/set_rgb"
TOPIC_LAMP_GET_ONLINE = LAMP_NAME+"/get_online"

NUMBER_OF_PIXELS = 3
PIN_WS281X = 4

#MARK: Constants
KEEP_ALIVE_TIME_SEC = 600
PING_EVERY_SEC = KEEP_ALIVE_TIME_SEC * 0.9
MQTT_PORT = 1883

PIN_ONBOARD_LED = 2
TRUE_STRING = "true"
FALSE_STRING = "false"

ONBOARD_LED = Pin(PIN_ONBOARD_LED, Pin.OUT)

class Ws281x:

    def __init__(self):
        self.client = MQTTClient(MQTT_CLIENT_ID_RANDOM, MQTT_BROKER_ADDRESS, port=MQTT_PORT, keepalive=KEEP_ALIVE_TIME_SEC)
        self.light_controller = Ws281xController(NUMBER_OF_PIXELS,PIN_WS281X)
        self.next_scheduled_ping_time = 0
        self._client_setup()
    
    def _client_setup(self):
        self.client.set_last_will(TOPIC_LAMP_GET_ONLINE, FALSE_STRING)
        self.client.connect()
        self.client.publish(TOPIC_LAMP_GET_ONLINE, TRUE_STRING)
        self.client.set_callback(self.mqtt_did_recieve)
        self.client.subscribe(TOPIC_LAMP_SET_ON)
        self.client.subscribe(TOPIC_LAMP_SET_RGB)


    def mqtt_did_recieve(self,topic_byte, message_byte):
        print("did recieve")
        topic = topic_byte.decode("utf-8")
        message = message_byte.decode("utf-8")
        #processing recieved topic and
        if (topic == TOPIC_LAMP_SET_ON):
            self.did_change_on(message)
        elif (topic == TOPIC_LAMP_SET_RGB):
            self.did_change_rgb(message)

    def did_change_on(self, message):
        if (message == TRUE_STRING):
            # On
            self.light_controller.set_is_on(True)
            ONBOARD_LED.off()
        elif(message == FALSE_STRING):
            # Off
            self.light_controller.set_is_on(False)
            ONBOARD_LED.on()

    def did_change_rgb(self,message):
        rgb = message_str.split(",")
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        self.light_controller.set_rgb_color(r, g, b)

    def _ping(self):
        if (self.next_scheduled_ping_time < utime.time() ):
            self.client.ping()
            self.next_scheduled_ping_time = utime.time() + PING_EVERY_SEC
    
    def _check_msg(self):
        self.client.check_msg()

    def run(self):
        self._ping()
        self._check_msg()