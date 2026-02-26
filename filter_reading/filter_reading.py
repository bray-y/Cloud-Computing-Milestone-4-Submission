from google.cloud import pubsub_v1
import json
import os

PROJECT_ID = "cloud-milestone4"
TOPIC_ID = "smart-meter-topic"
SUBSCRIPTION_ID = "filterreading-sub"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    
    # Filter out records with missing readings
    if data.get("pressure") is not None and data.get("temperature") is not None:
        publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening to {subscription_path} for incoming smart meter readings...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()