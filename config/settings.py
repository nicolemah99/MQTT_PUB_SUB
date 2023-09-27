from decouple import config

### Database configuration
# Read the configuration from environment variables securely
USERNAME = config('MQTT_PUB_SUB_DB_USERNAME')
PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DATABASE_NAME = config('MQTT_PUB_SUB_DB_NAME')
PORT = config('MQTT_PUB_SUB_DB_PORT')

# Construct the database connection URL
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"


### MQTT Broker configuration
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
# username = 'emqx'
# password = 'public'