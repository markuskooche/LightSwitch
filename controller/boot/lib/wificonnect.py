import ujson
from network import WLAN, AP_IF, STA_IF


def connect_to_network():
    with open("config.json", "r") as file:
        config = ujson.load(file)

    ssid = config["credentials"]["ssid"]
    password = config["credentials"]["password"]

    access_point = WLAN(AP_IF)
    access_point.active(False)
    
    station = WLAN(STA_IF)
    station.active(True)

    if not station.isconnected():
        print('Verbindung zu', ssid, 'wird hergestellt...')
        station.connect(ssid, password)

        while not station.isconnected():
            pass
    
    print('Verbindung wurde hergestellt!')
    print('Netzwerkverbinung:', station.ifconfig())
