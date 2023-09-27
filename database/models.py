from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base

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