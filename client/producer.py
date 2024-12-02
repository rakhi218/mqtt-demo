#standard package
import json
import time

#third party
import random
import paho.mqtt.client as mqtt

# Connect to the MQTT broker
def create_mqtt_connection():
    try:
        # Initialize MQTT Client
        mqtt_client = mqtt.Client()
        mqtt_client.connect("localhost", 1883, 60)
        return mqtt_client
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    print("Message Published with MID - ", mid)

mqtt_client = create_mqtt_connection()
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.loop_start()

# Publish messages to the MQTT topic every 1 second
count = 0
while True:
    t = random.randint(0, 6)
    count += 1
    msg = {"status": t, "count": count}
    mqtt_client.publish("mqtt_topic", json.dumps(msg), qos=1, retain=False)
    time.sleep(1)