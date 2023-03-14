
## AUTO


## APP CONFIG
appdata = {
    "host": "localhost",
    "port": 5000,
}

## UAPI CONFIG
timeout = 21

## MQTT CONFIG
filter = "#"
querrying_period = 10

MA_CONFIG = {
    "MQTT_BROKER_URL": "siur123.pl",
    "MQTT_BROKER_PORT": 18833,
    "MQTT_USERNAME": "hackaton",
    "MQTT_PASSWORD": "",
    "MQTT_KEEPALIVE": 30,
    "MQTT_TLS_ENABLED": False,
}

devices_knownbefore = [
    # room_id: 1 - pokój
    "room/1/window/0//",
    "room/1/light/0//",
    "room/1/radiator/0//",
    "room/1/temperature/0//",
    # room_id: 2 - łazienka
    "room/2/boiler/0//",
    "room/2/light/0//",
    "room/2/window/0//",
    # room_id: 3 - przedpokój
    "room/3/light/0//",
]
"""
convert dk to hashes:
['.'.join([tag for tag in dev.split('/') if tag]) for dev in devices_knownbefore]

['room.1.window.0', 
'room.1.light.0', 
'room.1.radiator.0', 
'room.1.temperature.0', 
'room.2.boiler.0', 
'room.2.light.0', 
'room.2.window.0', 
'room.3.light.0']
"""

#devices = {}
"""
    device_hash: {
        tags: {
            "room_type": "room"
            "room_id": "0"
            "device_type": "radiator"
            "device_id": "0",
        }
        fields: {
            "state": (value, last_time_updated)
            "value": (value, last_time_updated)
        }
        field_properties: {
            "state": ("on", "off")
            "value": "float"
        }
    }
"""

states_open = ("closed", "open")
states_on = ("off", "on")
values = "float"
fields_by_device_type = {
    "window": {"state": states_open},
    "temperature": {"value": values},
    "radiator": {"state": states_on, "value": values},
    "light": {"state": states_on},
    "boiler": {"state": states_on},
}