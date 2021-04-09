#!/usr/bin/env bash

port='/dev/cu.usbserial-1420'

ampy -p $port put ../config.json
ampy -p $port put multiway.py
ampy -p $port put ../lib/mqtt.py
ampy -p $port put ../lib/wificonnect.py
ampy -p $port put ../lib/mqttdevice.py
ampy -p $port put boot.py
ampy -p $port run -n boot.py
