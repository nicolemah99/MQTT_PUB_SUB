import sys
from database.db_utils import connect_to_database, add_message_to_db
from mqtt.mqtt_utils import mqtt_start
from config.settings import MQTT_BROKER, MQTT_PORT

def main():
    # Connect to the database
    if connect_to_database():
        #add_message_to_db("hello/","hello world!")
        mqtt_start()
    else:
        sys.exit("Error: Unable to connect to the database!")
    

if __name__ == "__main__":
    main()