import redis
import time
import os

redis_host: str = os.environ.get("redis_host", "10.11.153.189")
redis_port: int = int(os.environ.get("REDIS_PORT", 6379))

def main():
    # Connect to Redis
    r = redis.Redis(host=redis_host, port=6379, db=0)

    # Publish messages to a channel
    channel = 'channel_test'
    while True:
        message = input("Enter a message to publish: ")
        r.publish(channel, message)
        print(f"Message '{message}' published to channel '{channel}'")

if __name__ == "__main__":
    main()
