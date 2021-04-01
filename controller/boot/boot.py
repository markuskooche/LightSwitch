import gc
from machine import Pin


# CONFIGURATION
ONBOARD_LED = Pin(2, Pin.OUT)
RELAY = Pin(15, Pin.OUT)
STATE = Pin(4, Pin.IN)


# MAIN PROGRAM
while True:
    
