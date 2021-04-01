# LightSwitch


## Table of Contents
1. Installation
    1. a
    2. b
    3. c
2. ...


Please create a [config.json](./controller/boot/config.json) file
```
{
    "credentials": {
        "ssid": "YOUR_SSID",
        "password": "YOUR_PASSWORD"
    }
}
```

## HOW TO FLASH A ESP8266
1. Please make sure your controller is connected with a DATA CABLE.
2. Open the terminal and navigate into this directory
3. Run the init.sh script to install al dependencies and flash the controller.
```
#!/usr/bin/env bash

brew install --build-from-source python@3.9
xcode-select --install
brew install picocom
brew install pip3
pip3 install esptool
pip3 install adafruit-ampy

binary='binary/esp8266-[0-9]*-v*.bin'
port='/dev/cu.usbserial-1420'

esptool.py --port $port erase_flash
esptool.py --port $port --baud 460800 write_flash --flash_size=detect 0 $binary
```


## HOW TO INSTALL NODE.JS & HOMEBRIDGE ON A RASPBERRY PI

1. Setup the Repository
```
curl -sL https://deb.nodesource.com/setup_14.16.0 | sudo bash -
````

2. Install node.js additional packages
sudo apt install -y nodejs gcc g++ make python net-tools

3. Upgrade node.js to the newest LTS version
```
wget http://nodejs.org/dist/v14.16.0/node-v14.16.0-linux-armv7l.tar.xz
```

4. Unpack the node.js LTS version
```
tar -xvf node-v14.16.0-linux-armv7l.tar.xz
```

5. Navigate into the unpacked folder
```
cd node-v14.16.0-linux-armv7l.tar.xz
````

6. Transfer the folder and restart your device
```
sudo cp -R * /usr/local/
shutdown -r now
```

7. Install Homebridge and Homebridge UI
```
sudo npm install -g --unsafe-perm homebridge homebridge-config-ui-x
```

8. Setup Homebridge as a service that will start on boot
```
sudo hb-service install --user homebridge
```

9. Make sure that you have all npm packages are update to date
```
npm install -g npm-check-updates
```

10. Restart your device
```
shutdown -r now
```

Now homebridge is runing on port 8581

You can get your IP Adress with this command
```
hostname -I
```

## Technologies
***
A list of technologies used within the project:
* [Node.js](https://nodejs.org): Version 14.16.0