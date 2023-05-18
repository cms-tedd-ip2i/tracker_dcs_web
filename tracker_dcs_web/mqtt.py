import os
import paho.mqtt.client as mqtt
from tracker_dcs_web.utils.logger import logger


mqtt_host = os.environ["MQTT_HOST"]
mqtt_port = int(os.environ["MQTT_PORT"])


def on_connect(client, userdata, flags, rc):
    logger.info(f"connected to mosquitto: {mqtt_host}:{mqtt_port}")


def on_publish(client, userdata, result):
    logger.info(f"data published: {result}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(mqtt_host, mqtt_port, 60)
client.loop_start()
