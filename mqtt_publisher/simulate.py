import os
import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = 1883

topics = ["canbus/speed", "canbus/temp", "canbus/door"]

def generate_payload(topic):
    if "speed" in topic:
        return str(random.randint(0, 120))  # km/h
    elif "temp" in topic:
        return str(round(random.uniform(15.0, 30.0), 1))  # °C
    elif "door" in topic:
        return random.choice(["open", "closed"])
    return "unknown"

# Setup client
client = mqtt.Client()

print(f"[{datetime.now()}] 🔌 Connecting to MQTT broker at '{MQTT_HOST}:{MQTT_PORT}'...")
try:
    client.connect(MQTT_HOST, MQTT_PORT)
except Exception as e:
    print(f"[{datetime.now()}] ❌ Failed to connect to MQTT broker: {e}")
    exit(1)

print(f"[{datetime.now()}] ✅ Connected to broker. Starting publish loop...")

client.loop_start()

try:
    while True:
        for topic in topics:
            payload = generate_payload(topic)
            client.publish(topic, payload)
            print(f"[{datetime.now()}] 📡 Sent '{payload}' to topic '{topic}'")
            time.sleep(1)
except KeyboardInterrupt:
    print(f"\n[{datetime.now()}] ⛔ Stopped by user.")
finally:
    client.loop_stop()
    client.disconnect()
