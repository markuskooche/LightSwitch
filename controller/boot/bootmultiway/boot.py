import gc, utime
from multiway import MultiwaySwitch
from wificonnect import connect_to_network

SLEEPTIME_SECONDS = 0.05

connect_to_network()
switch = MultiwaySwitch()


while True:
    switch.run()
    utime.sleep(SLEEPTIME_SECONDS)
