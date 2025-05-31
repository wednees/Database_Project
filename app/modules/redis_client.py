# modules/redis_client.py
import redis
import os
from dotenv import load_dotenv
import json

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    # password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True  # чтобы возвращать строки вместо bytes
)

def publish_event(channel, message):
    redis_client.publish(channel, json.dumps(message))

def subscribe_to_channel(channel, callback):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message['type'] == 'message':
            callback(json.loads(message['data']))