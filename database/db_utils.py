import sys
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from database.models import MQTTMessage

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
        print(f"{payload} successfully added to {topic}")
    except Exception as e:
        # Rollback the transaction in case of an error during the commit
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Close the session to release the connection back to the connection pool
        session.close()