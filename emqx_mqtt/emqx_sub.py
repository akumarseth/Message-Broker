import json
import random
import time
import os
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import dotenv

dotenv.load_dotenv()

broker=os.getenv('MQTT_HOST')
port=os.getenv('MQTT_PORT')
username=os.getenv('MQTT_USERNAME')
password=os.getenv('MQTT_PASSWORD')

topic = "python001"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
FLAG_CONNECTED = 0


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def subscribe(client):
    client.subscribe(topic, qos=2)
    client.on_message = on_message


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        subscribe(client)

    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def connect_mqtt():
    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def run():
    client = connect_mqtt()
    time.sleep(5)
    client.loop_forever()
    # client.loop_start()
    # if FLAG_CONNECTED:
    #     while True:
    #         subscribe(client)
    # else:
    #     client.loop_stop()


if __name__ == '__main__':
    run()
