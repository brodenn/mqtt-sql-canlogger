import os
import time
import psycopg2
import paho.mqtt.client as mqtt

# 📦 Anslut till PostgreSQL med fallback-värden från miljövariabler
db_conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "mqtt"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASS", "postgres"),
    host=os.getenv("DB_HOST", "db")
)
cursor = db_conn.cursor()

# 🔧 Skapa topic om det inte finns, hämta ID
def get_or_create_topic_id(topic):
    cursor.execute(
        "INSERT INTO topics (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (topic,)
    )
    db_conn.commit()
    cursor.execute("SELECT id FROM topics WHERE name = %s", (topic,))
    return cursor.fetchone()[0]

# 📥 Callback vid mottaget MQTT-meddelande
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode(errors="replace")
    topic_id = get_or_create_topic_id(topic)
    cursor.execute(
        "INSERT INTO messages (topic_id, payload) VALUES (%s, %s)",
        (topic_id, payload)
    )
    db_conn.commit()
    print(f"📦 Saved message: {topic} -> {payload}")

# 🔌 MQTT-inställningar
mqtt_host = os.getenv("MQTT_HOST", "mosquitto")
client = mqtt.Client()
client.on_message = on_message

# ♻️ Retry-loop för att vänta in MQTT-broker
for attempt in range(10):
    try:
        print(f"🔌 Trying to connect to MQTT broker at '{mqtt_host}' (attempt {attempt+1}/10)")
        client.connect(mqtt_host, 1883)
        print("✅ Connected to MQTT broker.")
        break
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        time.sleep(2)
else:
    print("❗ Could not connect to MQTT broker after 10 attempts. Exiting.")
    exit(1)

# 📡 Prenumerera och starta loopen
client.subscribe("canbus/#")
client.loop_forever()
