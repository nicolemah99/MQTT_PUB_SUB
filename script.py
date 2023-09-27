import random
import sys
from sqlalchemy import create_engine, exc, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config
from paho.mqtt import client as mqtt_client


# Read the configuration from environment variables securely
USERNAME = config('MQTT_PUB_SUB_DB_USERNAME')
PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DATABASE_NAME = config('MQTT_PUB_SUB_DB_NAME')
PORT = config('MQTT_PUB_SUB_DB_PORT')

# Construct the database connection URL
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"

# Define a declarative base class from which all mapped classes should inherit
Base = declarative_base()

class MQTTMessage(Base):
    """
    Define a class mapped to the mqtt_message table in the database.
    This class will be the representation of the table in the Python code.
    """
    __tablename__ = 'mqtt_message'  # Define the actual table name in the database
    # Define the columns in the table, including their types and constraints
    id = Column(Integer, Sequence('mqtt_msg_id_seq'), primary_key=True)
    topic = Column(String(50))
    payload = Column(String(500))


# Create a new instance of the Engine object to manage database connections
engine = create_engine(DATABASE_URL)
# Configure a Session class which will serve as a factory for creating Session objects
Session = sessionmaker(bind=engine)


def connect_to_database():
    """
    Establishes a connection to the database and verifies its success.
    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        with engine.connect() as connection:
            print("Database connected successfully!")
            return True
    except exc.SQLAlchemyError as e:
        # Handle any errors during connection establishment and print them to stderr
        print(f"Error: Unable to connect to the database: {e}", file=sys.stderr)
        return False


def add_message(topic, payload):
    """
    Inserts a new message into the mqtt_message table in the database.
    
    Parameters:
        topic (str): The topic of the message.
        payload (str): The payload of the message.
    """
    # Create a new session for the operation
    session = Session()
    # Create a new MQTTMessage object with the provided topic and payload
    message = MQTTMessage(topic=topic, payload=payload)
    
    try:
        # Add the new message to the session and commit it to the database
        session.add(message)
        session.commit()
        print("Data added successfully!")
    except Exception as e:
        # Rollback the transaction in case of an error during the commit
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Close the session to release the connection back to the connection pool
        session.close()


def main():
    # Connect to the database
    if connect_to_database():
        print("Connected to database")
        #client = mqtt.Client()
        #client.on_connect = on_connect
        #client.on_message = on_message
    
        # Connect to the MQTT broker
        # You will need to change the hostname to the IP address or hostname of your MQTT broker
        #client.connect("mqtt.eclipse.org", 1883, 60)  
    
        # Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting.
        #client.loop_forever()
    else:
        sys.exit(1)
    

if __name__ == "__main__":
    main()