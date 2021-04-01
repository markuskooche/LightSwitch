## Preparing Homebridge On RaspberryPi

1. Execute [homebridge/install.sh](homebridge/install.sh) with
    ````
    ./homebridge/install.sh
    ````
2. Add the contents of [homebridge-config.json](homebridge/install.sh) to the accessories array in the homebridge config.json file at [/var/lib/homebridge/config.json](/var/lib/homebridge/config.json)
3. Restart homebridge with command
    ````
    systemctl restart homebridge.service
    ````

## Setting Up MQTT Server On RaspberryPi

1. Execute [mqtt/install.sh](mqtt/install.sh) with
    ````
    sudo ./mqtt/install.sh
    ````