
from machine import Pin
from mqttdevice import MQTTDevice
from ws281xctl import Ws281xController

#MARK: Configurable Constants
LAMP_NAME = "wlan-lamp"
TOPIC_LAMP_SET_ON = LAMP_NAME+"/set_on"
TOPIC_LAMP_SET_RGB = LAMP_NAME+"/set_rgb"
TOPIC_LAMP_GET_ONLINE = LAMP_NAME+"/get_online"

NUMBER_OF_PIXELS = 3
PIN_WS281X = 4

#MARK: Constants
PIN_ONBOARD_LED = 2
TRUE_STRING = "true"
FALSE_STRING = "false"

ONBOARD_LED = Pin(PIN_ONBOARD_LED, Pin.OUT)


class Ws281x(MQTTDevice):
    
    def __init__(self):
        self.light_controller = Ws281xController(NUMBER_OF_PIXELS,PIN_WS281X)
        super().__init__(TOPIC_LAMP_GET_ONLINE)

    def setup_subscriptions(self):
        self.client.set_callback(self.mqtt_did_recieve)
        self.client.subscribe(TOPIC_LAMP_SET_ON)
        self.client.subscribe(TOPIC_LAMP_SET_RGB)

    def mqtt_did_recieve(self,topic_byte, message_byte):
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
        rgb = message.split(",")
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        self.light_controller.set_rgb_color(r, g, b)
