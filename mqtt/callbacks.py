from database.db_utils import add_message_to_db

# Callback function: triggered when broker responds to connection request
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT Broker.\n")
    else:
        print("Failed to connect to MQTT Broker, return code %d\n", rc)

# Callback function: triggered once client receives a message from the MQTT Broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    print(f"Received `{payload}` from `{topic}` topic")
    add_message_to_db(topic, payload)


# Callback function: triggered once client receives a message from the MQTT Broker
def on_subscribe(client, userdata, mid, granted_qos):
    if granted_qos[0] == 0:
        print(f"Successfully subscribed to topic! QoS: {granted_qos[0]}")
    else:
        print("Failed to subscribe!")