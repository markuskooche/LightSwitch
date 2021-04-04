import gc, utime
from multiway import MultiwaySwitch
from wificonnect import connect_to_network


connect_to_network()
switch = MultiwaySwitch()


while True:
    switch.run()
    utime.sleep(0.2)
