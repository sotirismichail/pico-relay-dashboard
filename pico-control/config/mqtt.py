MQTT_CLIENT_ID = "WavesharePicoRelay-B"
MQTT_HOST = "HOST_IP"
MQTT_PORT = 1883  # The default RabbitMQ port for MQTT
MQTT_USER = "relay_user"
MQTT_PASS = "relay_pass"
SUBSCRIBE_TOPIC = b"control.relays.cmd.picorelay"
PUBLISH_TOPIC = b"control.relays.status.picorelay"
PUBLISH_INTERVAL = 5
