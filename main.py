import sys
import threading
from database.db_utils import connect_to_database, add_message_to_db
from mqtt.mqtt_utils import connect_mqtt,subscribe
from config.settings import MQTT_BROKER, MQTT_PORT

def main():
    # Connect to the database
    if connect_to_database():
        client = connect_mqtt()
        subscribe(client)
        mqtt_thread = threading.Thread(target=client.loop_forever, args=())
        mqtt_thread.start()

        try:
            input("Press Enter to stop the script...")
        except KeyboardInterrupt:
            pass
        finally:
            print("Disconnecting MQTT Client...")
            client.disconnect()  # Disconnect the client
            mqtt_thread.join()  # Ensure the MQTT thread has finished
            print("MQTT Client Disconnected. Exiting...")

    else:
        sys.exit("Error: Unable to connect to the database!")
    

if __name__ == "__main__":
    main()