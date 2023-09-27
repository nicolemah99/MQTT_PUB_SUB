# python3.6
import random
from paho.mqtt import client as mqtt_client
from mqtt import callbacks

broker = 'broker.emqx.io'
port = 1883
topic_list = ["sports/skiing", "sports/football"]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# Callback function: triggered when broker responds to connection request
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT Broker.\n")
    else:
        print("Failed to connect to MQTT Broker, return code %d\n", rc)

# Callback function: triggered once client receives a message from the MQTT Broker
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


# Callback function: triggered once client receives a message from the MQTT Broker
def on_subscribe(client, userdata, mid, granted_qos):
    if granted_qos[0] == 0:
        print(f"Successfully subscribed to topic! QoS: {granted_qos[0]}")
    else:
        print("Failed to subscribe!")

def connect_mqtt() -> mqtt_client:  # returns instance of mqtt_client
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = callbacks.on_connect
    client.connect(broker, port)
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
