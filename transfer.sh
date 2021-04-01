#!/usr/bin/env bash

port='/dev/cu.usbserial-1420'

ampy -p $port put controller/boot.py
ampy -p $port run -n controller/boot.py
