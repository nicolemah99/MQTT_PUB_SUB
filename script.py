import sys
from sqlalchemy import create_engine, exc, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from decouple import config

# Define a class that represents the mqtt_messages table
Base = declarative_base()

class MQTTMessage(Base):
    __tablename__ = 'mqtt_messages'  # should match the actual table name
    id = Column(Integer, Sequence('mqtt_msg_id_seq'), primary_key=True)
    topic = Column(String(50))
    payload = Column(String(500))


# Replace with your actual PostgreSQL database connection details
USERNAME = config('MQTT_PUB_SUB_DB_USERNAME') # Fixed the environment variable name
PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DATABASE_NAME = config('MQTT_PUB_SUB_DB_NAME')  # replace with your database name
PORT = config('MQTT_PUB_SUB_DB_PORT')

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

try:
    # Try to create a connection to the database
    with engine.connect() as connection:
        print("Database connected successfully!")
except exc.SQLAlchemyError as e:
    print(f"Error: Unable to connect to the database: {e}", file=sys.stderr)
    sys.exit(1)  # Exit the script with an error code
    
Session = sessionmaker(bind=engine)



