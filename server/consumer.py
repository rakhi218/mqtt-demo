#standard package
import json
from datetime import datetime

#third party
import pymongo
from fastapi import FastAPI
import paho.mqtt.client as mqtt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["mqtt-db"]
collection = db["statusCollection"]

# Connect to the MQTT broker
def create_mqtt_connection():
    try:
        # Initialize MQTT Client
        mqtt_client = mqtt.Client(client_id="consumner1", clean_session=False)
        mqtt_client.connect("localhost", 1883, 60)
        return mqtt_client
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# consumer code
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    obj = json.loads(msg.payload.decode())
    obj["timestamp"] = datetime.now()
    print(f"inserting data to mongo - {obj}")
    collection.insert_one(obj)

# initializing fastAPI app
app = FastAPI()

mqtt_client = create_mqtt_connection()
mqtt_client.on_connect = on_connect
mqtt_client.subscribe("mqtt_topic", qos=1)
mqtt_client.on_message = on_message

mqtt_client.loop_start()

@app.get("/get-status-count")
async def aggregate_data(start: str, end: str):
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except Exception:
        return "provide datetime in valid format"

    pipeline = [
        {"$match": {"timestamp": {"$gte": start_dt, "$lt": end_dt}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$project": {"status": "$_id", "count": 1, "_id": 0}},
        {"$sort": {"count": pymongo.DESCENDING}},
    ]

    result = list(collection.aggregate(pipeline))

    r = []
    for doc in result:
        print(f"Status: {doc['status']}, Count: {doc['count']}")
        r.append({"Status": doc["status"], "Count": doc["count"]})

    return r