#!/usr/bin/env bash

port='/dev/cu.usbserial-1420'

ampy -p $port put boot/boot.py
ampy -p $port run -n boot/boot.py