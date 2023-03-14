from flask import Blueprint
from flask.wrappers import Response
from uapi_bp import get_all, get_device, set_device
from config import *
from flask_apscheduler import APScheduler

devices = {}

schedules = {}

auto_bp = Blueprint("auto", __name__, url_prefix="/auto")

# fields_by_device_type = {
#     "window": {"state": states_open},
#     "temperature": {"value": values},
#     "radiator": {"state": states_on, "value": values},
#     "light": {"state": states_on},
#     "boiler": {"state": states_on},
# }

rules = {
    "lights_on": {
        "light": {"state": "on"},
    },
    "lights_off":{
        "light": {"state": "off"},
    },
    "max_heat": {
        "window": {"state": "closed"},
        "radiator": {"state": "on"},
        "boiler": {"state": "on"}
    },
    "min_heat": {
        "window": {"state": "open"},
        "radiator": {"state": "off"},
        # "boiler": {"state": "off"},
    },
    "off_all": {
        "window": {"state": "closed"},
        "radiator": {"state": "off"},
        "light": {"state": "off"},
        "boiler": {"state": "off"},
    },
    "on_all": {
        "window": {"state": "open"},
        "radiator": {"state": "on"},
        "light": {"state": "on"},
        "boiler": {"state": "on"},
    },
}

@auto_bp.route("apply_rule/<rule>")
def apply_rule(rule):
    rule = rules[rule]
    for device_hash, device in devices.items():
        device_type = device["tags"]["device_type"]
        if device_type in rule.keys():
            for field, content in rule[device_type].items():
                set_device(device_hash, field, content)
    return Response(None, 200)

@auto_bp.route("apply_rule_room/<room_id>/<rule>")
def apply_rule_for_room(room_id, rule):
    rule = rules[rule]
    for device_hash, device in devices.items():
        device_type = device["tags"]["device_type"]
        droom_id = device["tags"]["room_id"]
        if device_type in rule.keys() and room_id == droom_id:
            for field, content in rule[device_type].items():
                set_device(device_hash, field, content)
    return Response(None, 200)


freq = 2
lmem = {0: False}
def lights():
    if lmem[0]:
        apply_rule("max_heat")
        set_device("room.1.window.0", "state", "open")
        apply_rule("lights_off")
    else:
        apply_rule("min_heat")
        apply_rule("lights_on")
    lmem[0] = not lmem[0]
    

# scheds = {schedule_name: False for schedule_name in schedules.keys()}
schscheduler = APScheduler()

@auto_bp.route("enable_schedule")
def enable_schedule():
    schscheduler.add_job(id='exemplary', func=lights, trigger='interval', seconds=freq)
    return Response(None, 200)

@auto_bp.route("disable_schedule")
def disable_schedule():
    schscheduler.delete_job(id='exemplary')
    return Response(None, 200)



