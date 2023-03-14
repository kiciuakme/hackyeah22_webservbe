from flask import Blueprint
from flask.wrappers import Response
from flask_mqtt import Mqtt
from flask_apscheduler import APScheduler
from datetime import datetime as dt
from config import *

devices = {}

def unify(field, content):  # 2be changed prolly
    # if field == "status":
    #     if content in ("open", "on"):
    #         si = 1
    #     elif content in ("closed", "off"):
    #         si = 0
    #     else:
    #         raise NotImplementedError
    #     return (si, field)
    # elif field == "value":
    #     return float(content)
    return content


def is_setable(field):
    return field == "status"

## PARSER
class MQTT_Topic:
    format = (
        "room_type/room_id/device_type/device_id",  # device_tags
        "field", # field
        "method", # method
    )
    format_join = '/'.join(format)
    format_tags = [tag for tag in format[0].split('/') if tag]
    format_splits = (slice(0,4), 4, 5)

    def __init__(self, topic):
        # [tag for tag in "/".join(topic_format_tags).split('/') if tag]
        topic_split = topic.split('/')
        self.tag_tuple = topic_split[self.format_splits[0]]
        self.field = topic_split[self.format_splits[1]]
        self.method = topic_split[self.format_splits[2]]

    def to_hash(self):
        return '.'.join(self.tag_tuple)

    def to_dict(self):
        return dict(zip(self.format_tags, self.tag_tuple))

## INIT
for topic in devices_knownbefore:
    topic = MQTT_Topic(topic)
    device_hash = topic.to_hash()
    device_tags = topic.to_dict()
    device_type = device_tags["device_type"]
    fields = fields_by_device_type[device_type]
    field_keys = fields.keys()
    devices[device_hash] = {
        "tags": device_tags,
        "fields": {field_key: (None, dt.now()) for field_key in field_keys},
        "field_properties": fields
    }

mqtt_client = Mqtt()

## MQTT -> WEBSERV    
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       mqtt_client.subscribe(filter) # subscribe topic
   else:
        pass # print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    topic=message.topic
    content=message.payload.decode()

    if type(topic) is tuple:
        topic = ''.join(topic)  # KS, lat 23 - ma dość

    if topic.endswith("/rsp"): # method; vbasic safeguard
        topic = MQTT_Topic(topic)
        device_hash = topic.to_hash()
        content = unify(topic.field, content)

        devices[device_hash]["fields"][topic.field] = (content, dt.now())
    return

## WEBSERV -> MQTT
mqtt_bp = Blueprint("mqtt", __name__, url_prefix="/mqtt")

@mqtt_bp.route("<device_hash>/<field>/get", methods=["GET"])
def get_field(device_hash, field):
    topic_device_hash = device_hash.replace('.', '/')
    topic = f'{topic_device_hash}/{field}/get'
    rc = mqtt_client.publish(topic, None)
    return Response(None, 200) if not rc[0] else Response("Sth went wrong", 400)


@mqtt_bp.route("<device_hash>/<field>/set/<content>", methods=["GET", "POST"])
def set_field(device_hash, field, content):
    topic_device_hash = device_hash.replace('.', '/')
    topic = f'{topic_device_hash}/{field}/set'
    rc = mqtt_client.publish(topic, content)
    return Response(None, 200) if not rc[0] else Response("Sth went wrong", 400)


## CRON
def querry_nodes():
    for device_hash, device in devices.items():
        for field in device["fields"].keys():
            get_field(device_hash, field)
    # print(devices) #DG

scheduler = APScheduler()
scheduler.add_job(id='querry_nodes', func=querry_nodes, 
    trigger='interval', seconds=querrying_period)


