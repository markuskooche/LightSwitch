import utime
from machine import Pin
from mqtt import MQTTClient

MQTT_CLIENT_ID_RANDOM = "a8b3"
MQTT_BROKER_ADDRESS = "raspberrypi"

MQTT_PORT = 1883
KEEP_ALIVE_TIME_SEC = 600
PING_EVERY_SEC = KEEP_ALIVE_TIME_SEC * 0.9

TOPIC_LAMP_SET_ON = "esp-led-set"
TOPIC_LAMP_GET_ON = "esp-led-get"
TOPIC_LAMP_GET_ONLINE = "get_online"

TRUE_STRING = "true"
FALSE_STRING = "false"


STATE = Pin(4, Pin.IN)
CHANGE = Pin(5, Pin.OUT)


class MultiwaySwitch():

    def __init__(self):
        self.client = MQTTClient(MQTT_CLIENT_ID_RANDOM, MQTT_BROKER_ADDRESS, port=MQTT_PORT, keepalive=KEEP_ALIVE_TIME_SEC)
        self.next_scheduled_ping_time = 0
        self.previous_state = -1
        self._client_setup()
    
    def _client_setup(self):
        self.client.set_last_will(TOPIC_LAMP_GET_ONLINE, FALSE_STRING)
        self.client.connect()
        self.client.publish(TOPIC_LAMP_GET_ONLINE, TRUE_STRING)
        self.client.set_callback(self._siri_switch_handler)
        self.client.subscribe(TOPIC_LAMP_SET_ON)
        self._physical_switch_handler()

    def _physical_switch_handler(self):
        if STATE.value() != self.previous_state:
            self.previous_state = STATE.value()
            if STATE.value() == 0:
                self.client.publish(TOPIC_LAMP_GET_ON, TRUE_STRING)
            else:
                self.client.publish(TOPIC_LAMP_GET_ON, FALSE_STRING)

    def _siri_switch_handler(self, topic, msg):
        topic_string = topic.decode("utf-8")
        msg_string = msg.decode("utf-8")
        if (topic_string == TOPIC_LAMP_SET_ON):
            if (msg_string == TRUE_STRING and STATE.value() == 1) or \
                (msg_string == FALSE_STRING and STATE.value() == 0):
                CHANGE.on()
                utime.sleep(0.1)
                CHANGE.off()
    
    def _ping(self):
        if (self.next_scheduled_ping_time < utime.time() ):
            self.client.ping()
            self.next_scheduled_ping_time = utime.time() + PING_EVERY_SEC
    
    def _check_msg(self):
        self.client.check_msg()

    def run(self):
        self._ping()
        self._physical_switch_handler()
        self._check_msg()
