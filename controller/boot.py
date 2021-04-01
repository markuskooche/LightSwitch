from machine import Pin
from time import sleep


# CONFIGURATION
LED = Pin(2, Pin.OUT)


# MAIN PROGRAM
while True:
    LED.value(not LED.value())
    sleep(0.5)
