# python3.6
import random
from paho.mqtt import client as mqtt_client
from config.settings import BROKER, PORT
from mqtt import callbacks

topic_list = ["sports/skiing", "sports/football"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:  # returns instance of mqtt_client
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = callbacks.on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client):
    client.on_subscribe = callbacks.on_subscribe
    client.on_message = callbacks.on_message
    for topic in topic_list:
        client.subscribe(topic)


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
