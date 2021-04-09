import utime
from mqtt import MQTTClient


MQTT_CLIENT_ID_RANDOM = "a8b3"
MQTT_BROKER_ADDRESS = "raspberrypi"

MQTT_PORT = 1883
KEEP_ALIVE_TIME_SEC = 600
PING_EVERY_SEC = KEEP_ALIVE_TIME_SEC * 0.9

#this class should be the superclass of every device with MQTT Functionality
#its __init__ ; setup_subscriptions ; and run methods may be overwritten
#the run method has to be called every execution cycle
class MQTTDevice:

    def __init__(self,topic_online,true_message="true",false_message="false"):
        self.true_message = true_message
        self.false_message = false_message
        self.client = MQTTClient(MQTT_CLIENT_ID_RANDOM, MQTT_BROKER_ADDRESS, port=MQTT_PORT, keepalive=KEEP_ALIVE_TIME_SEC)
        self.next_scheduled_ping_time = 0
        self._client_setup(topic_online)
    
    def _client_setup(self,topic_online):
        self.client.set_last_will(topic_online, self.false_message)
        self.client.connect()
        self.client.publish(topic_online, self.true_message)
        self.setup_subscriptions()

    # override this method in subclass
    # set callback and subscriptions
    def setup_subscriptions(self):
        pass
    
    def _ping(self):
        if (self.next_scheduled_ping_time < utime.time() ):
            self.client.ping()
            self.next_scheduled_ping_time = utime.time() + PING_EVERY_SEC

    #run method has to be called every execution cycle
    def run(self):
        self._ping()
        self.client.check_msg()
