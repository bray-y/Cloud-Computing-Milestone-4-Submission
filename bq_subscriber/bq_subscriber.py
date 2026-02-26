# bq_subscriber.py
import json
from datetime import datetime
from google.cloud import pubsub_v1, bigquery

# -----------------------------
# Configuration
# -----------------------------
PROJECT_ID = "cloud-milestone4"
TOPIC_ID = "smart-meter-topic"
SUBSCRIPTION_ID = "bq-sub"
DATASET_ID = "smart_meter_dataset"
TABLE_ID = "processed_readings"

# -----------------------------
# Initialize clients
# -----------------------------
subscriber = pubsub_v1.SubscriberClient()
bq_client = bigquery.Client(project=PROJECT_ID)

subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# -----------------------------
# Callback for incoming messages
# -----------------------------
def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))

        # Convert types to match BigQuery schema
        row = {
            "meter_id": str(data["meter_id"]),
            "timestamp": datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            "pressure": float(data["pressure"]),
            "temperature": float(data["temperature"]),
        }

        # Insert row into BigQuery
        errors = bq_client.insert_rows_json(table_ref, [row])
        if errors:
            print("BigQuery insertion errors:", errors)
        else:
            print(f"Inserted row into BigQuery: {row}")

        # Acknowledge message
        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

# -----------------------------
# Start subscriber
# -----------------------------
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\nPress Ctrl+C to exit.")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("Stopped subscriber.")