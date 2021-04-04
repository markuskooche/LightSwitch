import gc, utime
from ws281x import Ws281x
from wificonnect import connect_to_network

SLEEPTIME_SECONDS = 0.3

connect_to_network()
switch = Ws281x()


while True:
    switch.run()
    utime.sleep(SLEEPTIME_SECONDS)