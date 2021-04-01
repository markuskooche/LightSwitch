#!/usr/bin/env bash

brew install python3
brew install picocom
brew install pip3
pip3 install esptool
pip3 install adafruit-ampy

system_bin='system/esp8266-20200911-v1.13.bin'
port='/dev/cu.usbserial-1420'

esptool.py --port $port erase_flash
esptool.py --port $port --baud 460800 write_flash --flash_size=detect 0 $system_bin
