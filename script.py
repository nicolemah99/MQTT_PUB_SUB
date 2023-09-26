import sys
from sqlalchemy import create_engine, exc, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

# Database Configuration
# Using the decouple config to obtain environment variables securely
USERNAME = config('MQTT_PUB_SUB_DB_USERNAME')
PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DATABASE_NAME = config('MQTT_PUB_SUB_DB_NAME')
PORT = config('MQTT_PUB_SUB_DB_PORT')
# Constructing the DATABASE_URL using the obtained environment variables
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"

# Define a class to represent the mqtt_message table in the database
# Using declarative base for cleaner and high-level database specification
Base = declarative_base()


class MQTTMessage(Base):
    __tablename__ = 'mqtt_message'  # Define the actual table name in the database
    # Define the columns in the table, their types, and any sequences or constraints
    id = Column(Integer, Sequence('mqtt_msg_id_seq'), primary_key=True)
    topic = Column(String(50))
    payload = Column(String(500))


# Create engine to handle the connection to the Database
# The engine is the starting point for any SQLAlchemy application
engine = create_engine(DATABASE_URL)

# Attempt to connect to the database
try:
    # engine.connect() establishes a connection to the database
    with engine.connect() as connection:
        print("Database connected successfully!")
except exc.SQLAlchemyError as e:
    # Handle any errors that occur while connecting to the database
    print(f"Error: Unable to connect to the database: {e}", file=sys.stderr)
    sys.exit(1)  # Exit the script with an error code

# Create a configured "Session" class
# Session is a factory for creating new Session objects
Session = sessionmaker(bind=engine)

# Writing Data to Database
# Instantiate a session which represents the 'workspace' for our operations
session = Session()


def add_message(topic, payload):
    """
    Adds a new message to the mqtt_message table.

    :param topic: The topic of the message.
    :param payload: The payload of the message.
    """
    # Create a session
    session = Session()
    # Create an instance of MQTTMessage
    message = MQTTMessage(topic=topic, payload=payload)
    try:
        # Add the message to the session
        session.add(message)
        # Commit the transaction to write the message to the database
        session.commit()
        print("Data added successfully!")
    except Exception as e:
        # Rollback the transaction in case of error
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Always close the session
        session.close()


# Call the add_message function to add a new message
add_message("example/topic", "This is a message.")
