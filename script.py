import sys
from sqlalchemy import create_engine, exc, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

# Database Configuration
USERNAME = config('MQTT_PUB_SUB_DB_USERNAME')
PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DATABASE_NAME = config('MQTT_PUB_SUB_DB_NAME')
PORT = config('MQTT_PUB_SUB_DB_PORT')
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"

Base = declarative_base()


class MQTTMessage(Base):
    __tablename__ = 'mqtt_message'
    id = Column(Integer, Sequence('mqtt_msg_id_seq'), primary_key=True)
    topic = Column(String(50))
    payload = Column(String(500))


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def connect_to_database():
    """
    Function to connect to the database and print a success message 
    if the connection is established successfully.
    """
    try:
        with engine.connect() as connection:
            print("Database connected successfully!")
            return True
    except exc.SQLAlchemyError as e:
        print(
            f"Error: Unable to connect to the database: {e}", file=sys.stderr)
        return False


def add_message(topic, payload):
    session = Session()
    message = MQTTMessage(topic=topic, payload=payload)
    try:
        session.add(message)
        session.commit()
        print("Data added successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    if connect_to_database():
        add_message("example/topic", "This is a message.")
    else:
        sys.exit(1)
