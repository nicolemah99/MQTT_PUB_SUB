from decouple import config

### Database configuration
# Read the configuration from environment variables securely
DB_USERNAME = config('MQTT_PUB_SUB_DB_USERNAME')
DB_PASSWORD = config('MQTT_PUB_SUB_DB_PASSWORD')
DB_NAME = config('MQTT_PUB_SUB_DB_NAME')
DB_PORT = config('MQTT_PUB_SUB_DB_PORT')

# Construct the database connection URL
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"


### MQTT Broker configuration
MQTT_BROKER = 'broker.emqx.io'
MQTT_PORT = 1883
# username = 'emqx'
# password = 'public'