import redis
import os

redis_host: str = os.environ.get("redis_host", "localhost")
redis_port: int = int(os.environ.get("REDIS_PORT", 6379))

def main():
    # Connect to Redis
    r = redis.Redis(host=redis_host, port=6379, db=0)

    # Subscribe to a channel
    pubsub = r.pubsub()
    channel = 'channel_test'
    pubsub.subscribe(channel)
    print(f"Subscribed to channel '{channel}'")

    # Listen for messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")

if __name__ == "__main__":
    main()
