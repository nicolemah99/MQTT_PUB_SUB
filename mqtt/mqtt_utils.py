# python3.6
import random
from paho.mqtt import client as mqtt_client
from config.settings import MQTT_BROKER, MQTT_PORT
from mqtt import callbacks

topic_list = ["sports/skiing", "sports/football"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:  # returns instance of mqtt_client
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = callbacks.on_connect
    client.on_subscribe = callbacks.on_subscribe
    client.on_message = callbacks.on_message
    client.on_disconnect = callbacks.on_disconnect
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client


def subscribe(client: mqtt_client):
    for topic in topic_list:
        client.subscribe(topic)
