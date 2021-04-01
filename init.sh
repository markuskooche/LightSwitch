#!/usr/bin/env bash


#brew install --build-from-source python@3.9
#xcode-select --install
#brew install picocom
#brew install pip3
#pip3 install esptool
#pip3 install adafruit-ampy

binary='binary/esp8266-[0-9]*-v*.bin'
port='/dev/cu.usbserial-1420'

esptool.py --port $port erase_flash
esptool.py --port $port --baud 460800 write_flash --flash_size=detect 0 $binary
