#!/bin/bash

#checking for root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#setup mqtt mosquitto
apt-get update

apt-get install -y mosquitto mosquitto-clients

systemctl enable mosquitto.service