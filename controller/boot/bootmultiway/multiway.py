import utime
from machine import Pin
from mqttdevice import MQTTDevice

#MARK: Configurable Constants
TOPIC_LAMP_SET_ON = "esp-led-set"
TOPIC_LAMP_GET_ON = "esp-led-get"
TOPIC_LAMP_GET_ONLINE = "get_online"

TRUE_STRING = "true"
FALSE_STRING = "false"

#MARK: Constants
STATE = Pin(4, Pin.IN)
CHANGE = Pin(5, Pin.OUT)


class MultiwaySwitch(MQTTDevice):

    def __init__(self):
        self.previous_state = -1
        super().__init__(TOPIC_LAMP_GET_ONLINE)

    def setup_subscriptions(self):
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
    
    def run(self):
        super().run()
        self._physical_switch_handler()
