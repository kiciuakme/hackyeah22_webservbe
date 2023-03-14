from flask import Blueprint, jsonify, redirect
from flask.wrappers import Response
from datetime import datetime as dt
from config import *
from mqtt_bp import set_field

devices = {}

uapi_bp = Blueprint("uapi", __name__, url_prefix="/uapi")

@uapi_bp.route("get_all", methods=["GET"])
def get_all():
    devices_cpy = {}
    for device_hash in devices.keys():
        device = dict(devices[device_hash])
        device["fields"] = {field: content 
            if (dt.now()-last_updated).seconds <= timeout else None
            for field, (content, last_updated) in device["fields"].items()}
        devices_cpy[device_hash] = device
    return jsonify(devices_cpy)

@uapi_bp.route("<device_hash>/get", methods=["GET"])
def get_device(device_hash):
    device = dict(devices[device_hash])
    device["fields"] = {field: content  
        if (dt.now()-last_updated).seconds <= timeout else None 
        for field, (content, last_updated) in device["fields"].items()}
    return jsonify(device)

@uapi_bp.route("<device_hash>/set/<field>/<content>", methods=["GET", "POST"])
def set_device(device_hash, field, content):
    # cpy: <device_hash>/<field>/set/<content>
    # rel_url = f"{device_hash}/{field}/set/{content}"
    # return redirect("/mqtt/" + rel_url)
    return set_field(device_hash, field, content)

